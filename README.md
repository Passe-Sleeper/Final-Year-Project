# Democratizing LLMs: Evaluating Language Model Deployment on Consumer Devices
This repository contains the code and resources used to evaluate the feasibility of deploying quantized Large Language Models (LLMs) on consumer-grade devices such as laptops and smartphones. The project investigates whether these models can be run locally, and compares their performance across hardware and optimization methods including prompt engineering and quantization.

🚀 **Project Overview**
The central goal of this project is to explore whether large-scale language models—like Gemma, Llama, and Qwen—can be effectively used without relying on cloud-based infrastructure. To do this, the project evaluates model accuracy, runtime performance, and memory usage across multiple devices, quantization levels, and categories from the MMLU dataset.

Key components of the project include:

- Model Benchmarking
- Prompt Engineering
- Quantization
- Seed Fixing for Reproducibility
- Performance & Category-Wise Accuracy Analysis

🧰 **Repository Structure**
.
├── llm_eval.py                 # Main evaluation script for querying LLM via LM Studio API
├── gemma-2-9b-it@q8_0.sh       # Bash script to automate the evaluation for a specific model
├── data                        # Folder containing input dataset files (one CSV per category)
├── data/college_physics.csv    # Example input file from the MMLU dataset (per-category format)
├── results/                    # Output directory where evaluation results will be saved
├── README.md                   # You're here!

📦 **Requirements**
- Python 3.11+
- LM Studio (running a supported LLM with a local API server, default port: 1234)
- requests
- tqdm

Install Python dependencies:
`pip install requests tqdm`

🧪 **How to Run**
1. Start LM Studio and load the desired model (ensure API mode is active).
2. Place your MMLU-style dataset files in a folder (e.g., `./data`).
3. Run the evaluation using the bash script provided:
`bash gemma-2-9b-it@q8_0.sh`
Or directly using Python:
`python llm_eval.py --model_name "gemma-2-9b-it@q8_0" \
                   --output_csv_file "results/output.csv" \
                   --data_dir "./data/"`

📝 **Input Format**
Each category file (e.g., `college_physics.csv`) must be a CSV with 6 columns:
question,option_a,option_b,option_c,option_d,correct_option
Example:
`What is Newton's second law?,Force equals mass,Energy equals mass,Power equals energy,Force equals time,A`

🧮 **Output Format**
Each query generates one row in the output CSV:
`llm_model,category,question_asked,expected_answer,received_answer,computation_time,correct,prompt_tokens,completion_tokens,total_tokens`
Example:
`gemma-2-9b-it@q8_0,college_physics,What is Newton's second law?,A,A,0.154373,1,50,1,51`

🔁 **Reproducibility**
The model is queried using fixed random seeds during testing to ensure reproducibility and evaluate consistency across runs.

📊 **Results**
Results are saved in the results/ directory and can be used for further analysis:
- Accuracy by model and category
- Response time per question
- Token usage breakdown

📚 **Dataset**
The project uses the MMLU Benchmark Dataset[https://github.com/hendrycks/test], covering 57 subject areas across humanities, science, engineering, and more.

⚖️ **License**
This project is for academic, research, and educational purposes only.

🙌 **Acknowledgements**
- HuggingFace for open-source LLM repositories.
- LM Studio for providing a user-friendly local model inference platform.
- Hendrycks et al. for the MMLU benchmark dataset.

