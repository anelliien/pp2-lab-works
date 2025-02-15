from datetime import datetime
current = datetime.now()
new = current.replace(microsecond=0)
print(f"Date: {new}")