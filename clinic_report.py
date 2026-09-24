#!/usr/bin/env python3
"""Summarize one week of clinic encounters and save the two report files."""

from pathlib import Path

from vitals_tools import (
    count_patients,
    mean_systolic,
    patients_at_or_above,
    systolic_readings,
)


DATA_PATH = Path("data") / "clinic_encounters.csv"
OUTPUT_DIR = Path("output")


def read_encounters(data_path):
    """TODO: describe what one usable encounter looks like.

    Give back two values: the list of usable encounters, and how many data
    rows you skipped. `main()` unpacks them the way the lecture unpacks a
    tuple, with two names on the left of the `=`.
    """
    # TODO: read the rows and skip the header line.
    # TODO: keep a row only when it has three fields, int() can read the
    #       systolic field, and the reading is plausible.
    # TODO: count every other data row as skipped, the blank line included,
    #       and print one line per skipped row so you can see what dropped out.
    # TODO: end with `return encounters, skipped`.

    encounters = []
    skipped = 0
    with open(DATA_PATH, 'r', encoding='utf-8') as file:
        lines = file.read().split("\n")

    header = lines[0]
    rows = lines[1:] 

    for row in rows:
        if not row.strip():
            print("Skipping a blank row.")
            skipped += 1
            continue

        
        fields = row.split(',')

        if len(fields) != 3:
            print(f"Skipped. Expected 3 fields, got {len(fields)} -> '{row}'")
            skipped += 1
            continue

        third_field = fields[2].strip()
        try:
            systolic = int(third_field)
        except ValueError:
            print(f"Skipped. Third field '{third_field}' is not a valid integer.")
            skipped += 1
            continue

        if not (60 <= systolic <= 250):
            print(f"Skipped. Recording error (BP {systolic} mmHg out of range 60-250).")
            skipped += 1
            continue

        encounter = [fields[0].strip(), fields[1].strip(), systolic]
        encounters.append(encounter)

    
    return encounters, skipped


def main():
    """TODO: describe the two artifacts this writes."""
    encounters, skipped = read_encounters(DATA_PATH)

    # TODO: build the six report lines and write them to output/vitals_report.txt.
    # TODO: read the file back and print it, so you can see what was saved.
    # TODO: choose your follow-up cutoff, then write output/followup_list.txt
    #       with the Cutoff line, the Reason line, and one patient ID per line.

    encounter_count = len(encounters)
    skipped_count = skipped
    num_unique_patients = count_patients(encounters)
    sys_readings = systolic_readings(encounters)
    sys_mean = mean_systolic(sys_readings)
    sys_max = max(sys_readings)
    sys_min = min(sys_readings)

    lines = [f"Usable encounters: {encounter_count}", 
             f"Skipped rows: {skipped_count}",
             f"Patients seen: {num_unique_patients}",
             f"Mean systolic: {sys_mean:.1f} mmHg",
             f"Highest systolic: {sys_max} mmHg",
             f"Lowest systolic: {sys_min} mmHg"]

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_DIR / "vitals_report.txt", "w", encoding='utf-8') as f:
        f.write("\n".join(lines) + "\n")

    with open(OUTPUT_DIR / "vitals_report.txt", "r", encoding='utf-8') as f:
        print(f.read())

    follow_up_cutoff = 130
    follow_up_patients = patients_at_or_above(encounters, follow_up_cutoff)

    with open(OUTPUT_DIR / "followup_list.txt", "w", encoding='utf-8') as f:
        f.write(f"Cutoff: {follow_up_cutoff} mmHg\n")
        f.write(f"Reason: 130 mmHg is the general lower bound for Stage 1 Hypertension\n")
        for id in follow_up_patients:
            f.write(f"{id}\n")





if __name__ == "__main__":
    main()
