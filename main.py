import os
import logging
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Logging
logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")

# Google Sheets Auth
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]

import json
from oauth2client.service_account import ServiceAccountCredentials

google_creds = json.loads(os.getenv("GOOGLE_CREDENTIALS"))

creds = ServiceAccountCredentials.from_json_keyfile_dict(
    google_creds, scope
)
)
client = gspread.authorize(creds)
sheet = client.open_by_key(SPREADSHEET_ID).sheet1


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Sinyo Ops CRM Active 🚀")


async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = " ".join(context.args)
    row = data.split("|")

    if len(row) < 12:
        await update.message.reply_text("Format salah.")
        return

    sheet.append_row(row)
    await update.message.reply_text("Data berhasil ditambahkan ✅")


async def list_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    records = sheet.get_all_values()

    if len(records) <= 1:
        await update.message.reply_text("Belum ada data.")
        return

    response = ""
    for row in records[1:]:
        response += f"{row[0]} - {row[1]} - {row[5]}\n"

    await update.message.reply_text(response)


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("add", add))
app.add_handler(CommandHandler("list", list_data))

app.run_polling()


