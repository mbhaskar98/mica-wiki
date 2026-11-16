"""Read saved Mica/Parquet results and plot granularity tradeoffs; no benchmarks.

Usage: python plot_clustering_hypothesis.py /path/to/batch
The default points to the batch inspected on 2026-11-12.
"""
from pathlib import Path
import argparse
import csv
import hashlib
import json
import math
import statistics
import subprocess

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('batch', nargs='?', type=Path,
                    default=Path('/home/mbhas/research/mica/mica/exp/results/batch-20261103T100910Z-2r2sbqiy'))
args = parser.parse_args()
batch = args.batch.resolve()
output = Path(__file__).resolve().parents[1] / 'figures'
output.mkdir(exist_ok=True)


def read_csv(path):
    with path.open() as stream:
        return list(csv.DictReader(stream))


records = []
source_paths = {batch / 'config.json'}
checks = {}
configs = json.loads((batch / 'config.json').read_text())
for config in configs:
    for mode in ('cold-read', 'warm-read', 'parquet-coalescing'):
        if mode not in config['tests']:
            continue
        summary = batch / config['name'] / mode / 'run/summary.csv'
        raw = summary.parent / 'merged_iterations.csv'
        source_paths.update((summary, raw))
        raw_rows = read_csv(raw)
        for row in read_csv(summary):
            if row['contract'] != 'exact':
                continue
            iterations = [item for item in raw_rows
                          if item['contract'] == 'exact'
                          and item['workload'] == row['workload']
                          and item['reader'] == row['reader']]
            values = [float(item['elapsed_ms']) for item in iterations]
            assert len(values) == int(row['n']) == 10
            mean = statistics.mean(values)
            assert math.isclose(mean, float(row['elapsed_ms_mean']), abs_tol=1e-5)
            matched = float(row['rows_matched_mean'])
            assert float(row['rows_returned_mean']) == matched
            key = config['dataset'], row['workload']
            checks.setdefault(key, set()).add(matched)
            record = {
                'dataset': config['dataset'], 'workload': row['workload'],
                'system': row['system'], 'configuration': config['name'],
                'reader': row['reader'], 'test': mode, 'contract': 'exact',
                'n': len(values), 'mean_ms': mean,
                'sample_sd_ms': statistics.stdev(values),
                'median_ms': statistics.median(values),
                'matched_rows': matched,
                'candidate_rows_for_decode_mean': (statistics.mean(float(item['rows_selected_for_decode']) for item in iterations) if all(item.get('rows_selected_for_decode') not in (None, '') for item in iterations) else ''),
                'final_candidate_pages_mean': (statistics.mean(float(item['pages_final']) for item in iterations) if all(item.get('pages_final') not in (None, '') for item in iterations) else ''),
                'os_read_bytes_mean': float(row['os_read_bytes_mean']),
                'data_physical_read_bytes_mean': row.get('data_physical_read_bytes_mean', ''),
                'mica_rows_per_page': (int(config['name'].rsplit('-', 1)[1])
                                       if config['format'] == 'mica' else ''),
                'summary_source': str(summary), 'iterations_source': str(raw),
            }
            records.append(record)
assert len(checks) == 14
assert all(len(counts) == 1 for counts in checks.values())

with (output / 'clustering-hypothesis.csv').open('w', newline='') as stream:
    writer = csv.DictWriter(stream, fieldnames=list(records[0]))
    writer.writeheader()
    writer.writerows(records)

# Every point is ONE fixed layout used for the entire dataset query catalog.
# Query frequencies are assumed equal; these are reweighted saved timings.
workload_rows = []
for dataset in ('nyc', 'clickbench'):
    groups = {}
    for row in records:
        if row['dataset'] != dataset or row['test'] == 'warm-read':
            continue
        key = row['system'], row['configuration'], row['test']
        groups.setdefault(key, []).append(row)
    for (system, config, test), group in groups.items():
        expected_count = 9 if dataset == 'nyc' else 5
        assert len(group) == expected_count
        workload_rows.append(dict(
            dataset=dataset, system=system, configuration=config, test=test,
            query_count=len(group), assumed_weights='equal_frequency',
            mean_reader_ms=statistics.mean(row['mean_ms'] for row in group),
            mica_rows_per_page=group[0]['mica_rows_per_page']))
with (output / 'clustering-workload-layouts.csv').open('w', newline='') as stream:
    writer = csv.DictWriter(stream, fieldnames=list(workload_rows[0]))
    writer.writeheader()
    writer.writerows(workload_rows)

