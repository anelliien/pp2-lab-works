from datetime import timedelta
import datetime
today = datetime.datetime.now()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)

print(f"Yesterday: {yesterday.strftime("%d %b %Y")}")
print(f"Today: {today.strftime("%d %b %Y")}")
print(f"Tomorrow: {tomorrow.strftime("%d %b %Y")}")