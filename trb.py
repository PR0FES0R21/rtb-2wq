import telebot
from telebot import types
import logging
import time
import requests

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Ganti dengan API token bot Anda
API_TOKEN = '7343119973:AAHsthbTmna_Ogwi_52P6WtHr48Hlcp7jyI'

# Inisialisasi bot
bot = telebot.TeleBot(API_TOKEN)

# Handler untuk perintah /start
@bot.message_handler(commands=['start'])
def start(message):
    try:
        logger.info(f"Received /start command from user: {message.from_user.username}")

        # Inline keyboard markup
        inline_markup = types.InlineKeyboardMarkup()

        # URL button (WebAppInfo)
        url_btn = types.InlineKeyboardButton(
            text="🎮 Mainkan Sekarang",
            web_app=types.WebAppInfo(url="https://pr0fes0r21.github.io/rois_coin_bot/", fullscreen=True)  # Ganti URL dengan yang sesuai
        )
        inline_markup.add(url_btn)

        # Inline buttons for About, Invite, Announcement, and Chat Group
        about_btn = types.InlineKeyboardButton("ℹ️ About", callback_data="about")
        invite_btn = types.InlineKeyboardButton("💌 Invite", callback_data="invite")
        announcement_btn = types.InlineKeyboardButton("📢 Announcement", url="https://t.me/+VpyrwKHR7hxkODE1")
        chat_group_btn = types.InlineKeyboardButton("👥 Chat Group", url="https://t.me/+1MpAxTxgWK0xZjRl")

        # Adding buttons in rows
        inline_markup.row(about_btn, invite_btn)
        inline_markup.row(announcement_btn, chat_group_btn)

        # Kirim pesan dengan gambar dan inline markup
        photo_path = 'image.png'
        with open(photo_path, 'rb') as photo:
            # Retry logic with a maximum of 5 retries
            for attempt in range(5):
                try:
                    bot.send_photo(
                        message.chat.id, 
                        photo, 
                        caption=f"Selamat datang @{message.from_user.username} 🤖🚀 Kami mengundang Anda untuk meraih peluang dalam dunia crypto dengan bergabung dalam program airdrop Rois Coin. Di sini, Anda tidak hanya mendapatkan Rois Coin secara cuma-cuma, tetapi juga memasuki pintu pertama ke dalam ekosistem blockchain yang penuh inovasi dan potensi besar. Segera jelajahi fitur-fitur eksklusif, ikuti perkembangan terbaru, dan raih keuntungan di tengah komunitas yang dinamis dan mendukung. Mari mulai petualangan crypto Anda bersama Rois Coin Bot!", 
                        reply_markup=inline_markup
                    )
                    logger.info("Photo sent successfully.")
                    break  # Break the loop if the request was successful
                except requests.exceptions.RequestException as e:
                    logger.error(f"Attempt {attempt + 1}: Failed to send photo. Error: {e}")
                    if attempt < 4:
                        time.sleep(2 ** attempt)  # Exponential backoff
                    else:
                        raise  # Re-raise the exception after the final attempt
    except Exception as e:
        logger.error(f"Failed to process /start command. Error: {e}")

# Handler untuk callback dari tombol About dan Invite
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    try:
        logger.info(f"Callback received: {call.data}")
        if call.data == "about":
            bot.send_message(call.message.chat.id, "Rois Coin adalah proyek cryptocurrency inovatif yang bertujuan untuk memperluas akses ke ekosistem crypto bagi semua orang. Dengan fokus pada keamanan, keandalan, dan inovasi, Rois Coin menawarkan solusi untuk mendukung transaksi global yang efisien dan aman.")
        elif call.data == "invite":
            bot.send_message(call.message.chat.id, f"Kode undangan anda https://t.me/RoisCoin_bot?start={call.message.chat.id}")
    except Exception as e:
        logger.error(f"Failed to process callback query. Error: {e}")

# Start polling
try:
    bot.polling()
except Exception as e:
    logger.error(f"Failed to start polling. Error: {e}")
