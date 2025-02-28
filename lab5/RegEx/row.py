import re

# Read receipt text from a file
with open("row.txt", "r", encoding="utf-8") as file:
    receipt_text = file.read()

# Regex pattern to extract product details
pattern = r'(\d+)\.\n(.+?)\n([\d,]+)\s+x\s*([\d\s]+,\d+)\n([\d\s]+,\d+)'
matches = re.findall(pattern, receipt_text)

# Save as Markdown
with open("row.md", "w", encoding="utf-8") as file:
    file.write("| Product Name | Quantity | Unit Price | Total Price |\n")
    file.write("|-------------|----------|------------|-------------|\n")
    for match in matches:
        file.write(f"| {match[1].strip()} | {match[3].replace(' ', '').replace(',', '.')} | {match[2]} | {match[4].replace(' ', '').replace(',', '.')} |\n")

print("Data saved to row.md.")  # Исправил название файла в print
