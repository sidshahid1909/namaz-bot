from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Namaz time table").worksheet("Sheet1")
rows = sheet.get_all_values()

# Pre-format timings
def get_namaz_timings():
    message = "🕌 Namaz Timings:\n"
    for row in rows[1:]:  # skip header
        if len(row) >= 2:
            message += f"{row[0]}: {row[1]}\n"
    return message

# Flask route to respond to incoming WhatsApp
@app.route("/sms", methods=["POST"])
def sms_reply():
    msg = request.form.get("Body").strip().lower()
    resp = MessagingResponse()

    if "namaz" in msg:
        resp.message(get_namaz_timings())
    else:
        resp.message("Send 'Namaz' to get today's Namaz timings 🕌")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
