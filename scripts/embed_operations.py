#!/usr/bin/env python3
"""
Script to embed operationId+description pairs using OpenAI embeddings API.
Saves embeddings to a file for later analysis.
"""

import json
import os
import sys
from pathlib import Path

import numpy as np
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Model to use - text-embedding-3-large is the best embedding model for GPT-4 era
EMBEDDING_MODEL = "text-embedding-3-large"


def load_operations(filepath: str) -> list[dict]:
    """Load operation data from JSON file."""
    with open(filepath, "r") as f:
        return json.load(f)


def create_embedding_text(operation: dict) -> str:
    """Create the text to embed from operationId and description."""
    operation_id = operation["operationId"]
    description = operation["description"]
    return f"{operation_id}: {description}"


def embed_operations(operations: list[dict], batch_size: int = 100) -> list[dict]:
    """
    Embed all operations using OpenAI API.
    Returns list of dicts with operationId, description, text, and embedding.
    """
    results = []

    # Prepare texts
    for op in operations:
        text = create_embedding_text(op)
        results.append({
            "operationId": op["operationId"],
            "description": op["description"],
            "text": text,
            "embedding": None
        })

    # Batch embed
    print(f"Embedding {len(operations)} operations using {EMBEDDING_MODEL}...")

    for i in range(0, len(results), batch_size):
        batch = results[i:i + batch_size]
        texts = [r["text"] for r in batch]

        print(f"Processing batch {i // batch_size + 1}/{(len(results) - 1) // batch_size + 1}...")

        response = client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=texts
        )

        # Store embeddings
        for j, embedding_obj in enumerate(response.data):
            results[i + j]["embedding"] = embedding_obj.embedding

    print("Embedding complete!")
    return results


def save_embeddings(results: list[dict], output_path: str):
    """Save embeddings to JSON file."""
    # Convert numpy arrays to lists for JSON serialization
    serializable_results = []
    for r in results:
        serializable_results.append({
            "operationId": r["operationId"],
            "description": r["description"],
            "text": r["text"],
            "embedding": r["embedding"]  # Already a list from API
        })

    with open(output_path, "w") as f:
        json.dump(serializable_results, f, indent=2)

    print(f"Saved embeddings to {output_path}")


def main():
    # Parse arguments
    if len(sys.argv) != 3:
        print("Usage: python embed_operations.py <input_json> <output_json>")
        print("\nExample:")
        print("  python embed_operations.py data/spec3-top-level-name-description.json analysis/top-level-176/operation-embeddings.json")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    # Check input file exists
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    # Check for API key
    if not os.environ.get("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)

    # Create output directory if needed
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Load operations
    print(f"Loading operations from {input_path}...")
    operations = load_operations(input_path)
    print(f"Loaded {len(operations)} operations")

    # Embed operations
    results = embed_operations(operations)

    # Save results
    save_embeddings(results, output_path)

    # Print summary statistics
    embedding_dim = len(results[0]["embedding"])
    print(f"\nSummary:")
    print(f"  Total operations: {len(results)}")
    print(f"  Embedding model: {EMBEDDING_MODEL}")
    print(f"  Embedding dimension: {embedding_dim}")
    print(f"  Output file: {output_path}")


if __name__ == "__main__":
    main()
