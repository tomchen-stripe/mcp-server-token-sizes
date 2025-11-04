#!/usr/bin/env python3
"""
Quick script to check the actual distance between two operations.
"""

import json
import sys
from pathlib import Path
from scipy.spatial.distance import cosine

def main():
    if len(sys.argv) != 4:
        print("Usage: python check_operation_distance.py <embeddings_json> <op1> <op2>")
        sys.exit(1)

    embeddings_path = Path(sys.argv[1])
    op1_id = sys.argv[2]
    op2_id = sys.argv[3]

    # Load embeddings
    with open(embeddings_path, 'r') as f:
        embeddings_data = json.load(f)

    # Find the two operations
    op1 = None
    op2 = None
    for op in embeddings_data:
        if op['operationId'] == op1_id:
            op1 = op
        if op['operationId'] == op2_id:
            op2 = op

    if not op1:
        print(f"Error: Operation '{op1_id}' not found")
        sys.exit(1)
    if not op2:
        print(f"Error: Operation '{op2_id}' not found")
        sys.exit(1)

    # Calculate distance
    distance = cosine(op1['embedding'], op2['embedding'])

    print(f"\nOperation 1: {op1['operationId']}")
    print(f"  Embedded text: {op1['text']}")
    print(f"\nOperation 2: {op2['operationId']}")
    print(f"  Embedded text: {op2['text']}")
    print(f"\nCosine Distance: {distance:.6f}")

if __name__ == '__main__':
    main()
