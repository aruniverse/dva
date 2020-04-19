import json
with open('analysis/aapl.json', 'r') as f:
	data = json.load(f)

print(data)