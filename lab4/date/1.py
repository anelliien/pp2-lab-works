from datetime import timedelta
import datetime
current = datetime.datetime.now()
before = current - timedelta(days=5)

print(f"Date after subtracting 5 days: {before.strftime("%d %b %Y")}")