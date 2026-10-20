import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

CHANNEL = "@blac_wolf_uz"
GROUP = "@BLACK_WOLF_UZ"

SITE_URL = "https://YOUR-WEBSITE.com"


async def check_subscription(user_id, context):
    try:
        channel = await context.bot.get_chat_member(CHANNEL, user_id)
        group = await context.bot.get_chat_member(GROUP, user_id)

        channel_ok = channel.status in ["member", "administrator", "creator"]
        group_ok = group.status in ["member", "administrator", "creator"]

        return channel_ok and group_ok

    except Exception:
        return False


def subscription_buttons():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "📢 KANALGA OBUNA",
                url="https://t.me/blac_wolf_uz"
            )
        ],
        [
            InlineKeyboardButton(
                "👥 GURUHGA QO‘SHILISH",
                url="https://t.me/BLACK_WOLF_UZ"
            )
        ],
        [
            InlineKeyboardButton(
                "✅ OBUNANI TEKSHIRISH",
                callback_data="check_subscription"
            )
        ]
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    subscribed = await check_subscription(user_id, context)

    if not subscribed:
        await update.message.reply_text(
            "🐺 BLACK WOLF\n\n"
            "Botdan foydalanish uchun avval ikkala joyga ham obuna bo‘ling:\n\n"
            "📢 BLACK WOLF kanal\n"
            "👥 BLACK WOLF guruh\n\n"
            "Obuna bo‘lgach, «OBUNANI TEKSHIRISH» tugmasini bosing.",
            reply_markup=subscription_buttons()
        )
        return

    await show_main_menu(update)


async def show_main_menu(update):
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "📖 BLACK WOLF MANGA",
                callback_data="manga"
            )
        ],
        [
            InlineKeyboardButton(
                "🎬 BLACK WOLF ANIME",
                callback_data="anime"
            )
        ],
        [
            InlineKeyboardButton(
                "🐺 QAHRAMONLAR",
                callback_data="characters"
            )
        ],
        [
            InlineKeyboardButton(
                "🌐 BLACK WOLF SAYTI",
                url=SITE_URL
            )
        ]
    ])

    text = (
        "🐺 BLACK WOLF\n\n"
        "ONE PACK • ONE FAMILY • NO LIMITS\n\n"
        "BLACK WOLF olamiga xush kelibsiz."
    )

    if update.callback_query:
        await update.callback_query.edit_message_text(
            text,
            reply_markup=keyboard
        )
    else:
        await update.message.reply_text(
            text,
            reply_markup=keyboard
        )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    if query.data == "check_subscription":
        subscribed = await check_subscription(user_id, context)

        if subscribed:
            await show_main_menu(update)
        else:
            await query.edit_message_text(
                "❌ Hali ikkala joyga ham obuna bo‘lmagansiz.\n\n"
                "Avval kanal va guruhga qo‘shiling, "
                "keyin yana tekshiring.",
                reply_markup=subscription_buttons()
            )

    elif query.data == "manga":
        await query.edit_message_text(
            "📖 BLACK WOLF MANGA\n\n"
            "Bu yerda BLACK WOLF manga boblari joylashtiriladi."
        )

    elif query.data == "anime":
        await query.edit_message_text(
            "🎬 BLACK WOLF ANIME\n\n"
            "Anime qismlari tayyor bo‘lgach, shu yerga qo‘shiladi."
        )

    elif query.data == "characters":
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("⚪ MIKEY", callback_data="mikey")],
            [InlineKeyboardButton("🔵 RYUGA", callback_data="ryuga")],
            [InlineKeyboardButton("🟡 HAYATO", callback_data="hayato")],
            [InlineKeyboardButton("🔴 REI", callback_data="rei")],
            [InlineKeyboardButton("🟣 ONI", callback_data="oni")],
            [InlineKeyboardButton("⚫ YOURU", callback_data="youru")],
            [InlineKeyboardButton("🟢 KENZO", callback_data="kenzo")]
        ])

        await query.edit_message_text(
            "🐺 BLACK WOLF QAHRAMONLARI\n\n"
            "Qahramonni tanlang:",
            reply_markup=keyboard
        )

    elif query.data in [
        "mikey", "ryuga", "hayato", "rei",
        "oni", "youru", "kenzo"
    ]:

        characters = {
            "mikey": (
                "⚪ MIKEY",
                "ALPHA • LEADER • THE COLD KING"
            ),
            "ryuga": (
                "🔵 RYUGA",
                "STRATEGIST • SECOND COMMANDER • THE MIND"
            ),
            "hayato": (
                "🟡 HAYATO",
                "THE JOKER • CHEERFUL • UNPREDICTABLE"
            ),
            "rei": (
                "🔴 REI",
                "RECON • SHADOW • CROW"
            ),
            "oni": (
                "🟣 ONI",
                "MAIN CHARACTER • BLACK WOLF"
            ),
            "youru": (
                "⚫ YOURU",
                "CALM • SHADOW • UNSEEN"
            ),
            "kenzo": (
                "🟢 KENZO",
                "POWER • LOYALTY • PROTECTOR"
            )
        }

        name, role = characters[query.data]

        await query.edit_message_text(
            f"{name}\n\n"
            f"{role}\n\n"
            "BLACK WOLF guruhining asosiy qahramonlaridan biri."
        )


async def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN topilmadi!")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("🐺 BLACK WOLF BOT ISHLADI!")

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    try:
        while True:
            await asyncio.sleep(3600)
    finally:
        await app.updater.stop()
        await app.stop()
        await app.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
