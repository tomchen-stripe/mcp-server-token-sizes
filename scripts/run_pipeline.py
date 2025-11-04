#!/usr/bin/env python3
"""
Run the complete discriminative power analysis pipeline for both datasets.
"""

import subprocess
import sys
from pathlib import Path


def run_command(description, command):
    """Run a command and handle errors."""
    print("\n" + "=" * 80)
    print(f"STEP: {description}")
    print("=" * 80)
    print(f"Running: {' '.join(command)}\n")

    try:
        result = subprocess.run(command, check=True)
        print(f"\n✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n✗ {description} failed with error code {e.returncode}", file=sys.stderr)
        return False


def main():
    project_root = Path(__file__).parent.parent
    scripts_dir = project_root / "scripts"

    print("=" * 80)
    print("DISCRIMINATIVE POWER ANALYSIS PIPELINE")
    print("=" * 80)
    print("\nThis will process both datasets:")
    print("  1. Top-Level (176 operations)")
    print("  2. All Operations (572 operations)")
    print()

    # Dataset configurations
    datasets = [
        {
            'name': 'Top-Level (176 operations)',
            'input': project_root / 'data/spec3-top-level-name-description.json',
            'output_dir': project_root / 'analysis/top-level-176'
        },
        {
            'name': 'All Operations (572 operations)',
            'input': project_root / 'data/spec3-all-name-description.json',
            'output_dir': project_root / 'analysis/all-572'
        }
    ]

    # Process each dataset
    for dataset in datasets:
        print(f"\n{'='*80}")
        print(f"Processing: {dataset['name']}")
        print(f"{'='*80}")

        embeddings_file = dataset['output_dir'] / 'operation-embeddings.json'
        analysis_file = dataset['output_dir'] / 'discriminative-power-analysis.json'

        # Step 1: Generate embeddings
        if not run_command(
            f"Generate embeddings for {dataset['name']}",
            [sys.executable, str(scripts_dir / 'embed_operations.py'),
             str(dataset['input']), str(embeddings_file)]
        ):
            return False

        # Step 2: Calculate discriminative power
        if not run_command(
            f"Calculate discriminative power for {dataset['name']}",
            [sys.executable, str(scripts_dir / 'calculate_discriminative_power.py'),
             str(embeddings_file), str(analysis_file)]
        ):
            return False

    # Step 3: Export to CSV (processes both datasets)
    if not run_command(
        "Export nearest neighbor distances to CSV",
        [sys.executable, str(scripts_dir / 'export_nn_distances_csv.py')]
    ):
        return False

    # Step 4: Find confusion clusters (processes both datasets)
    if not run_command(
        "Find confusion clusters",
        [sys.executable, str(scripts_dir / 'find_confusion_clusters.py')]
    ):
        return False

    # Success summary
    print("\n" + "=" * 80)
    print("PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 80)
    print("\nResults saved to:")
    for dataset in datasets:
        print(f"\n{dataset['name']}:")
        print(f"  - Embeddings: {dataset['output_dir'] / 'operation-embeddings.json'}")
        print(f"  - Analysis: {dataset['output_dir'] / 'discriminative-power-analysis.json'}")
        print(f"  - NN Distances CSV: {dataset['output_dir'] / 'nn_distances.csv'}")
        print(f"  - Confusion Clusters CSV: {dataset['output_dir'] / 'confusion_clusters.csv'}")

    return True


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
