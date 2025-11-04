#!/usr/bin/env python3
"""
Script to calculate discriminative power metrics for operationId embeddings.
Calculates:
- NN distance (nearest neighbor distance) for each operation
- kNN average distance for various k values
"""

import json
import sys
from pathlib import Path

import numpy as np
from scipy.spatial.distance import cosine, euclidean


def load_embeddings(filepath: str) -> list[dict]:
    """Load embeddings from JSON file."""
    with open(filepath, "r") as f:
        return json.load(f)


def compute_distance_matrix(embeddings: np.ndarray, metric: str = "cosine") -> np.ndarray:
    """
    Compute pairwise distance matrix for embeddings.

    Args:
        embeddings: Array of shape (n_samples, embedding_dim)
        metric: Distance metric to use ("cosine" or "euclidean")

    Returns:
        Distance matrix of shape (n_samples, n_samples)
    """
    n = len(embeddings)
    distances = np.zeros((n, n))

    print(f"Computing {metric} distance matrix for {n} embeddings...")

    for i in range(n):
        for j in range(i + 1, n):
            if metric == "cosine":
                dist = cosine(embeddings[i], embeddings[j])
            elif metric == "euclidean":
                dist = euclidean(embeddings[i], embeddings[j])
            else:
                raise ValueError(f"Unknown metric: {metric}")

            distances[i, j] = dist
            distances[j, i] = dist

    return distances


def calculate_nn_distances(distance_matrix: np.ndarray) -> np.ndarray:
    """
    Calculate nearest neighbor distance for each sample.

    Args:
        distance_matrix: Square distance matrix

    Returns:
        Array of NN distances for each sample
    """
    n = len(distance_matrix)
    nn_distances = np.zeros(n)

    for i in range(n):
        # Get all distances for sample i, excluding itself (distance 0)
        distances = distance_matrix[i]
        # Find minimum non-zero distance
        nn_distances[i] = np.min(distances[distances > 0])

    return nn_distances


def calculate_knn_distances(distance_matrix: np.ndarray, k_values: list[int]) -> dict:
    """
    Calculate average k-nearest neighbor distances for each sample.

    Args:
        distance_matrix: Square distance matrix
        k_values: List of k values to compute

    Returns:
        Dictionary mapping k -> array of kNN average distances
    """
    n = len(distance_matrix)
    knn_results = {}

    for k in k_values:
        if k >= n:
            print(f"Warning: k={k} >= n_samples={n}, skipping")
            continue

        knn_distances = np.zeros(n)

        for i in range(n):
            # Get all distances for sample i
            distances = distance_matrix[i]
            # Sort and take k nearest (excluding self at index 0)
            k_nearest = np.partition(distances, k)[:k + 1]
            k_nearest = k_nearest[k_nearest > 0][:k]  # Remove self and take k
            # Average distance to k nearest neighbors
            knn_distances[i] = np.mean(k_nearest)

        knn_results[k] = knn_distances

    return knn_results


def analyze_discriminative_power(
    operations: list[dict],
    nn_distances: np.ndarray,
    knn_results: dict,
    metric: str
) -> dict:
    """
    Analyze and summarize discriminative power metrics.

    Returns:
        Dictionary with analysis results
    """
    analysis = {
        "metric": metric,
        "n_operations": len(operations),
        "nn_stats": {
            "mean": float(np.mean(nn_distances)),
            "median": float(np.median(nn_distances)),
            "std": float(np.std(nn_distances)),
            "min": float(np.min(nn_distances)),
            "max": float(np.max(nn_distances)),
            "q25": float(np.percentile(nn_distances, 25)),
            "q75": float(np.percentile(nn_distances, 75)),
        },
        "knn_stats": {}
    }

    # Add per-operation NN distances
    analysis["nn_distances"] = [
        {
            "operationId": operations[i]["operationId"],
            "nn_distance": float(nn_distances[i]),
            "description": operations[i]["description"]
        }
        for i in range(len(operations))
    ]

    # Sort by NN distance to find most/least discriminative
    analysis["nn_distances"].sort(key=lambda x: x["nn_distance"])

    # kNN statistics
    for k, distances in knn_results.items():
        analysis["knn_stats"][f"k={k}"] = {
            "mean": float(np.mean(distances)),
            "median": float(np.median(distances)),
            "std": float(np.std(distances)),
            "min": float(np.min(distances)),
            "max": float(np.max(distances)),
        }

        # Store per-operation kNN distances
        analysis[f"knn_k{k}_distances"] = [
            {
                "operationId": operations[i]["operationId"],
                f"knn_k{k}_distance": float(distances[i]),
            }
            for i in range(len(operations))
        ]

    return analysis


