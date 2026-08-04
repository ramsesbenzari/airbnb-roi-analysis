import requests, re

r = requests.get("https://insideairbnb.com/get-the-data")
r.encoding = "utf-8"
page = r.text

links = sorted(set(re.findall(r"https://data\.insideairbnb\.com/\S+?/visualisations/listings\.csv", page)))

print(len(links))

f = open("data/city_urls.txt", "w", encoding="utf-8")
f.write("\n".join(links))
f.close()