plt.rcParams.update({'font.size': 10, 'axes.spines.top': False,
                     'axes.spines.right': False, 'svg.fonttype': 'none'})
fig, ax = plt.subplots(figsize=(7.6, 4.7))
baselines = []
for dataset, label, color in [('nyc', 'NYC: all 9 queries, including 2 dense cases', '#246f9f'),
                              ('clickbench', 'ClickBench: all 5 selective queries', '#b06326')]:
    subset = [row for row in workload_rows if row['dataset'] == dataset]
    mica = sorted([row for row in subset if row['system'] == 'mica'],
                  key=lambda row: row['mica_rows_per_page'])
    parquet = min([row for row in subset if row['system'] == 'parquet'],
                  key=lambda row: row['mean_reader_ms'])
    ax.plot([row['mica_rows_per_page'] for row in mica],
            [parquet['mean_reader_ms'] / row['mean_reader_ms'] for row in mica],
            marker='o', linewidth=1.9, markersize=5, label=label, color=color)
    baselines.append(dict(dataset=dataset, parquet_fixed_workload_baseline=parquet))
ax.axhline(1, color='0.3', linestyle='--', linewidth=1)
ax.text(60, 1.42, 'Equal workload mean', color='0.3', fontsize=9)
ax.set_xscale('log')
ax.set_xticks([50, 200, 800, 3200, 20000], ['50', '200', '800', '3,200', '20,000'])
ax.set_ylim(0, 6)
ax.set_xlabel('MICA target rows per page: fixed across every query')
ax.set_ylabel('Parquet workload mean / MICA workload mean')
ax.set_title('One fixed file layout serves the whole query catalog', pad=12)
ax.grid(which='major', alpha=0.18)
ax.legend(fontsize=9, loc='center right', bbox_to_anchor=(0.98, 0.56), framealpha=0.92)
fig.text(0.5, 0.035,
         'Assumed equal query frequencies; averages of saved exact cold-reader means (10 runs each).\n'
         'Parquet: one layout and reader chosen for each whole catalog from 9 layouts, plain/coalesced.\n'
         'Reweighting of one batch; not a concurrent workload run or evidence on unseen queries.',
         ha='center', fontsize=8, color='0.3')
fig.tight_layout(rect=(0, 0.16, 1, 1))
for suffix in ('png', 'svg', 'pdf'):
    fig.savefig(output / f'clustering-hypothesis.{suffix}', dpi=180, bbox_inches='tight')

# Record current code identity separately from the historical benchmark identity.
repo = batch.parents[2]
source_paths.update(repo / rel for rel in [
    'mica/src/reader/mod.rs', 'mica/src/reader/predicate.rs',
    'mica/src/writer/facade.rs', 'eval/native-format-bench/src/parquet_reader_tuned_sync.rs',
    'eval/native-format-bench/src/bin/profile_parquet_sync_lazy.rs',
    'eval/native-format-bench/src/parquet_writer.rs'])
source_paths.update(repo.parent / 'papers' / f'mica_atc26_manuscript.{suffix}' for suffix in ('pdf', 'md'))
for dataset in ('nyc', 'clickbench'):
    source_paths.add(batch / f'mica-{dataset}/tables/stages.csv')
    source_paths.add(batch / f'parquet-{dataset}/tables/metadata-comparison.csv')
provenance = {
    'batch': str(batch), 'comparison': 'one fixed layout and reader per workload; equal-frequency reweighting of exact cold-reader means',
    'benchmark_runs_executed': False, 'records_exported': len(records),
    'matched_row_count_checks': 'consistent across all exported conditions and configurations for 14 queries',
    'current_code_revision': subprocess.check_output(['git', '-C', str(repo), 'rev-parse', 'HEAD'], text=True).strip(),
    'code_revision_caveat': 'Inspected current source; not a claim that this is the historical benchmark build revision.',
    'plotted_fixed_workload_baselines': baselines,
    'workload_frequency_assumption': 'Equal frequencies within each dataset catalog; not measured arrival frequencies.',
    'sha256': {str(path): hashlib.sha256(path.read_bytes()).hexdigest()
               for path in sorted(source_paths)},
}
(output / 'clustering-hypothesis-provenance.json').write_text(json.dumps(provenance, indent=2) + '\n')
print(f'Validated and exported {len(records)} saved exact-result rows across 14 queries.')
for baseline in baselines:
    row = baseline['parquet_fixed_workload_baseline']
    print(f"{baseline['dataset']}: fixed Parquet workload mean {row['mean_reader_ms']:.3f} ms, {row['configuration']}, {row['test']}")
print('No database experiments executed.')