def print_summary(analysis: dict):
    """Print summary of discriminative power analysis."""
    print("\n" + "=" * 80)
    print("DISCRIMINATIVE POWER ANALYSIS")
    print("=" * 80)

    print(f"\nMetric: {analysis['metric']}")
    print(f"Total operations: {analysis['n_operations']}")

    print("\n--- Nearest Neighbor (NN) Distance Statistics ---")
    nn_stats = analysis["nn_stats"]
    print(f"  Mean:   {nn_stats['mean']:.6f}")
    print(f"  Median: {nn_stats['median']:.6f}")
    print(f"  Std:    {nn_stats['std']:.6f}")
    print(f"  Min:    {nn_stats['min']:.6f}")
    print(f"  Max:    {nn_stats['max']:.6f}")
    print(f"  Q25:    {nn_stats['q25']:.6f}")
    print(f"  Q75:    {nn_stats['q75']:.6f}")

    print("\n--- Most Discriminative (Highest NN Distance) ---")
    top_5 = analysis["nn_distances"][-5:][::-1]
    for i, op in enumerate(top_5, 1):
        print(f"{i}. {op['operationId']}: {op['nn_distance']:.6f}")
        print(f"   Description: {op['description'][:80]}...")

    print("\n--- Least Discriminative (Lowest NN Distance) ---")
    bottom_5 = analysis["nn_distances"][:5]
    for i, op in enumerate(bottom_5, 1):
        print(f"{i}. {op['operationId']}: {op['nn_distance']:.6f}")
        print(f"   Description: {op['description'][:80]}...")

    print("\n--- k-Nearest Neighbor (kNN) Distance Statistics ---")
    for k_label, stats in analysis["knn_stats"].items():
        print(f"\n{k_label}:")
        print(f"  Mean:   {stats['mean']:.6f}")
        print(f"  Median: {stats['median']:.6f}")
        print(f"  Std:    {stats['std']:.6f}")

    print("\n" + "=" * 80)


def main():
    # Parse arguments
    if len(sys.argv) != 3:
        print("Usage: python calculate_discriminative_power.py <embeddings_json> <output_json>")
        print("\nExample:")
        print("  python calculate_discriminative_power.py analysis/top-level-176/operation-embeddings.json analysis/top-level-176/discriminative-power-analysis.json")
        sys.exit(1)

    embeddings_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    # Check if embeddings file exists
    if not embeddings_path.exists():
        print(f"Error: Embeddings file not found at {embeddings_path}", file=sys.stderr)
        print("Please run embed_operations.py first", file=sys.stderr)
        sys.exit(1)

    # Create output directory if needed
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Load embeddings
    print(f"Loading embeddings from {embeddings_path}...")
    operations = load_embeddings(embeddings_path)
    print(f"Loaded {len(operations)} operations")

    # Convert embeddings to numpy array
    embeddings = np.array([op["embedding"] for op in operations])
    print(f"Embedding shape: {embeddings.shape}")

    # Compute distance matrix (using cosine distance, which is standard for embeddings)
    metric = "cosine"
    distance_matrix = compute_distance_matrix(embeddings, metric=metric)

    # Calculate NN distances
    print("\nCalculating nearest neighbor distances...")
    nn_distances = calculate_nn_distances(distance_matrix)

    # Calculate kNN distances for various k values
    k_values = [3, 5, 10, 20, 50]
    print(f"\nCalculating kNN distances for k={k_values}...")
    knn_results = calculate_knn_distances(distance_matrix, k_values)

    # Analyze results
    print("\nAnalyzing discriminative power...")
    analysis = analyze_discriminative_power(operations, nn_distances, knn_results, metric)

    # Save results
    print(f"\nSaving analysis to {output_path}...")
    with open(output_path, "w") as f:
        json.dump(analysis, f, indent=2)

    # Print summary
    print_summary(analysis)

    print(f"\nFull analysis saved to: {output_path}")


if __name__ == "__main__":
    main()
