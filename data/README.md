# 📁 `data/` — Sample MMLU CSV Files

This folder contains a **small subset** of the full MMLU dataset used in the evaluation phase of this project. These files are included for demonstration and testing purposes only.

## 📄 File Format

Each CSV file corresponds to a specific **subject category** (e.g., `college_physics.csv`) and follows this column structure:

Question,Option A,Option B,Option C,Option D,Correct Answer (A/B/C/D)

These files serve as input for evaluating LLM performance using the script [`llm_eval.py`](../llm_eval.py).

## ✅ Example Use Cases

- Testing and debugging the LLM evaluation script
- Understanding the expected input structure
- Running lightweight benchmarks on specific topics

## 📦 Full Dataset

This is not the complete MMLU dataset. The full dataset includes over 15,000 examples across 57 categories. To use the complete dataset, please refer to the official [MMLU GitHub repository](https://github.com/hendrycks/test).

## 🔗 Related Files

- [`llm_eval.py`](../llm_eval.py) — Python script to evaluate LLMs using these CSVs
- [`gemma-2-9b-it@q8_0.sh`](../gemma-2-9b-it@q8_0.sh) — Shell script for batch evaluation

---

Feel free to expand this dataset locally for full-scale experimentation.
