import requests
import os
import unicodedata
from urllib.parse import quote

fails = []

for line in open("data/city_urls.txt", encoding="utf-8"):
    url = line.strip()

    city = url.split("/")[-4]
    city = unicodedata.normalize("NFKD", city)
    city = city.encode("ascii", "ignore").decode("ascii")

    name = "data/" + city + ".csv"

    if os.path.exists(name):
        continue

    safe_url = quote(url, safe=":/")
    r = requests.get(safe_url)

    if r.status_code == 200:
        open(name, "wb").write(r.content)
        print("ok  ", city, round(len(r.content) / 1000000, 1), "MB")
    else:
        fails.append(city + " (" + str(r.status_code) + ")")
        print("FAIL", city, r.status_code)

print()
print(len(fails), "failed:", fails)