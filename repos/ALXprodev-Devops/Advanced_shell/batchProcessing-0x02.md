# Task 4: Error Handling and Retry Logic (Enhancing Task 2)

## Objective
Add robust error handling and retry logic for API requests to the batch processing script.

## Instructions
Modify the script from Task 2 (`batchProcessing-0x02`) to handle potential errors (e.g., network issues, invalid Pokémon names). If an API request fails, implement a retry mechanism that attempts the request up to 3 times before logging the error and skipping to the next Pokémon.

## Solution (batchProcessing-0x02 - Enhanced)

The `batchProcessing-0x02` script has been enhanced with a robust error handling and retry mechanism.
- It now includes a `while` loop that attempts to download data for each Pokémon up to a maximum of 3 times.
- The `curl` command uses the `--fail` flag, which causes it to return a non-zero exit code on HTTP errors (like 404 Not Found), making error detection more reliable.
- If a request fails, the script waits for a short delay before retrying.
- If all retry attempts fail for a specific Pokémon, an error message is logged to `error.log`, and the script moves on to the next Pokémon.
- An invalid Pokémon name was added to the list to demonstrate this functionality.

```bash
#!/bin/bash

POKEMON_LIST=("bulbasaur" "ivysaur" "venusaur" "charmander" "charmeleon" "invalidpokemon") # Added an invalid name to test error handling
OUTPUT_DIR="pokemon_data"
ERROR_LOG="error.log"
API_BASE_URL="https://pokeapi.co/api/v2/pokemon/"
DELAY_SECONDS=1
MAX_RETRIES=3
RETRY_DELAY=2

# Create output directory if it doesn't exist
mkdir -p "${OUTPUT_DIR}"

echo "Starting batch data retrieval for Pokémon..."

for pokemon_name in "${POKEMON_LIST[@]}"; do
  API_URL="${API_BASE_URL}${pokemon_name}"
  OUTPUT_FILE="${OUTPUT_DIR}/${pokemon_name}.json"
  attempt=1
  success=false

  echo "Fetching data for ${pokemon_name}..."

  while [ ${attempt} -le ${MAX_RETRIES} ]; do
    # Use curl with --fail to exit with an error code on HTTP failure (like 404)
    if curl -s --fail -o "${OUTPUT_FILE}" "${API_URL}"; then
      if [ -s "${OUTPUT_FILE}" ]; then
        echo "Saved data to ${OUTPUT_FILE} ✅"
        success=true
        break
      else
        echo "Attempt ${attempt}/${MAX_RETRIES}: Failed to save data for ${pokemon_name} (received empty response). Retrying in ${RETRY_DELAY}s..."
        rm -f "${OUTPUT_FILE}" # Clean up empty file
      fi
    else
      echo "Attempt ${attempt}/${MAX_RETRIES}: Failed to fetch data for ${pokemon_name} (HTTP error). Retrying in ${RETRY_DELAY}s..."
    fi

    attempt=$((attempt + 1))
    sleep "${RETRY_DELAY}"
  done

  if [ "${success}" = false ]; then
    echo "All attempts failed for ${pokemon_name}. Logging error and skipping. ❌"
    echo "$(date): Failed to fetch data for ${pokemon_name} from ${API_URL} after ${MAX_RETRIES} attempts." >> "${ERROR_LOG}"
  fi

  sleep "${DELAY_SECONDS}" # Delay between different Pokémon
done

echo "Batch data retrieval complete."
```

## Usage

To run the script:
```bash
chmod +x repos/ALXprodev-Devops/Advanced_shell/batchProcessing-0x02
./repos/ALXprodev-Devops/Advanced_shell/batchProcessing-0x02
```

## Verification

The script will attempt to fetch data for all Pokémon in the list. For an invalid name, it will show retry attempts:
```
Fetching data for invalidpokemon...
Attempt 1/3: Failed to fetch data for invalidpokemon (HTTP error). Retrying in 2s...
Attempt 2/3: Failed to fetch data for invalidpokemon (HTTP error). Retrying in 2s...
Attempt 3/3: Failed to fetch data for invalidpokemon (HTTP error). Retrying in 2s...
All attempts failed for invalidpokemon. Logging error and skipping. ❌
```
After execution, you can check the `error.log` file for the logged error:
```bash
cat error.log
```
The file should contain a message similar to: `Wed Dec 3 22:57:08 EAT 2025: Failed to fetch data for invalidpokemon from https://pokeapi.co/api/v2/pokemon/invalidpokemon after 3 attempts.`

---
**File:** `repos/ALXprodev-Devops/Advanced_shell/batchProcessing-0x02`
**Outcome:** The script is now more robust, capable of handling transient network errors and invalid inputs gracefully by retrying requests and logging persistent failures.