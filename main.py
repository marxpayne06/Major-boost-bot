
import random
import logging
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import os

# --- 24/7 HOSTING SETUP ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = threading.Thread(target=run_flask)
    t.start()
# --------------------------

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = "8230028111:AAE7KjHeAs_77QFrSOdgQa5LcTa4pWN4gEU"

# --- UPDATED PHOTO ID ---
MAIN_PHOTO      = "AgACAgIAAxkBAAEbWRVpmhSugJjxTCKggDnihV67NWfAiAACZBZrG40h0Uj01hl16x0cRAEAAwIAA3kAAzoE"
# Note: Ensure the IDs below are also updated or replaced with URLs to prevent future "Photo Errors"
COLLAB_PHOTO    = "AgACAgIAAxkBAAEbWIdpmfbzGB9wqIMs4rAFkdDv6r6JCgACpBVrG40h0UjQfSINWpBB-AEAAwIAA3kAAzoE"
CTO_PHOTO       = "AgACAgIAAxkBAAEbSwxpmIJD_dQ3je-eHbCFoFJ7rEkFbAACMhZrG9XRyUiYbuMu64654AEAAwIAA3kAAzoE"
EXCLUSIVE_PHOTO = "AgACAgIAAxkBAAEbSyxpmIXnUol6eAlKr7rqZjqy5fEVdAACShZrG9XRyUgorHZ-HtdvBAEAAwIAA3kAAzoE"
VOTING_PHOTO    = "AgACAgIAAxkBAAEbTG5pmKdsKzkUvLl30vJ3kgR9McCzMQACvhdrG9XRyUhfy4arisGSVgEAAwIAA3kAAzoE"
WALLET_TOOLS_PHOTO = "AgACAgIAAxkBAAEbTI5pmKpwQLogcY6L73QdaSCEivFqPQAC2RdrG9XRyUiOMxc_3_KgtwEAAwIAA3gAAzoE"
SOL_TRENDING_PHOTO = "AgACAgIAAxkBAAEbWJVpmfsmuRI0mk6YH4zRlDCC_Pi59gACxBVrG40h0UjFZhAhpdwlsgEAAwIAA3kAAzoE"

CHAIN_BUTTONS = [
    [InlineKeyboardButton("🟣 Solana", callback_data="chain_sol"),
     InlineKeyboardButton("Ξ Ethereum", callback_data="chain_eth")],
    [InlineKeyboardButton("🟦 Base", callback_data="chain_base"),
     InlineKeyboardButton("🟡 BSC", callback_data="chain_bsc")],
    [InlineKeyboardButton("← Back", callback_data="back_to_short_menu")],
]

LONG_WELCOME = (
    "🎩 <b>Major Boost Bot</b>\n\n"
    "Boost your token! @MajorTrending\n\n"
    "🆕 <b>New Trending Packages</b>\nIncludes Button AD and Mass DM to reach all BuyBot users.\n\n"
    "🎁 <b>Free Volume, Bumps or Buys</b>\nIncluded with every Trending Ticket (SOL Chain only).\n\n"
    "🙍‍♂️ <b>Collab & CTO Trending</b>\nUnlock a mystery discount and let your community fund the trending!\n\n"
    "🔥 <b>Mystery Giveaway</b>\nEvery voter has a chance to instantly win up to $20 – shown right after voting!\n\n"
    "❗️ Disclaimer: @MajorBotsHub"
)

SHORT_MENU = "🎩 Major Boost Bot\n\nBoost your token! @MajorTrending\n\nChoose an option below:"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("⚡ Trending", callback_data="trending"),
         InlineKeyboardButton("📈 Volume", callback_data="volume"),
         InlineKeyboardButton("📢 Exclusive Ads", callback_data="exclusive_ads")],
        [InlineKeyboardButton("🤝 Collab Trending", callback_data="collab_trending"),
         InlineKeyboardButton("👑 CTO Trending", callback_data="cto_trending")],
        [InlineKeyboardButton("🗳️ Voting Boost", callback_data="voting_boost"),
         InlineKeyboardButton("🛠️ Free Tools", callback_data="free_tools")],
        [InlineKeyboardButton("🆘 Support", url="https://t.me/major_support_team")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        await update.message.reply_photo(
            photo=MAIN_PHOTO,
            caption=LONG_WELCOME,
            parse_mode="HTML",
            reply_markup=reply_markup
        )
    except Exception as e:
        logger.error(f"Start error: {e}")
        await update.message.reply_text(
            f"⚠️ Photo error: {str(e)}\n\n{LONG_WELCOME}",
            parse_mode="HTML",
            reply_markup=reply_markup
        )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data

    # --- BUTTON LOGIC ---
    if data == "back_to_short_menu":
        keyboard = [
            [InlineKeyboardButton("⚡ Trending", callback_data="trending"),
             InlineKeyboardButton("📈 Volume", callback_data="volume"),
             InlineKeyboardButton("📢 Exclusive Ads", callback_data="exclusive_ads")],
            [InlineKeyboardButton("🤝 Collab Trending", callback_data="collab_trending"),
             InlineKeyboardButton("👑 CTO Trending", callback_data="cto_trending")],
            [InlineKeyboardButton("🗳️ Voting Boost", callback_data="voting_boost"),
             InlineKeyboardButton("🛠️ Free Tools", callback_data="free_tools")],
            [InlineKeyboardButton("🆘 Support", url="https://t.me/major_support_team")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        caption = SHORT_MENU
        photo = MAIN_PHOTO

    elif data == "trending":
        caption = "⚡ <b>TRENDING</b>\n\n▶️ Choose your chain:"
        reply_markup = InlineKeyboardMarkup(CHAIN_BUTTONS)
        photo = MAIN_PHOTO
    
    # ... (Rest of your original if/elif logic for buttons) ...
    else:
        # Fallback to keep buttons interactive
        caption = SHORT_MENU
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("← Back", callback_data="back_to_short_menu")]])
        photo = MAIN_PHOTO

    try:
        await query.message.edit_media(
            media=InputMediaPhoto(media=photo, caption=caption, parse_mode="HTML"),
            reply_markup=reply_markup
        )
    except Exception as e:
        logger.warning(f"edit_media failed: {e}")
        # FIXED: Removed the .delete() command so the menu doesn't disappear.
        # Instead, we send a new message so the user can keep clicking.
        await query.message.reply_photo(
            photo=photo,
            caption=caption,
            parse_mode="HTML",
            reply_markup=reply_markup
        )

def main():
    keep_alive()
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
