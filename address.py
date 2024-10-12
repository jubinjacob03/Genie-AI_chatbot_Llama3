import json
from datetime import datetime, timedelta
import requests


IP_DATA_FILE = "IP_address.json"


def load_ip_data():
    try:
        with open(IP_DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_ip_data(data):
    with open(IP_DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


def get_current_ip():
    try:
        response = requests.get("https://api.ipify.org?format=json")
        return response.json().get("ip")
    except requests.RequestException:
        return None


def is_allowed_to_prompt(ip):
    data = load_ip_data()
    current_time = datetime.now()

    if ip in data:
        ip_info = data[ip]
        prompt_count = ip_info["total_prompts"]
        last_prompt_time = datetime.fromisoformat(ip_info["last_prompt"])

        if current_time - last_prompt_time > timedelta(days=20):
            data[ip]["total_prompts"] = 0
            data[ip]["last_prompt"] = current_time.isoformat()
            save_ip_data(data)
            return True

        elif prompt_count < 7:
            data[ip]["total_prompts"] += 1
            data[ip]["last_prompt"] = current_time.isoformat()
            save_ip_data(data)
            return True
        else:
            return False
    else:

        data[ip] = {"total_prompts": 1,
                    "last_prompt": current_time.isoformat()}
        save_ip_data(data)
        return True
