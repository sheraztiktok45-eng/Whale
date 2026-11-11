import telebot
import re

# --- APNI DETAILS YAHAN LIKHEIN ---
# Jo token BotFather ne diya tha, use in quotes "" ke andar likhein
BOT_TOKEN =   "9054865447:AAGxzCywRwr8gBGx3X9ByHxg-pIwKJWIZL8"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(func=lambda message: True)
def filter_and_forward(message):
    msg_text = message.text.lower() if message.text else ""
    should_forward = False

    # 1. Whale Alert Filters (Exchange to Wallet / Wallet to Exchange & USDT Mint)
    if "whale" in msg_text or "alert" in msg_text:
        if ("exchange" in msg_text and "wallet" in msg_text) and not ("wallet to wallet" in msg_text):
            should_forward = True
        elif "minted" in msg_text and "usdt" in msg_text:
            should_forward = True

    # 2. Onchain Data Filters (BTC & ETH Inflow/Outflow)
    has_crypto = ("btc" in msg_text or "bitcoin" in msg_text or "eth" in msg_text or "ethereum" in msg_text)
    has_flow = ("inflow" in msg_text or "outflow" in msg_text or "exchange netflow" in msg_text)
    
    if has_crypto and has_flow:
        should_forward = True

    # Agar message hamari shart par poora utray to reply karega
    if should_forward:
        bot.reply_to(message, f"🎯 **[Filtered Alert]**\n\n{message.text}", parse_mode="Markdown")
    else:
        # Bakwas messages ko bot automatically group se delete kar dega
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except Exception:
            pass

print("Filter Bot successfully started...")
bot.infinity_polling()
  
