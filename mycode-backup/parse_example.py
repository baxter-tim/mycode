import json

try:
    data = json.loads("JSON")
except json.JSONDecodeError:
    print("Invalid JSON.")
else:
    print(data)
finally:
    print("Parsing complete.")
