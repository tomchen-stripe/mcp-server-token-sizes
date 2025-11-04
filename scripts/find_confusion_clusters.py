#!/usr/bin/env python3
"""
Find clusters of operations that are semantically close to each other.
These clusters represent potential confusion zones for LLMs.
"""

import json
import numpy as np
from pathlib import Path
from scipy.spatial.distance import cosine
from collections import defaultdict


def load_embeddings(filepath):
    """Load embeddings from JSON file."""
    with open(filepath, 'r') as f:
        return json.load(f)


def extract_http_method(operation_id):
    """Extract HTTP method from operationId (Get, Post, Delete, Put)."""
    for method in ['Get', 'Post', 'Delete', 'Put', 'Patch']:
        if operation_id.startswith(method):
            return method
    return 'Unknown'


def find_confusion_clusters(embeddings_data, distance_threshold=0.15):
    """
    Find clusters of operations that are close to each other.

    Uses complete-linkage clustering: all members of a cluster must be within
    threshold distance of each other (not just transitively connected).

    Args:
        embeddings_data: List of dicts with operationId, description, embedding
        distance_threshold: Maximum distance to consider operations as "close"

    Returns:
        List of clusters, where each cluster is a list of operations
    """
    embeddings = np.array([op["embedding"] for op in embeddings_data])
    n = len(embeddings)

    # Compute all pairwise distances
    print(f"Computing pairwise distances for {n} operations...")
    distance_matrix = np.zeros((n, n))

    for i in range(n):
        for j in range(i + 1, n):
            dist = cosine(embeddings[i], embeddings[j])
            distance_matrix[i, j] = dist
            distance_matrix[j, i] = dist

    # Use complete-linkage clustering: all pairs within a cluster must be close
    # This prevents "chain" effects where A-B-C are clustered but A and C are far apart
    visited = set()
    clusters = []

    for i in range(n):
        if i in visited:
            continue

        # Start a new cluster with operation i
        cluster = [i]
        visited.add(i)

        # Iteratively try to add operations that are close to ALL current cluster members
        candidates_to_check = set(range(n)) - visited

        while candidates_to_check:
            added_any = False

            for j in list(candidates_to_check):
                # Check if j is within threshold distance of ALL members in current cluster
                max_dist_to_cluster = max(distance_matrix[j, member] for member in cluster)

                if max_dist_to_cluster <= distance_threshold:
                    # j is close to all cluster members - add it
                    cluster.append(j)
                    visited.add(j)
                    candidates_to_check.remove(j)
                    added_any = True
                    break  # Restart the search with updated cluster

            if not added_any:
                # No more operations can be added while maintaining tight clustering
                break

        # Keep all clusters (including singletons)
        clusters.append(cluster)

    # Convert indices to operation data
    result_clusters = []
    for cluster_indices in clusters:
        cluster_data = []
        for idx in cluster_indices:
            op = embeddings_data[idx]
            cluster_data.append({
                'operationId': op['operationId'],
                'description': op['description'],
                'http_method': extract_http_method(op['operationId'])
            })

        # Calculate internal cluster statistics
        cluster_distances = []
        for i in range(len(cluster_indices)):
            for j in range(i + 1, len(cluster_indices)):
                cluster_distances.append(distance_matrix[cluster_indices[i], cluster_indices[j]])

        result_clusters.append({
            'indices': cluster_indices,  # Keep indices for inter-cluster distance calculation
            'size': len(cluster_data),
            'operations': cluster_data,
            'max_distance': max(cluster_distances) if cluster_distances else 0,
            'avg_distance': np.mean(cluster_distances) if cluster_distances else 0
        })

    # Calculate distance to nearest cluster for each cluster
    for i, cluster_i in enumerate(result_clusters):
        min_inter_cluster_dist = float('inf')

        for j, cluster_j in enumerate(result_clusters):
            if i == j:
                continue

            # Calculate minimum distance between any two operations in different clusters
            for idx_i in cluster_i['indices']:
                for idx_j in cluster_j['indices']:
                    dist = distance_matrix[idx_i, idx_j]
                    if dist < min_inter_cluster_dist:
                        min_inter_cluster_dist = dist

        cluster_i['nearest_cluster_distance'] = min_inter_cluster_dist if min_inter_cluster_dist != float('inf') else 0

    # Sort by cluster size descending
    result_clusters.sort(key=lambda x: x['size'], reverse=True)

    return result_clusters


def analyze_confusion_risk(cluster):
    """
    Analyze confusion risk within a cluster.
    High risk: multiple operations with same HTTP method.
    Low risk: different HTTP methods (action verbs can disambiguate).
    """
    method_groups = defaultdict(list)
    for op in cluster['operations']:
        method_groups[op['http_method']].append(op['operationId'])

    # High risk if any method has 2+ operations
    high_risk_methods = {method: ops for method, ops in method_groups.items() if len(ops) >= 2}

    return {
        'method_groups': dict(method_groups),
        'high_risk_methods': high_risk_methods,
        'risk_level': 'HIGH' if high_risk_methods else 'LOW'
    }


