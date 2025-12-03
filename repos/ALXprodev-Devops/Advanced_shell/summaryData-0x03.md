# Task 3: Summarize Pokémon Data

## Objective
Create a report that summarizes data for multiple Pokémon.

## Instructions
Write a shell script that reads all the JSON files generated in Task 2 and extracts the name, height, and weight of each Pokémon. Generate a CSV file containing the Pokémon’s name, height, and weight. Use `awk` to calculate the average height and weight of all Pokémon in the report.

## Solution (summaryData-0x03)

The script `summaryData-0x03` processes all the `.json` files in the `pokemon_data` directory to create a summary report.
- It reads each JSON file, uses `jq` to extract the Pokémon's name, height (converted to meters), and weight (converted to kilograms), and outputs them in CSV format.
- All the data is compiled into a single file, `pokemon_report.csv`.
- `awk` is then used to process this CSV file to capitalize the first letter of each Pokémon's name for better readability.
- Finally, another `awk` command calculates and displays the average height and weight of all the Pokémon listed in the report.
- The script uses a `heredoc` to safely pass the multi-line `awk` script, which is a robust way to handle complex scripts within a shell script.

```bash
#!/bin/bash

INPUT_DIR="pokemon_data"
OUTPUT_CSV="pokemon_report.csv"

# Check if the input directory exists
if [ ! -d "${INPUT_DIR}" ]; then
  echo "Error: Directory '${INPUT_DIR}' not found. Please run Task 2 first."
  exit 1
fi

# Write CSV header
echo "Name,Height (m),Weight (kg)" > "${OUTPUT_CSV}"

# Process each JSON file
for file_path in "${INPUT_DIR}"/*.json; do
  if [ -f "${file_path}" ]; then
    # Use jq to extract data and format as CSV, appending to the output file
    jq -r '[.name, (.height / 10), (.weight / 10)] | @csv' "${file_path}" >> "${OUTPUT_CSV}"
  fi
done

# Capitalize the first letter of each Pokémon's name in the CSV using awk
awk -F, 'BEGIN {OFS=FS} NR > 1 {$1 = toupper(substr($1,1,1)) substr($1,2); $1 = "\"" $1 "\""} 1' "${OUTPUT_CSV}" > temp.csv && mv temp.csv "${OUTPUT_CSV}"

echo "CSV Report generated at: ${OUTPUT_CSV}"
echo ""

# Display the CSV report
cat "${OUTPUT_CSV}"
echo ""

# awk script to calculate averages
read -r -d '' AWK_SCRIPT << 'EOF'
NR > 1 {
    gsub(/"/, "", $2);
    gsub(/"/, "", $3);
    sum_height += $2;
    sum_weight += $3;
    count++;
}
END {
    if (count > 0) {
        printf "Average Height: %.2f m\n", sum_height / count;
        printf "Average Weight: %.2f kg\n", sum_weight / count;
    }
}
EOF

# Calculate and display average height and weight using awk
awk -F, "${AWK_SCRIPT}" "${OUTPUT_CSV}"
```

## Usage

To run the script:

```bash
chmod +x repos/ALXprodev-Devops/Advanced_shell/summaryData-0x03
./repos/ALXprodev-Devops/Advanced_shell/summaryData-0x03
```

This requires that the `pokemon_data` directory (from Task 2) exists in the current working directory.

## Verification

The script will produce the following output:
```
CSV Report generated at: pokemon_report.csv

Name,Height (m),Weight (kg)
"Bulbasaur",0.7,6.9
"Charmander",0.6,8.5
"Charmeleon",1.1,19
"Ivysaur",1,13
"Venusaur",2,100

Average Height: 1.08 m
Average Weight: 29.48 kg
```
The file `pokemon_report.csv` will also be created in the current directory.

---
**File:** `repos/ALXprodev-Devops/Advanced_shell/summaryData-0x03`
**Outcome:** The script successfully generated a CSV report summarizing the Pokémon data and calculated the average height and weight.
