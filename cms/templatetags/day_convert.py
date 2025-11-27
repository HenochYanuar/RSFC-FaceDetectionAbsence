from datetime import datetime
from django import template
import calendar

register = template.Library()

hari_mapping = {
    "Monday": "Senin",
    "Tuesday": "Selasa",
    "Wednesday": "Rabu",
    "Thursday": "Kamis",
    "Friday": "Jumat",
    "Saturday": "Sabtu",
    "Sunday": "Minggu",
}

@register.filter
def hari_id(value):
    # 1. Jika value nama hari (string Inggris)
    if isinstance(value, str) and value in hari_mapping:
        return hari_mapping[value]

    # 2. Jika value adalah object date/datetime
    if hasattr(value, "weekday"):
        eng_name = calendar.day_name[value.weekday()]
        return hari_mapping.get(eng_name, eng_name)

    # 3. Jika string tanggal "YYYY-mm-dd"
    try:
        date_obj = datetime.strptime(value, "%Y-%m-%d").date()
        eng_name = calendar.day_name[date_obj.weekday()]
        return hari_mapping.get(eng_name, eng_name)
    except:
        return value
