import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Setup access
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Open the correct sheet
sheet = client.open("Namaz time table").worksheet("Sheet1")

# Fetch all values
rows = sheet.get_all_values()

# Print Namaz timings
print("🕌 Namaz Timings:")
for row in rows[1:]:  # skip header
    if len(row) >= 2:
        print(f"{row[0]}: {row[1]}")