def print_clusters(clusters, max_clusters=None):
    """Print cluster analysis."""
    if max_clusters:
        clusters = clusters[:max_clusters]

    # Count confusion clusters (size >= 2)
    confusion_count = sum(1 for c in clusters if c['size'] >= 2)
    singleton_count = sum(1 for c in clusters if c['size'] == 1)

    print(f"\n{'='*80}")
    print(f"Found {len(clusters)} total clusters")
    print(f"  - {confusion_count} confusion clusters (2+ operations)")
    print(f"  - {singleton_count} singleton clusters (1 operation)")
    print(f"{'='*80}\n")

    for i, cluster in enumerate(clusters, 1):
        risk_analysis = analyze_confusion_risk(cluster)

        print(f"Cluster {i}: {cluster['size']} operation(s)")
        if cluster['size'] >= 2:
            print(f"  Risk Level: {risk_analysis['risk_level']}")
            print(f"  Avg Internal Distance: {cluster['avg_distance']:.4f}")
            print(f"  Max Internal Distance: {cluster['max_distance']:.4f}")
        print(f"  Distance to Nearest Cluster: {cluster['nearest_cluster_distance']:.4f}")

        # Group by HTTP method
        print(f"\n  Operations by HTTP method:")
        for method, ops in sorted(risk_analysis['method_groups'].items()):
            risk_marker = " ⚠️  HIGH RISK" if method in risk_analysis['high_risk_methods'] else ""
            print(f"    {method}: {len(ops)} operation(s){risk_marker}")
            for op_id in ops:
                # Find the operation details
                op_data = next(o for o in cluster['operations'] if o['operationId'] == op_id)
                print(f"      - {op_id}")
                print(f"        {op_data['description'][:100]}...")

        print()


def export_clusters_csv(clusters, output_path):
    """Export clusters to CSV for analysis."""
    import csv

    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['cluster_id', 'cluster_size', 'risk_level', 'http_method', 'operationId', 'description', 'avg_internal_distance', 'max_internal_distance', 'nearest_cluster_distance'])

        for i, cluster in enumerate(clusters, 1):
            risk_analysis = analyze_confusion_risk(cluster)
            for op in cluster['operations']:
                writer.writerow([
                    i,
                    cluster['size'],
                    risk_analysis['risk_level'],
                    op['http_method'],
                    op['operationId'],
                    op['description'],
                    f"{cluster['avg_distance']:.6f}",
                    f"{cluster['max_distance']:.6f}",
                    f"{cluster['nearest_cluster_distance']:.6f}"
                ])

    print(f"✓ Exported {len(clusters)} clusters to {output_path}")


def main():
    base_path = Path(__file__).parent.parent

    datasets = [
        {
            'name': 'Top-Level (176 operations)',
            'embeddings_path': base_path / 'analysis/top-level-176/operation-embeddings.json',
            'output_path': base_path / 'analysis/top-level-176/confusion_clusters.csv'
        },
        {
            'name': 'All Operations (572 operations)',
            'embeddings_path': base_path / 'analysis/all-572/operation-embeddings.json',
            'output_path': base_path / 'analysis/all-572/confusion_clusters.csv'
        }
    ]

    # Test with different thresholds
    thresholds = [0.10, 0.15, 0.20]

    for dataset in datasets:
        print(f"\n{'='*80}")
        print(f"Analyzing: {dataset['name']}")
        print(f"{'='*80}")

        embeddings_data = load_embeddings(dataset['embeddings_path'])

        for threshold in thresholds:
            print(f"\n--- Distance Threshold: {threshold} ---")
            clusters = find_confusion_clusters(embeddings_data, distance_threshold=threshold)

            confusion_count = sum(1 for c in clusters if c['size'] >= 2)
            singleton_count = sum(1 for c in clusters if c['size'] == 1)

            if threshold == 0.15:  # Use 0.15 as default for export
                print_clusters(clusters, max_clusters=20)
                export_clusters_csv(clusters, dataset['output_path'])
            else:
                print(f"Found {len(clusters)} total clusters ({confusion_count} confusion, {singleton_count} singleton)")
                # Show summary of top 5 confusion clusters
                confusion_clusters = [c for c in clusters if c['size'] >= 2]
                for i, cluster in enumerate(confusion_clusters[:5], 1):
                    risk_analysis = analyze_confusion_risk(cluster)
                    print(f"  {i}. Size: {cluster['size']}, Risk: {risk_analysis['risk_level']}, "
                          f"Nearest Cluster: {cluster['nearest_cluster_distance']:.4f}, "
                          f"Methods: {list(risk_analysis['method_groups'].keys())}")


if __name__ == '__main__':
    main()
