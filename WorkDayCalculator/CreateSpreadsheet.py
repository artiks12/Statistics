import json

with open('WorkDayStats.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

results = {
    'same day':0,
    'within week':0,
    'within 2 weeks':0,
    'within month':0,
    'within 2 months':0,
    'within 3 months':0,
    'within 6 months':0,
    'within year':0,
    'longer':0
}

longest = -1

for month in data.keys():
    for entry in data[month].keys():
        days = int(entry)
        if days > longest: longest = days

        if days == 1: results['same day'] += data[month][entry]
        elif days >= 2 and days <= 5: results['within week'] += data[month][entry]
        elif days >= 6 and days <= 10: results['within 2 weeks'] += data[month][entry]
        elif days >= 11 and days <= 20: results['within month'] += data[month][entry]
        elif days >= 21 and days <= 40: results['within 2 months'] += data[month][entry]
        elif days >= 41 and days <= 60: results['within 3 months'] += data[month][entry]
        elif days >= 61 and days <= 120: results['within 6 months'] += data[month][entry]
        elif days >= 121 and days <= 240: results['within year'] += data[month][entry]
        else: results['longer'] += data[month][entry]

print(results)
print(longest)