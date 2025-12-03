# Task 5: Parallel Data Fetching

## Objective
Speed up data retrieval using parallel processing.

## Instructions
Write a script that fetches data for these Pokémon [Bulbasaur, Ivysaur, Venusaur, Charmander, Charmeleon] in parallel by leveraging background processes and process management tools. Ensure that the script handles background processes properly and waits for all processes to complete before moving to the next step.

## Solution (batchProcessing-0x04)

The script `batchProcessing-0x04` significantly speeds up the data retrieval process by fetching data for multiple Pokémon in parallel.
- It defines a function, `fetch_pokemon`, to handle the `curl` request for a single Pokémon.
- It iterates through a list of Pokémon and launches a `fetch_pokemon` process for each one in the background using the `&` operator.
- The Process ID (PID) of each background job is stored in an array.
- After all jobs are started, the script uses a loop and the `wait` command to pause execution until all the background processes have completed.
- This parallel approach is much more efficient than fetching data sequentially, especially for a large number of requests.

```bash
#!/bin/bash

POKEMON_LIST=("bulbasaur" "ivysaur" "venusaur" "charmander" "charmeleon")
OUTPUT_DIR="pokemon_data_parallel"
API_BASE_URL="https://pokeapi.co/api/v2/pokemon/"

# Create output directory if it doesn't exist
mkdir -p "${OUTPUT_DIR}"

# Function to fetch data for a single Pokémon
fetch_pokemon() {
  local pokemon_name=$1
  local api_url="${API_BASE_URL}${pokemon_name}"
  local output_file="${OUTPUT_DIR}/${pokemon_name}.json"

  echo "Starting fetch for ${pokemon_name}..."
  if curl -s --fail -o "${output_file}" "${api_url}"; then
    echo "Finished fetch for ${pokemon_name} ✅"
    return 0
  else
    echo "Failed to fetch data for ${pokemon_name} ❌"
    return 1
  fi
}

pids=() # Array to store background process IDs

# Start all fetch processes in the background
for pokemon in "${POKEMON_LIST[@]}"; do
  fetch_pokemon "${pokemon}" &
  pids+=($!) # Save the PID of the background process
done

echo "All Pokémon fetch jobs started in the background."
echo "Waiting for all jobs to complete..."

# Wait for all background processes to complete
for pid in "${pids[@]}"; do
  wait "${pid}"
  if [ $? -ne 0 ]; then
    echo "A fetch job failed. See logs above for details."
  fi
done

echo "All Pokémon data has been fetched."
echo "You can find the data in the '${OUTPUT_DIR}' directory."
```

## Usage

To run the script:
```bash
chmod +x repos/ALXprodev-Devops/Advanced_shell/batchProcessing-0x04
./repos/ALXprodev-Devops/Advanced_shell/batchProcessing-0x04
```
This will create a `pokemon_data_parallel` directory and populate it with the fetched data.

## Verification

The output will show the jobs starting in the background and finishing in a non-sequential order, demonstrating parallel execution.
```
Starting fetch for bulbasaur...
Starting fetch for ivysaur...
...
All Pokémon fetch jobs started in the background.
Waiting for all jobs to complete...
Finished fetch for charmeleon ✅
...
All Pokémon data has been fetched.
```
You can then verify the created files:
```bash
ls -l pokemon_data_parallel/
```
---
**File:** `repos/ALXprodev-Devops/Advanced_shell/batchProcessing-0x04`
**Outcome:** The script successfully demonstrates how to use background processes (`&`) and `wait` to perform tasks in parallel, significantly improving the efficiency of the data fetching process.
