# Get water intake totals for the last N days (returns list of (date, total_ml))
def get_last_n_days_totals(n=7):
    data = load_water_log()
    today = datetime.date.today()
    days = [(today - datetime.timedelta(days=i)).isoformat() for i in range(n-1, -1, -1)]
    return [(d, sum(e['amount_ml'] for e in data.get(d, []))) for d in days]
import datetime
import json
import os
import calendar

WATER_LOG_FILE = 'water_intake_log.json'

# Helper to get today's date as string
def today_str():
    return datetime.date.today().isoformat()

# Log water intake (in ml)
def log_water_intake(amount_ml):
    data = load_water_log()
    today = today_str()
    if today not in data:
        data[today] = []
    data[today].append({'amount_ml': amount_ml, 'timestamp': datetime.datetime.now().isoformat()})
    save_water_log(data)

# Get total water intake for today (in ml)
def get_today_total():
    data = load_water_log()
    today = today_str()
    if today in data:
        return sum(entry['amount_ml'] for entry in data[today])
    return 0

# Load water log from file
def load_water_log():
    if not os.path.exists(WATER_LOG_FILE):
        return {}
    with open(WATER_LOG_FILE, 'r') as f:
        return json.load(f)

# Save water log to file
def save_water_log(data):
    with open(WATER_LOG_FILE, 'w') as f:
        json.dump(data, f)

# Get all water intake entries for today
def get_today_entries():
    data = load_water_log()
    today = today_str()
    return data.get(today, [])

# Delete a specific water intake entry by its timestamp
def delete_water_intake_entry(timestamp):
    data = load_water_log()
    today = today_str()
    if today in data:
        original_count = len(data[today])
        data[today] = [entry for entry in data[today] if entry['timestamp'] != timestamp]
        
        if len(data[today]) < original_count:
            save_water_log(data)
            return True
    return False

# Get water intake data for a specific month
def get_monthly_data(year, month):
    data = load_water_log()
    month_data = {}
    num_days = calendar.monthrange(year, month)[1]
    for day in range(1, num_days + 1):
        date_str = f"{year}-{month:02d}-{day:02d}"
        total = sum(entry['amount_ml'] for entry in data.get(date_str, []))
        month_data[date_str] = total
    return month_data

# Edit a specific water intake entry
def edit_water_intake_entry(timestamp, new_amount_ml):
    data = load_water_log()
    today = today_str()
    if today in data:
        for entry in data[today]:
            if entry['timestamp'] == timestamp:
                entry['amount_ml'] = new_amount_ml
                save_water_log(data)
                return True
    return False
