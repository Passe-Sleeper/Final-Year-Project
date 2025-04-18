# =========================
# IMPORTS
# =========================
import os
import csv
import time
import argparse
import requests
import json
from tqdm import tqdm  # For displaying a progress bar

# =========================
# CONFIGURATION
# =========================
# LM Studio API endpoint (change to your local or remote server address)
LMSTUDIO_URL = "http://143.239.73.233:1234/v1/chat/completions"

# =========================
# FUNCTION: get_llm_response
# =========================
def get_llm_response(prompt, model_name=None):
    """
    Sends a prompt to LM Studio and retrieves the response.

    Args:
        prompt (str): The question + multiple choice options formatted for the model.
        model_name (str): The specific model name to use.

    Returns:
        tuple: (response content, prompt tokens, completion tokens, total tokens)
    """
    headers = {"Content-Type": "application/json"}
    data = {
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 1,  # Expecting only a single letter output (A/B/C/D)
        "stream": False,
    }
    if model_name:
        data["model"] = model_name

    try:
        response = requests.post(LMSTUDIO_URL, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        json_response = response.json()

        if "choices" in json_response and len(json_response["choices"]) > 0:
            content = json_response["choices"][0]["message"]["content"]
            usage = json_response["usage"]
            return content, usage["prompt_tokens"], usage["completion_tokens"], usage["total_tokens"]
        else:
            print("Error: No 'choices' found in the response.")
            return None, None, None, None

    except (requests.exceptions.RequestException, json.JSONDecodeError, Exception) as e:
        print(f"Error communicating with LM Studio: {e}")
        return None, None, None, None

# =========================
# FUNCTION: process_csv
# =========================
def process_csv(csv_file_path, model_name, total_questions, progress_bar):
    """
    Reads a category CSV file, sends prompts to the LLM, and collects performance data.

    Args:
        csv_file_path (str): Path to the input CSV file.
        model_name (str): Name of the model used for inference.
        total_questions (int): Total number of questions for progress tracking.
        progress_bar (tqdm): Progress bar instance.

    Returns:
        list: A list of result rows for each question.
    """
    category = os.path.splitext(os.path.basename(csv_file_path))[0]
    data_rows = []

    try:
        with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header row

            for row in reader:
                if len(row) != 6:
                    print(f"Skipping malformed row: {row}")
                    continue

                question, *options, expected_answer = row
                expected_answer = expected_answer.strip().upper()

                # Prompt formulation
                prompt = (
                    f"Question: {question}\nOptions:\n"
                    f"A. {options[0]}\nB. {options[1]}\nC. {options[2]}\nD. {options[3]}\n"
                    "For the answer write only the letter A, B, C, or D. Do not write anything before or after the letter. Give only a letter response."
                )

                start_time = time.time()
                try:
                    llm_answer, pt, ct, tt = get_llm_response(prompt, model_name)
                    if llm_answer is None:
                        # Inference failed
                        result = [model_name, category, question, expected_answer, "ERROR", -1, -1, -1, -1, -1]
                        data_rows.append(result)
                        continue

                    llm_answer = llm_answer.strip().upper()
                except Exception as e:
                    print(f"Unexpected LLM error: {e}")
                    result = [model_name, category, question, expected_answer, "ERROR", -1, -1, -1, -1, -1]
                    data_rows.append(result)
                    continue

                computation_time = time.time() - start_time

                # Determine selected letter
                llm_letter = next((ch for ch in "ABCD" if ch in llm_answer), "ERROR")

                # Validate correctness
                correct = 1 if llm_letter == expected_answer else 0

                # Save result row
                result = [model_name, category, question, expected_answer, llm_letter, computation_time, correct, pt, ct, tt]
                data_rows.append(result)

                # Update progress
                progress_bar.update(1)

                # Estimate ETA
                completed = [r for r in data_rows if r[5] != -1]
                if completed:
                    avg_time = sum(r[5] for r in completed) / len(completed)
                    eta = avg_time * (total_questions - progress_bar.n)
                    progress_bar.set_postfix({"ETA": f"{eta:.2f}s"})

    except Exception as e:
        print(f"Error processing file {csv_file_path}: {e}")

    return data_rows

# =========================
# FUNCTION: main
# =========================
def main():
    """
    Entry point for processing all CSV files and saving the final evaluation output.
    """
    parser = argparse.ArgumentParser(description="Evaluate LLM on MMLU-style datasets.")
    parser.add_argument("--model_name", required=True, help="Model name used in LM Studio.")
    parser.add_argument("--output_csv_file", required=True, help="Output CSV file name.")
    parser.add_argument("--data_dir", required=True, help="Directory containing input CSVs.")
    args = parser.parse_args()

    csv_folder = args.data_dir
    model_name = args.model_name
    output_file = os.path.join("results", args.output_csv_file)

    # Ensure output directory exists
    os.makedirs("results", exist_ok=True)

    # Prepare CSV header
    header = [
        "llm_model", "category", "question_asked", "expected_answer", "received_answer",
        "computation_time", "correct", "prompt_tokens", "completion_tokens", "total_tokens"
    ]

    all_results = []
    total_questions = 0

    # Count total questions (used for progress bar)
    for fname in os.listdir(csv_folder):
        if fname.endswith(".csv"):
            try:
                with open(os.path.join(csv_folder, fname), 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    next(reader)
                    total_questions += sum(1 for _ in reader)
            except Exception as e:
                print(f"Failed to count questions in {fname}: {e}")

    # Start evaluation loop with progress bar
    with tqdm(total=total_questions, desc="Processing Questions", unit="question") as bar:
        for fname in os.listdir(csv_folder):
            if fname.endswith(".csv"):
                file_path = os.path.join(csv_folder, fname)
                results = process_csv(file_path, model_name, total_questions, bar)
                all_results.extend(results)

    # Save results to CSV
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(all_results)

    print(f"✅ Results written to {output_file}")

# =========================
# SCRIPT ENTRY POINT
# =========================
if __name__ == "__main__":
    main()
