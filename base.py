import json
import os

def load_data():
    if os.path.exists("strom_data.json"):
        try:
            with open("strom_data.json", "r", encoding="utf-8") as file:
                data = json.load(file)
                if isinstance(data, dict):
                    return data
        except json.JSONDecodeError:
            print("Error decoding JSON, returning default structure.")
    return {"contracts": [], "tarife": [], "ablesungen": []}

def save_data(data):
    try:
        with open("strom_data.json", "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print("Data saved successfully to strom_data.json")
    except Exception as e:
        print(f"Error saving data: {e}")