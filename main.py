import random
import logging
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
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

# Logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = "8230028111:AAE7KjHeAs_77QFrSOdgQa5LcTa4pWN4gEU"

# Photos (updated/added the ones you specified)
MAIN_PHOTO      = "AgACAgIAAxkBAAEDJ0tpkkmqIdsliLFxwSgmhXty3PARVwACfg9rG2yOmEhK28zLz3KpYwEAAwIAA3kAAzoE"
COLLAB_PHOTO    = "AgACAgIAAxkBAAEbSwxpmIJD_dQ3je-eHbCFoFJ7rEkFbAACMhZrG9XRyUiYbuMu64654AEAAwIAA3kAAzoE"  # ← updated as requested
CTO_PHOTO       = "AgACAgIAAxkBAAEbSwxpmIJD_dQ3je-eHbCFoFJ7rEkFbAACMhZrG9XRyUiYbuMu64654AEAAwIAA3kAAzoE"  # ← updated as requested
EXCLUSIVE_PHOTO = "AgACAgIAAxkBAAEbSyxpmIXnUol6eAlKr7rqZjqy5fEVdAACShZrG9XRyUgorHZ-HtdvBAEAAwIAA3kAAzoE"  # ← updated as requested
VOTING_PHOTO    = "AgACAgIAAxkBAAEDJ2NpkmG3S76BOLcDS6t7FE_VeMx5MQACnhhrG9vzkUjW7miUVjLbHAEAAwIAA3kAAzoE"

# Chain buttons (used for collab, cto, trending)
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
        [InlineKeyboardButton("🆘 Support", callback_data="support")],
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

    if data == "back_to_short_menu":
        keyboard = [
            [InlineKeyboardButton("⚡ Trending", callback_data="trending"),
             InlineKeyboardButton("📈 Volume", callback_data="volume"),
             InlineKeyboardButton("📢 Exclusive Ads", callback_data="exclusive_ads")],
            [InlineKeyboardButton("🤝 Collab Trending", callback_data="collab_trending"),
             InlineKeyboardButton("👑 CTO Trending", callback_data="cto_trending")],
            [InlineKeyboardButton("🗳️ Voting Boost", callback_data="voting_boost"),
             InlineKeyboardButton("🛠️ Free Tools", callback_data="free_tools")],
            [InlineKeyboardButton("🆘 Support", callback_data="support")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        caption = SHORT_MENU
        photo = MAIN_PHOTO

    elif data == "trending":
        caption = (
            "⚡ <b>TRENDING</b>\n\n"
            "🆕 Button AD Included\nEvery Trending Ticket comes with a guaranteed Button AD placement.\n\n"
            "🆕 Mass DM (Optional)\nReach over 600K+ BuyBot users with an additional Mass DM push.\n\n"
            "🎁 Free Volume, Bumps & Buys\nIncluded with every trending (SOL Chain only).\n\n"
            "▶️ Choose your chain:"
        )
        reply_markup = InlineKeyboardMarkup(CHAIN_BUTTONS)
        photo = MAIN_PHOTO

    elif data == "collab_trending":
        caption = (
            "👥 <b>COLLAB TRENDING – Powered by Community</b>\n\n"
            "🎁 NO Upfront Payment\n\n"
            "🔥 You have 60 minutes to raise the goal\n"
            "If met → Auto listed | If not → Auto refund\n\n"
            "➗ Mystery Button – Unlock Hidden Deals\n\n"
            "▶️ Select chain to begin:"
        )
        reply_markup = InlineKeyboardMarkup(CHAIN_BUTTONS)
        photo = COLLAB_PHOTO

    elif data == "cto_trending":
        caption = (
            "👥 <b>CTO TRENDING – No Dev? No Problem</b>\n\n"
            "🔥 Community takeover trending\n"
            "⏱ 60 minutes funding\n"
            "💸 Auto refund if failed\n\n"
            "➗ Mystery Discount Available\n\n"
            "▶️ Select chain:"
        )
        reply_markup = InlineKeyboardMarkup(CHAIN_BUTTONS)
        photo = CTO_PHOTO

    elif data == "exclusive_ads":
        caption = (
            "🎩 <b>Exclusive Ads – High Impact Promotion for Your Project</b>\n\n"
            "🔥 Reach thousands of real users with our top tier ad options across the Major ecosystem.\n\n"
            "⚡️ Choose one of the options below to learn more and boost your project visibility."
        )
        
        # Buttons with emojis + randomized order
        ad_options = [
            InlineKeyboardButton("🚀 Major Ultimate Boost", callback_data="major_ultimate"),
            InlineKeyboardButton("🗳️ Join2Vote", callback_data="join_vote"),
            InlineKeyboardButton("📩 Mass DM", callback_data="mass_dm"),
            InlineKeyboardButton("🔘 Button Ads", callback_data="button_ads"),
            InlineKeyboardButton("🎤 Major AMA", callback_data="major_ama"),
        ]
        random.shuffle(ad_options)
        
        # Make it more square/random-looking (2–3 per row mix)
        keyboard = []
        i = 0
        while i < len(ad_options):
            if random.random() > 0.4 and i + 1 < len(ad_options):
                keyboard.append([ad_options[i], ad_options[i+1]])
                i += 2
            else:
                keyboard.append([ad_options[i]])
                i += 1
        
        keyboard.append([InlineKeyboardButton("← Back", callback_data="back_to_short_menu")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        photo = EXCLUSIVE_PHOTO

    elif data == "voting_boost":
        caption = (
            "🗳 <b>Voting Boost</b>\n\n"
            "⚡️ Boost your token's votes instantly and climb higher in the @MajorCommunityTrending!\n\n"
            "⭐️ Each boost is valid for 24 hours and adds instant votes to your project - no waiting, no limits.\n"
            "Anyone can support a token: developers, holders, or community members.\n\n"
            "<b>🗳 Top 3 Daily Winners</b>\nThe top 3 tokens will be shared as our daily winners on our partner call channels.\n\n"
            "🔥 Boosts can be stacked:\nMultiple boosts will add up to your total votes for even higher visibility.\n\n"
            "▶️ Select the number of votes you want to purchase:"
        )
        vote_buttons = [
            [InlineKeyboardButton("10 Votes – $5", callback_data="vote_10")],
            [InlineKeyboardButton("50 Votes – $20", callback_data="vote_50")],
            [InlineKeyboardButton("100 Votes – $35", callback_data="vote_100")],
            [InlineKeyboardButton("500 Votes – $150", callback_data="vote_500")],
            [InlineKeyboardButton("1000 Votes – $250", callback_data="vote_1000")],
            [InlineKeyboardButton("← Back", callback_data="back_to_short_menu")],
        ]
        reply_markup = InlineKeyboardMarkup(vote_buttons)
        photo = VOTING_PHOTO

    else:
        caption = f"Coming soon: {data.replace('_', ' ').title()} section 🚧"
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("← Back", callback_data="back_to_short_menu")]])
        photo = MAIN_PHOTO

    try:
        await query.message.edit_media(
            media=InputMediaPhoto(
                media=photo,
                caption=caption,
                parse_mode="HTML"
            ),
            reply_markup=reply_markup
        )
    except Exception as e:
        logger.warning(f"edit_media failed: {e}")
        try:
            await query.message.delete()
        except:
            pass
        await query.message.reply_photo(
            photo=photo,
            caption=caption,
            parse_mode="HTML",
            reply_markup=reply_markup
        )

def main():
    keep_alive()
    app_bot = ApplicationBuilder().token(BOT_TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(CallbackQueryHandler(button_handler))
    print("Major Boost Bot running... Test /start")
    app_bot.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
