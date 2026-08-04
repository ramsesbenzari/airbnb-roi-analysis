import pandas as pd
import glob
import os

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)

rows = []
problems = []

for path in glob.glob("data/*.csv"):
    city = os.path.basename(path).replace(".csv", "")

    if city == "city_index":
        continue

    try:
        df = pd.read_csv(path)
    except Exception:
        problems.append(city + " (unreadable)")
        continue

    if "room_type" not in df.columns:
        problems.append(city + " (wrong columns)")
        continue

    entire = df[df["room_type"] == "Entire home/apt"]
    active = entire[entire["number_of_reviews_ltm"] > 0]

    rows.append({
        "city": city,
        "total_listings": len(df),
        "entire_homes": len(entire),
        "active_entire_homes": len(active),
    })

index = pd.DataFrame(rows).sort_values("active_entire_homes", ascending=False)
index.to_csv("data/city_index.csv", index=False)

print(len(index), "cities loaded")
print(len(problems), "problem files:", problems)
print()
print(index.head(40))