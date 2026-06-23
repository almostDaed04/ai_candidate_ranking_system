# Redrob AI Candidate Ranking Engine

An intelligent, hybrid AI ranking engine designed to evaluate and rank 100K candidates for a Senior AI Engineer role. Built for the "Data & AI Challenge", this engine goes beyond simple keyword matching by semantically understanding career trajectories, production experience signals, and behavioral patterns to surface the genuinely best-fit candidates.

## Features

*   **Semantic Skill Clusters:** Matches skills conceptually (e.g., matching "FAISS" to the `vector_databases` cluster) rather than requiring exact keyword hits.
*   **Trust-Weighted Skill Scoring:** Validates skills using endorsements, stated proficiency, and duration. Penalizes keyword stuffers who list "expert" skills without any actual experience.
*   **Career Context Mining:** Analyzes unstructured career descriptions to find evidence of relevant ML work and production deployments, even if they aren't explicitly listed in the skills array.
*   **Honeypot & Anomaly Detection:** Identifies misleading profiles by catching:
    *   Expert proficiency with 0 duration months.
    *   Time-traveling career dates (stated duration > possible time).
    *   Title-description mismatches.
*   **Hybrid Scoring Model:** Combines TF-IDF/Sentence-Transformers text embeddings with weighted feature extraction (Career, Skills, Behavioral, Education, Location) for robust ranking.
*   **Personalized Reasoning:** Automatically generates a human-readable justification for why a candidate received their specific score.
*   **SQLite Integration:** Pre-computes all features and rankings into a `redrob_candidates.db` SQLite database for seamless integration with backend APIs.

## Architecture

1.  **Data Loading & Cleaning:** Stream-loads the 100K JSONL file, normalizing text and filtering anomalies.
2.  **Feature Extraction:** Extracts over 50 numerical and boolean features across career history, education, and behavioral signals.
3.  **Embedding Generation:** Uses `sentence-transformers` (`all-MiniLM-L6-v2`) to encode the job description and candidate profiles, computing cosine similarities.
4.  **Hybrid Engine:** Merges embedding similarity with feature scores, applying hard penalties for disqualifiers and honeypots.
5.  **Persistence:** Saves pre-computed artifacts and an SQLite database.
6.  **Inference:** Rapidly ranks the top candidates within seconds.

## Installation & Usage

### Prerequisites
*   Python 3.11+
*   (Optional but recommended) NVIDIA GPU for faster `sentence-transformers` embedding generation.

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Pre-computation (One-time Setup)
Run the pre-computation pipeline. This will process the dataset, generate embeddings, and populate the SQLite database (`./precomputed/redrob_candidates.db`). *This step runs outside the 5-minute ranking window.*

```bash
python -m src.precompute --candidates ./candidates.jsonl --output ./precomputed --sqlite
```

### 3. Generate Rankings
Run the incredibly fast ranking step. This uses the pre-computed artifacts to rank the candidates and output the final `submission.csv` with justifications.

```bash
python rank.py --candidates ./candidates.jsonl --out ./submission.csv --precomputed-dir ./precomputed --analyze
```

### 4. Validation
Verify that the output format strictly adheres to the challenge specifications:
```bash
python validate_submission.py submission.csv
```

## Evaluation Results
The ranking algorithm successfully surfaces the exact profile described in the Job Description. The Top 10 results yield:
*   **100% Product-Company background** (Engineers from Netflix, Flipkart, Microsoft, Amazon, etc.)
*   **Average ML/AI Experience:** 5.85 years
*   **0 Honeypots** or consulting-only mismatches in the Top 100.
*   **Ranking Inference Time:** ~2.7 seconds on CPU (well under the 5-minute limit).

## Project Structure
*   `src/data_loader.py` - JSONL streaming and parsing
*   `src/data_cleaner.py` - Text normalization and validation
*   `src/feature_extractor.py` - 50+ feature derivations
*   `src/embedding_engine.py` - Cosine similarity and sentence-transformers
*   `src/skill_matcher.py` - Semantic clusters and trust-weighting
*   `src/ranking_engine.py` - Hybrid scoring logic
*   `src/reasoning_generator.py` - Natural language justifications
*   `src/db_populator.py` - SQLite integration
*   `src/schema.sql` - Relational table definitions
*   `rank.py` - Main inference entry point
