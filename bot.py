import logging
import yaml
import pandas as pd
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackContext

# Tokenni config.yaml dan yuklash
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)
TOKEN = config["BOT_TOKEN"]

# Logger sozlamalari
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# Bosqichlar
NAME, PHONE, ADDRESS, QUESTION = range(4)

# Foydalanuvchi ma'lumotlarini saqlash
user_data = []

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Salom! Ismingizni kiriting:")
    return NAME

async def get_name(update: Update, context: CallbackContext):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("Telefon raqamingizni kiriting:")
    return PHONE

async def get_phone(update: Update, context: CallbackContext):
    context.user_data["phone"] = update.message.text
    await update.message.reply_text("Manzilingizni kiriting:")
    return ADDRESS

async def get_address(update: Update, context: CallbackContext):
    context.user_data["address"] = update.message.text
    await update.message.reply_text("Sizni qiziqtirgan savolni yozing:")
    return QUESTION

async def get_question(update: Update, context: CallbackContext):
    context.user_data["question"] = update.message.text
    user_data.append(context.user_data.copy())

    # Ma'lumotlarni Excel fayliga saqlash
    df = pd.DataFrame(user_data)
    df.to_excel("users_data.xlsx", index=False)

    await update.message.reply_text("Rahmat! Ma'lumotlaringiz saqlandi.")
    return ConversationHandler.END

async def cancel(update: Update, context: CallbackContext):
    await update.message.reply_text("Suhbat bekor qilindi.")
    return ConversationHandler.END

def main():
    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
            ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_address)],
            QUESTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_question)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    app.run_polling()

if __name__ == "__main__":
    main()
