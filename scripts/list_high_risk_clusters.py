#!/usr/bin/env python3
"""
List all HIGH risk clusters in a readable format.
"""

import csv
from pathlib import Path
from collections import defaultdict


def extract_common_theme(operation_ids):
    """Try to extract a common theme from operation IDs."""
    if not operation_ids:
        return "Operations"

    # Remove HTTP methods
    names = []
    for op_id in operation_ids:
        for method in ['Get', 'Post', 'Delete', 'Put', 'Patch']:
            if op_id.startswith(method):
                names.append(op_id[len(method):])
                break

    # Find common prefix
    if len(names) <= 1:
        return names[0] if names else "Operations"

    # Find longest common substring
    common_parts = []
    first = names[0]

    # Check for common words/parts
    for i in range(len(first)):
        for j in range(i+3, len(first)+1):
            substr = first[i:j]
            if all(substr in name for name in names[1:]):
                common_parts.append(substr)

    if common_parts:
        # Get longest common part
        longest = max(common_parts, key=len)
        return longest

    return names[0][:30] if names else "Operations"


def main():
    base_path = Path(__file__).parent.parent
    csv_path = base_path / 'analysis/all-572/confusion_clusters.csv'

    # Read CSV and group by cluster
    clusters = defaultdict(lambda: {'size': 0, 'operations': [], 'http_method': set()})

    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['risk_level'] == 'HIGH':
                cluster_id = int(row['cluster_id'])
                clusters[cluster_id]['size'] = int(row['cluster_size'])
                clusters[cluster_id]['operations'].append(row['operationId'])
                clusters[cluster_id]['http_method'].add(row['http_method'])

    # Sort by size (descending), then by cluster_id
    sorted_clusters = sorted(clusters.items(), key=lambda x: (-x[1]['size'], x[0]))

    print(f"HIGH RISK CLUSTERS (Total: {len(sorted_clusters)})")
    print("=" * 80)
    print()

    for cluster_id, data in sorted_clusters:
        operations = sorted(data['operations'])
        theme = extract_common_theme(operations)
        methods = ', '.join(sorted(data['http_method']))

        print(f"Cluster {cluster_id}: {theme} ({data['size']} operations, {methods})")
        for op in operations:
            print(f"  - {op}")
        print()


if __name__ == '__main__':
    main()
