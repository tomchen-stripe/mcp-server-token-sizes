#!/usr/bin/env python3
"""
Export nearest neighbor distances to CSV files for both datasets.
"""

import json
import csv
from pathlib import Path


def load_analysis(filepath):
    """Load discriminative power analysis JSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)


def export_to_csv(data, output_path):
    """Export nearest neighbor distances to CSV."""
    nn_distances = data['nn_distances']

    # Sort by distance descending
    sorted_data = sorted(nn_distances, key=lambda x: x['nn_distance'], reverse=True)

    with open(output_path, 'w', newline='') as csvfile:
        fieldnames = ['operationId', 'nn_distance', 'description']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for entry in sorted_data:
            writer.writerow({
                'operationId': entry['operationId'],
                'nn_distance': entry['nn_distance'],
                'description': entry['description']
            })

    print(f"✓ Exported {len(sorted_data)} operations to {output_path}")


def main():
    """Main function to export CSV files for both datasets."""

    base_path = Path(__file__).parent.parent

    # Dataset configurations
    datasets = [
        {
            'name': 'Top-Level (176 operations)',
            'input': base_path / 'analysis/top-level-176/discriminative-power-analysis.json',
            'output': base_path / 'analysis/top-level-176/nn_distances.csv'
        },
        {
            'name': 'All Operations (572 operations)',
            'input': base_path / 'analysis/all-572/discriminative-power-analysis.json',
            'output': base_path / 'analysis/all-572/nn_distances.csv'
        }
    ]

    print("Exporting nearest neighbor distances to CSV...\n")

    for dataset in datasets:
        print(f"Processing {dataset['name']}...")
        data = load_analysis(dataset['input'])
        export_to_csv(data, dataset['output'])

        # Print some statistics
        stats = data['nn_stats']
        print(f"  Statistics:")
        print(f"    Mean: {stats['mean']:.4f}")
        print(f"    Median: {stats['median']:.4f}")
        print(f"    Min: {stats['min']:.4f}")
        print(f"    Max: {stats['max']:.4f}")
        print(f"    Std Dev: {stats['std']:.4f}")
        print()

    print("✓ All CSV files generated successfully!")


if __name__ == '__main__':
    main()
