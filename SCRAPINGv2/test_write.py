import csv
import json


headers = ["id", "age", "name", "gender", "city", "country"]
rows = []

for i in range(10):
  rows.append({
    "id": i,
    "age": i*2,
    "name": "test"
  })

with open("example.csv", 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()
    for row in rows:
        writer.writerow(row)

