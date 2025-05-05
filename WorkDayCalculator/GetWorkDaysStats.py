from datetime import date
from dateutil.relativedelta import relativedelta
import pandas as pd
import holidays
import os
from os import listdir
from os.path import isfile, join
import json

with open("ParceltasDienas.json", 'r', encoding='utf-8') as f:
    PARCELTIE_DATI = json.load(f)

def darba_dienas_no_lidz(start_date: str, end_date: str):
    # Konvertējam datumus
    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)

    # Latvijas svētku dienas
    lv_svetki = holidays.CountryHoliday('LV')

    # Konvertē uz datetime.date kopām
    parceltie_no = {pd.to_datetime(k).date() for k in PARCELTIE_DATI.keys()}
    parceltie_uz = {pd.to_datetime(v).date() for v in PARCELTIE_DATI.values()}

    # Izveidojam datumu sarakstu
    visi_datumi = pd.date_range(start=start, end=end)

    darba_dienas = 0
    for d in visi_datumi:
        d_date = d.date()

        # Pārceltā diena: jāstrādā, pat ja brīvdiena
        if d_date in parceltie_uz:
            darba_dienas += 1
        # Izlaist dienas, no kurām pārcelts
        elif d_date in parceltie_no:
            continue
        # Parasta darba diena (pirmd. - piektd.) un nav svētki
        elif d.weekday() < 5 and d_date not in lv_svetki:
            darba_dienas += 1

    return darba_dienas


if __name__ == '__main__':
    path = 'lvportals/'
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

    result = {}
    start = date(year=2010,month=4,day=1)
    for file in onlyfiles:
        temp = {}
        with open(path+file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for entry in data:
            question = entry['Saturi'][0]['Datums']
            answer = entry['Saturi'][1]['Datums']
            days = darba_dienas_no_lidz(question, answer)

            if days not in temp: temp[days] = 0
            temp[int(days)] += 1
        temp = dict(sorted(temp.items()))
        result[start.strftime('%Y-%m')] = temp
        start += relativedelta(months=1)

    with open('WorkDayStats.json', 'wt', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
        