import re

with open("row.txt", "r", encoding="utf-8") as file:
    receipt_text = file.read()

pattern = r'(\d+)\.\n(.+?)\n([\d,]+)\s+x\s*([\d\s]+,\d+)\n([\d\s]+,\d+)'
matches = re.findall(pattern, receipt_text)

with open("row.md", "w", encoding="utf-8") as file:
    file.write("| Product Name | Unit Price | Quantity | Total Price |\n")
    file.write("|-------------|----------|------------|-------------|\n")
    for match in matches:
        file.write(f"| {match[1].strip()} | {match[3].replace(' ', '').replace(',', '.')} | {match[2]} | {match[4].replace(' ', '').replace(',', '.')} |\n")

print("Data saved to row.md.") 