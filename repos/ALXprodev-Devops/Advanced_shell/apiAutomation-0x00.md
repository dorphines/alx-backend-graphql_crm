# Task 0: API Request Automation

## Objective
Automate the process of making API requests to the Pokémon API and saving the results to a file.

## Instructions
Write a shell script that makes a request to the Pokémon API and retrieves data for a specific Pokémon (Pikachu). It should save the response to `data.json`. If the request fails, it should log the error to `errors.txt`.

## Solution (apiAutomation-0x00)

The script `apiAutomation-0x00` fetches data for "Pikachu" from the PokeAPI.
- If the API request is successful, the JSON response is saved to `data.json`.
- If the API request fails, an error message is appended to `errors.txt`.

```bash
#!/bin/bash

POKEMON_NAME="pikachu"
OUTPUT_FILE="data.json"
ERROR_FILE="errors.txt"
API_URL="https://pokeapi.co/api/v2/pokemon/${POKEMON_NAME}"

echo "Fetching data for ${POKEMON_NAME}..."

# Make the API request and save the output
if curl -s -o "${OUTPUT_FILE}" "${API_URL}"; then
  echo "Successfully fetched data for ${POKEMON_NAME} and saved to ${OUTPUT_FILE}"
else
  ERROR_MESSAGE="Error fetching data for ${POKEMON_NAME} from ${API_URL} at $(date)"
  echo "${ERROR_MESSAGE}" >> "${ERROR_FILE}"
  echo "Failed to fetch data for ${POKEMON_NAME}. Error logged to ${ERROR_FILE}"
fi
```

## Usage

To run the script:
```bash
chmod +x repos/ALXprodev-Devops/Advanced_shell/apiAutomation-0x00
./repos/ALXprodev-Devops/Advanced_shell/apiAutomation-0x00
```

After execution, `data.json` will contain the API response for Pikachu, and `errors.txt` will be created only if an error occurred during the `curl` request.

## Verification

To verify the content of `data.json`:
```bash
jq . < data.json | head -n 50
```
(Requires `jq` to be installed for pretty printing and truncation)

To check for errors (this file should not exist if the script ran successfully):
```bash
cat errors.txt
```

---
**File:** `repos/ALXprodev-Devops/Advanced_shell/apiAutomation-0x00`
**Outcome:** The script successfully fetched data for Pikachu and saved it to `data.json`. No `errors.txt` was created, indicating a successful operation.
