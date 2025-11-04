# Discriminative Power Analysis for Stripe API OperationIds

This directory contains scripts to analyze the discriminative power of Stripe API `operationId` names and descriptions using embeddings. The goal is to measure how easily LLMs can distinguish between different API endpoints when selecting the right one for a user's request.

## Overview

The analysis consists of several steps:

1. **Embedding**: Generate embeddings for each `operationId + description` using OpenAI's `text-embedding-3-large` model
2. **Distance Calculation**: Compute nearest neighbor (NN) and k-nearest neighbor (kNN) distances
3. **Export to CSV**: Export nearest neighbor distances to CSV for analysis
4. **Cluster Analysis**: Find semantic clusters of operations that could cause LLM confusion

## Setup

### 1. Install Dependencies

```bash
cd scripts
pip install -r requirements.txt
```

### 2. Set OpenAI API Key

```bash
export OPENAI_API_KEY="your-api-key-here"
```

## Usage

### Quick Start - Run Everything

To run the complete pipeline for both datasets:

```bash
python run_pipeline.py
```

This will automatically:
1. Generate embeddings for both datasets (176 and 572 operations)
2. Calculate discriminative power metrics
3. Export nearest neighbor distances to CSV
4. Find and export confusion clusters

### Nearest Neighbor (NN) Distance

The **NN distance** measures how far each operation is from its closest neighbor in embedding space.

- **High NN distance** → Operation is distinctive and easy to discriminate
- **Low NN distance** → Operation is similar to others and may be confused

### k-Nearest Neighbor (kNN) Average Distance

The **kNN average distance** measures the average distance to the k nearest neighbors.

- Higher k values show how isolated an operation is from a larger neighborhood
- Helps identify operations that might be confused with multiple similar operations

### Distance Metric

We use **cosine distance** (1 - cosine similarity), which is standard for comparing text embeddings:
- 0 = identical embeddings
- 1 = orthogonal embeddings
- 2 = opposite embeddings

## Interpreting Results

### Confusion Clusters (Critical)

**HIGH RISK clusters** indicate real confusion potential:
- Multiple operations with the **same HTTP method** and close semantic meaning
- Example: `DeleteAccountsAccountPeoplePerson` vs `DeleteAccountsAccountPersonsPerson` (distance: 0.009)
- User prompt "delete the person" cannot disambiguate between these

**LOW RISK clusters** are less problematic:
- Operations with **different HTTP methods** (GET vs POST)
- Example: `GetBalanceSettings` vs `PostBalanceSettings`
- User prompt "get my balance settings" or "update my balance settings" provides clear intent

### Operations with High NN Distance

These operations are distinctive and unlikely to be confused:
- Unique functionality
- Clear, specific descriptions
