import csv, json, os

INPUT_FILE = "mods.csv"
OUTPUT_DIR = "build"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "mods.json")

os.makedirs(OUTPUT_DIR, exist_ok=True)

mods = []
with open(INPUT_FILE, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    # Strip BOM and whitespace from header names
    reader.fieldnames = [name.strip().replace('\ufeff', '') for name in reader.fieldnames]
    for row in reader:
        row = {k.strip(): v.strip() for k, v in row.items()}
        row["current"] = row["current"].lower() == "true"
        mods.append(row)

mods.sort(key=lambda x: x["name"].lower())

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(mods, f, indent=4, ensure_ascii=False)

print(f"✅ Built {len(mods)} mods → {OUTPUT_FILE}")