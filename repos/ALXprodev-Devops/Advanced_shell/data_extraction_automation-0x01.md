# Task 1: Extract Pokémon Data

## Objective
Use advanced text manipulation tools (jq, awk, sed) to extract specific data from the API response.

## Instructions
Write a script that extracts the Pokémon’s name, height, weight, and type from the JSON file created in Task 0.

Format the output in a human-readable way: “Pikachu is of type Electric, weighs 6kg, and is 0.4m tall.”

You should only use these commands: `jq`, `awk`, `sed`.

## Solution (data_extraction_automation-0x01)

The script `data_extraction_automation-0x01` reads the `data.json` file (generated in Task 0) and uses `jq` to extract and format the required information.
- The Pokémon's name, height, weight, and the first type are extracted.
- Height and weight, which are originally in decimetres and hectograms from the PokeAPI, are converted to meters and kilograms respectively by dividing by 10.
- The `jq` program also handles capitalization for the Pokémon name and type to match the desired output format.

```bash
#!/bin/bash

DATA_FILE="data.json"

# Check if data.json exists
if [ ! -f "${DATA_FILE}" ]; then
  echo "Error: ${DATA_FILE} not found. Please run Task 0 first."
  exit 1
fi

# Extract name, height, weight, and first type using jq
# Height and weight are in decimetres and hectograms, convert to meters and kilograms
POKEMON_INFO=$(cat "${DATA_FILE}" | jq -r '
  .name as $name |
  (.height / 10) as $height_m |
  (.weight / 10) as $weight_kg |
  .types[0].type.name as $type_name |
  (
    ($name | ascii_upcase | .[0:1]) +
    ($name | ascii_downcase | .[1:]) +
    " is of type " +
    (($type_name | ascii_upcase | .[0:1]) + ($type_name | ascii_downcase | .[1:])) +
    ", weighs \($weight_kg)kg, and is \($height_m)m tall."
  )
')

echo "${POKEMON_INFO}"
```

## Usage

To run the script:
```bash
chmod +x repos/ALXprodev-Devops/Advanced_shell/data_extraction_automation-0x01
./repos/ALXprodev-Devops/Advanced_shell/data_extraction_automation-0x01
```

This script requires `jq` to be installed on your system. If not installed, you can install it using:
```bash
sudo apt-get update && sudo apt-get install -y jq
```

## Verification

The script should output the following:
```
Pikachu is of type Electric, weighs 6kg, and is 0.4m tall.
```

---
**File:** `repos/ALXprodev-Devops/Advanced_shell/data_extraction_automation-0x01`
**Outcome:** The script successfully extracted the required data from `data.json` and formatted it as specified.
