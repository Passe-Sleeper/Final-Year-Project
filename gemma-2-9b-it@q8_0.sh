#!/bin/bash

# Set the path to your Python interpreter (if necessary)
# PYTHON_BIN="/usr/bin/python3"  # Or wherever your python executable is
# Use 'which python3' to find it

# Set the model name for LM Studio
MODEL_NAME="gemma-2-9b-it@q8_0"

# Set the output CSV file name
OUTPUT_CSV="MMLU_response_result-seed_982-for_9b-it@q8_0.csv"

# Set the data directory containing the CSV files
DATA_DIR="./data"

# Check if the data directory exists
if [ ! -d "$DATA_DIR" ]; then
  echo "Error: Data directory '$DATA_DIR' not found."
  exit 1
fi

# Check if the Python script exists
if [ ! -f "llm_eval.py" ]; then
  echo "Error: Python script 'llm_eval.py' not found."
  exit 1
fi

# Record the start time
START_TIME=$(date +%s)

# Run the Python script
echo "Running the LLM evaluation script..."
python llm_eval.py --model_name "$MODEL_NAME" --output_csv_file "$OUTPUT_CSV" --data_dir "$DATA_DIR"

# Check the exit code of the Python script
if [ $? -eq 0 ]; then
  echo "LLM evaluation complete."
  echo "Results saved in the 'results' folder as '$OUTPUT_CSV'."
else
  echo "Error: LLM evaluation failed.  Check the output for details."
  exit 1
fi

# Record the end time
END_TIME=$(date +%s)

# Calculate the duration
DURATION=$((END_TIME - START_TIME))

# Print the start time, end time, and duration
echo "Start Time: $(date -d @$START_TIME)"
echo "End Time: $(date -d @$END_TIME)"
echo "Duration: $DURATION seconds"

exit 0
