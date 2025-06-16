import os
import random
import uuid

from dotenv import load_dotenv
from pydub import AudioSegment
from telegram import Update
from telegram.ext import ContextTypes, ApplicationBuilder, MessageHandler, filters, ConversationHandler

import whisper
model = whisper.load_model("medium")

message_download_templates = [
    "Я не хочу це слухать, але послухаю...",
    "Візьми і послухай сам, я вже втомивсі..",
    "Я теж не люблю довгі голосові...",
    "Добре, я це послухаю...",
    "0K8g0LLQttC1INGG0LUg0YfRg9CyLiDQkNC70LUg0YbRjNC+0LPQviDRgNCw0LfRgyDRidC+0YHRjCDQvdC1INGC0LDQui4u"
]

message_transcript_templates = [
    "Цейвот, якось отак вийшло",
    "Кажуть отаке",
    "Юно майлз колись сказав",
    "Діло було в 41-му році",
    "Я сам в шоці, але він сказав"
]

load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

async def download_voice_note(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    file_id = update.message.voice.file_id
    file_name = f"{uuid.uuid4()}"
    file = await context.bot.get_file(file_id)

    await file.download_to_drive(file_name)

    return file_name

def transcribe_voice(file_path: str):
    return model.transcribe(file_path).get("text")

def convert_to_wav(file_path: str):
    file_name  = file_path.split(".")[0] + ".wav"
    sound = AudioSegment.from_file(file_path, format="ogg")
    sound.export(file_name, format="wav")

    return file_name

async def process_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_download_reply = random.choice(message_download_templates)
    await update.effective_message.reply_text("🔪 "+ message_download_reply)

    file_name_ogg = await download_voice_note(update, context)
    file_name_wav = convert_to_wav(file_name_ogg)

    wth_did_nigga_say = transcribe_voice(file_name_wav)

    os.remove(file_name_ogg)
    os.remove(file_name_wav)

    message_transcript_reply = random.choice(message_transcript_templates)
    await update.effective_message.reply_text(f'🔮 {message_transcript_reply}:\n'
                                              f'"{wth_did_nigga_say}"')

def main():
    print("Bot started!!!!!!!!")
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.VOICE, process_message))

    app.run_polling()

if __name__ == "__main__":
    main()