#!/usr/bin/env python3
"""
Analyze cross-cluster ambiguity by sorting HIGH risk clusters by nearest_cluster_distance.
Shows which confusion clusters are dangerously close to other clusters.
"""

import csv
from pathlib import Path
from collections import defaultdict


def main():
    base_path = Path(__file__).parent.parent
    csv_path = base_path / 'analysis/all-572/confusion_clusters.csv'

    # Read CSV and group by cluster
    clusters = defaultdict(lambda: {
        'size': 0,
        'operations': [],
        'http_method': set(),
        'nearest_cluster_distance': 0,
        'avg_internal_distance': 0
    })

    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['risk_level'] == 'HIGH':
                cluster_id = int(row['cluster_id'])
                clusters[cluster_id]['size'] = int(row['cluster_size'])
                clusters[cluster_id]['operations'].append(row['operationId'])
                clusters[cluster_id]['http_method'].add(row['http_method'])
                clusters[cluster_id]['nearest_cluster_distance'] = float(row['nearest_cluster_distance'])
                clusters[cluster_id]['avg_internal_distance'] = float(row['avg_internal_distance'])

    # Sort by nearest_cluster_distance (ascending - most dangerous first)
    sorted_clusters = sorted(clusters.items(), key=lambda x: x[1]['nearest_cluster_distance'])

    print("HIGH RISK CLUSTERS - SORTED BY CROSS-CLUSTER RISK")
    print("(Lower nearest_cluster_distance = closer to other clusters = higher cross-cluster confusion)")
    print("=" * 100)
    print()

    # Show top 30
    for i, (cluster_id, data) in enumerate(sorted_clusters[:30], 1):
        operations = sorted(data['operations'])
        methods = ', '.join(sorted(data['http_method']))

        print(f"{i}. Cluster {cluster_id} ({data['size']} ops, {methods})")
        print(f"   Nearest Cluster Distance: {data['nearest_cluster_distance']:.4f}")
        print(f"   Avg Internal Distance: {data['avg_internal_distance']:.4f}")
        print(f"   Operations:")
        for op in operations:
            print(f"     - {op}")
        print()

    # Summary statistics
    print("=" * 100)
    print("SUMMARY STATISTICS")
    print("=" * 100)

    all_distances = [c['nearest_cluster_distance'] for c in clusters.values()]
    all_distances.sort()

    print(f"\nTotal HIGH risk clusters: {len(clusters)}")
    print(f"\nNearest Cluster Distance Distribution:")
    print(f"  Min (most dangerous):  {min(all_distances):.4f}")
    print(f"  25th percentile:       {all_distances[len(all_distances)//4]:.4f}")
    print(f"  Median:                {all_distances[len(all_distances)//2]:.4f}")
    print(f"  75th percentile:       {all_distances[3*len(all_distances)//4]:.4f}")
    print(f"  Max (most isolated):   {max(all_distances):.4f}")

    # Count dangerous clusters
    very_close = sum(1 for d in all_distances if d < 0.10)
    close = sum(1 for d in all_distances if 0.10 <= d < 0.15)
    moderate = sum(1 for d in all_distances if 0.15 <= d < 0.20)

    print(f"\nCross-cluster Risk Levels:")
    print(f"  Very High (distance < 0.10):   {very_close} clusters")
    print(f"  High (0.10 ≤ distance < 0.15):  {close} clusters")
    print(f"  Moderate (0.15 ≤ distance < 0.20): {moderate} clusters")


if __name__ == '__main__':
    main()
