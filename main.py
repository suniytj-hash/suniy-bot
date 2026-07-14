#!/usr/bin/env python3
"""
SUNIY TJ ACADEMY — Telegram Bot v5
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = "8522249623:AAEhdVX6xsvAZDluEhCogWslU8D8hs1oTqg"  # ⚠️ Замените на новый токен!
ADMIN_ID = 8329841937  # Только вы видите статистику

# База данных пользователей (в памяти)
users = set()

WELCOME = """👋 Хуш омадед ба SUNIY TJ ACADEMY!

🚀 Курси зеҳни сунъӣ аз 0 то натиҷа танҳо бо телефон.

📚 Зиёда аз 20 дарс
🎓 Зиёда аз 100 нафар омӯзиш гирифтанд
📱 Сурат • Видео • Реклама
• Ивази чеҳра • Мини сериал

👇 Барои гирифтани маълумоти пурра яке аз бахшҳоро интихоб намоед..."""

ABOUT = """🚀 КУРСИ ЗЕҲНИ СУНЪӢ | SUNIY TJ ACADEMY

Омӯзиши қадам ба қадам барои сохтани сурат, видео, реклама ва контент бо AI танҳо бо телефон.

🔥 Зиёда аз 100 шогирд
🔥 Миллионҳо тамошо дар шабакаҳои иҷтимоӣ
🔥 Барои шурӯъкунандагон ва блогерҳо

━━━━━━━━━━━━━━

👨‍🎓 Курс барои:

✅ Блогерҳо
✅ Соҳибони бизнес
✅ Донишҷӯён
✅ Эҷодкорони контент
✅ Ҳар касе ки мехоҳад бо AI кор кунад
✅ Ҳар касе ки мехоҳад видео ва реклама созад

━━━━━━━━━━━━━━

📚 Дарсҳо қадам ба қадам мебошанд ва ҳатто агар аз AI чизе надонед, метавонед аз сифр оғоз кунед.

📱 Барои омӯзиш танҳо телефон кофӣ аст.

🎁 Пас аз харид дастрасии доимӣ ба курс дода мешавад."""

PROGRAM = """📚 БАРНОМАИ КУРС

📖 Дарси 0 — Шиносоӣ бо курс
📖 Дарси 1 — Омодасозии аккаунт
📖 Дарси 2 — Сохтани сурат ва видео
📖 Дарси 3 — Тағйири сурат
📖 Дарси 4 — Реклама бо маҳсулот
📖 Дарси 5 — Монтаж
📖 Дарси 6 — Суруд сохтан
📖 Дарси 7 — Овоз сохтан
📖 Дарси 8 — Видео бо чеҳраи худ
📖 Дарси 9 — Мини сериал
📖 Дарси 10 — Pixar
📖 Дарси 11 — Персонажи гапзан
📖 Дарси 12 — Логотип ва обложка
📖 Дарси 13 — Инфографика
📖 Дарси 14 — Таргет Instagram
📖 Дарси 15 — Худро дар филм мондан
📖 Дарси 16 — Тарзи ройгон истифодаи зеҳни сунъӣ
📖 Дарси 17 — Ивази чеҳра дар видео
📖 Дарси 18 — 🔒 Дарси махфӣ
📖 Дарси 19 — 🔒 Дарси махфӣ
📖 Дарси 20 — 🔒 Дарси махфӣ

━━━━━━━━━━━━━━
🎁 Ва боз дарсҳои нав дар оянда илова мешаванд..."""

REVIEWS = """⭐ ФИКРИ ШОГИРДОН

Дар зер баъзе фикру мулоҳизаҳои шогирдон оварда шудаанд.

📸 Барои дидани натиҷаҳои воқеӣ тугмаи поёнро пахш намоед.

━━━━━━━━━━━━━━

⭐⭐⭐⭐⭐
Ростӣ курс хеле фаҳмо баромад.
Ман пеш ягон барномаи AI истифода накарда будам, аммо баъди чанд дарс аллакай видеои аввалини худро сохтам.
Ташаккур ба SUNIY TJ ACADEMY 🤝

━━━━━━━━━━━━━━

⭐⭐⭐⭐⭐
Ба ман бештар дарсҳои қадам ба қадам писанд омаданд.
Ҳама чиз бо телефон нишон дода шудааст ва фаҳмиданаш осон аст.
Акнун метавонам барои саҳифаи худ сурат ва видео созам.

━━━━━━━━━━━━━━

⭐⭐⭐⭐⭐
Аввал фикр мекардам AI мушкил аст.
Баъди тамошои курс фаҳмидам ки бо телефон ҳам бисёр чизҳоро сохтан мумкин будааст.
Аз ҳама бештар дарсҳои реклама ва мини сериал ба ман писанд омаданд.

━━━━━━━━━━━━━━

⭐⭐⭐⭐⭐
Ман курсро барои сохтани реклама гирифтам.
Баъди чанд дарс аллакай барои саҳифаи худ видео ва баннер сохта тавонистам.
Аз ҳама бештар дарсҳои инфографика ва реклама ба ман писанд омаданд.
Ташаккур ба SUNIY TJ ACADEMY 🙌"""

RESULTS = """🎬 НАТИҶАҲО ВА МИСОЛҲО

Дар ин ҷо метавонед натиҷаҳо, корҳои омодашуда ва пешрафти шогирдони моро бинед.

━━━━━━━━━━━━━━

📱 Барои дидани натиҷаҳо Instagram-и моро бинед:
@suniy.tj

━━━━━━━━━━━━━━

🔥 Шогирдони мо месозанд:

✅ Видео ва реклама барои бизнес
✅ Мини сериалҳо
✅ Мультфилмҳо
✅ Контент барои Instagram ва TikTok
✅ Логотип ва баннерҳо

🔥 Бисёре аз шогирдон баъди курс барои худ контент ва видеоҳои касбӣ месозанд."""

TARIFFS = """💰 ТАРИФҲО

Лутфан тарифи лозимаро интихоб намоед:

🥉 STANDARD — 249 сомонӣ
👑 VIP — 549 сомонӣ"""

STANDARD = """🥉 ТАРИФИ STANDARD — 249 СОМОНӢ

Ба тариф дохил мешавад:

✅ Сохтани сурат бо AI
✅ Сохтани видео бо AI
✅ Сохтани видео бе нишон додани чеҳра
✅ Сохтани реклама
✅ Сохтани мультфилм
✅ Сохтани мини сериал
✅ Сохтани овоз
✅ Сохтани суруд
✅ Логотип ва обложка
✅ Персонажи гапзан
✅ Роҳҳои ройгон истифода бурдани AI
✅ Гурӯҳи савол ва ҷавоб

━━━━━━━━━━━━━━

💰 Нарх: 249 сомонӣ
📚 Дастрасии доимӣ ба курс
📱 Дарсҳо онлайн дар Telegram"""

VIP = """👑 ТАРИФИ VIP — 549 СОМОНӢ

Ба тариф дохил мешавад:

✅ Ҳамаи имкониятҳои STANDARD

🔥 Сохтани персонажи шахсӣ
🔥 Сохтани контент барои блог
🔥 Таргет дар Instagram
🔥 Монтаж дар CapCut
🔥 Клони овози худ
🔥 Рекламаи маҳсулот
🔥 Инфографика
🔥 Ашёи гапзан
🔥 Дастгирии VIP
🔥 Ҷавоб ба саволҳо ва кӯмаки шахсӣ

━━━━━━━━━━━━━━

🎁 БОНУСҲО

🎁 Промптҳои тайёр
🎁 Маводҳои иловагӣ
🎁 Навсозиҳои ояндаи курс
🎁 Дастрасӣ ба гурӯҳи VIP

━━━━━━━━━━━━━━

💰 Нарх: 549 сомонӣ
📚 Дастрасии доимӣ ба курс
📱 Дарсҳо онлайн дар Telegram
👨‍💻 Дастгирии шахсӣ аз ҷониби маъмур"""

BUY = """💳 ХАРИДИ КУРС

🥉 STANDARD — 249 сомонӣ

✅ Ҳамаи дарсҳо
✅ Дастрасии доимӣ
✅ Навсозиҳои курс

━━━━━━━━━━━━━━

👑 VIP — 549 сомонӣ

✅ Ҳамаи дарсҳо
✅ Дастрасии доимӣ
✅ Навсозиҳои курс
✅ Кӯмаки шахсӣ
✅ Ҷавоб ба саволҳо
✅ Машварат

━━━━━━━━━━━━━━

📩 Пас аз интихоб рақами корт барои пардохт фиристода мешавад.

📸 Пас аз пардохт чек ё скриншоти пардохтро ирсол намоед.

✅ Баъди тасдиқи пардохт дастрасӣ ба курс дода мешавад."""

PAYMENT_STANDARD = """💳 ПАРДОХТИ STANDARD — 249 сомонӣ

━━━━━━━━━━━━━━

🏦 Душанбе Сити
📱 900 779 222
👤 Ба номи: ПАРВИНА М.

━━━━━━━━━━━━━━

🏦 Алиф Бонк
💳 4444 8844 1014 0902
👤 Ба номи: Ш. Ҷ.

━━━━━━━━━━━━━━

📩 Пас аз пардохт чек ё скриншоти пардохтро ба Telegram фиристед:
📲 @suniy_tj

✅ Пас аз тасдиқи пардохт дастрасӣ ба курс дода мешавад.
🤝 Ташаккур барои боварӣ ба SUNIY TJ ACADEMY."""

PAYMENT_VIP = """💳 ПАРДОХТИ VIP — 549 сомонӣ

━━━━━━━━━━━━━━

🏦 Душанбе Сити
📱 900 779 222
👤 Ба номи: ПАРВИНА М.

━━━━━━━━━━━━━━

🏦 Алиф Бонк
💳 4444 8844 1014 0902
👤 Ба номи: Ш. Ҷ.

━━━━━━━━━━━━━━

📩 Пас аз пардохт чек ё скриншоти пардохтро ба Telegram фиристед:
📲 @suniy_tj

✅ Пас аз тасдиқи пардохт дастрасӣ ба курс дода мешавад.
🤝 Ташаккур барои боварӣ ба SUNIY TJ ACADEMY."""

CONTACT = """📞 ТАМОС БО МО

━━━━━━━━━━━━━━

📱 WhatsApp:
900 779 222

📲 Telegram:
@suniy_tj

📸 Instagram:
@suniy.tj

━━━━━━━━━━━━━━

🤝 Агар савол дошта бошед ё маълумоти бештар хоҳед, ба мо нависед.

⚡ Одатан дар муддати кӯтоҳ ҷавоб медиҳем."""


VPN = """🇹🇯 VPN-и ватанӣ

⚡️ Тез, устувор ва қулай барои истифода.

👇 Барои фаъол кардани VPN ба линкаи зер ворид шавед:

🔗 https://t.me/WebSafeTelbot?start=ref_ODMyOTg0MTkzNy4wDly57ogZbQ"""

# ===================== КЛАВИАТУРЫ =====================

def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎓 Дар бораи курс", callback_data="about")],
        [InlineKeyboardButton("💰 Тарифҳо", callback_data="tariffs")],
        [InlineKeyboardButton("📚 Барномаи курс", callback_data="program")],
        [InlineKeyboardButton("🎬 Натиҷаҳо ва мисолҳо", callback_data="results")],
        [InlineKeyboardButton("⭐ Фикри шогирдон", callback_data="reviews")],
        [InlineKeyboardButton("🧾 Харид кардан", callback_data="buy")],
        [InlineKeyboardButton("🇹🇯 VPN-и ватанӣ", callback_data="vpn")],
        [InlineKeyboardButton("📞 Тамос бо маъмур", callback_data="contact")],
    ])

def back_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ Бозгашт", callback_data="menu")]
    ])

def tariffs_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🥉 STANDARD — 249 сомонӣ", callback_data="standard")],
        [InlineKeyboardButton("👑 VIP — 549 сомонӣ", callback_data="vip")],
        [InlineKeyboardButton("⬅️ Бозгашт", callback_data="menu")],
    ])

def buy_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🥉 STANDARD — 249 сомонӣ", callback_data="pay_standard")],
        [InlineKeyboardButton("👑 VIP — 549 сомонӣ", callback_data="pay_vip")],
        [InlineKeyboardButton("⬅️ Бозгашт", callback_data="menu")],
    ])

def reviews_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📸 Натиҷаҳо дар Instagram", url="https://www.instagram.com/suniy.tj")],
        [InlineKeyboardButton("⬅️ Бозгашт", callback_data="menu")],
    ])

def results_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📸 Instagram @suniy.tj", url="https://www.instagram.com/suniy.tj")],
        [InlineKeyboardButton("⬅️ Бозгашт", callback_data="menu")],
    ])

def contact_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💬 WhatsApp", url="https://wa.me/992900779222")],
        [InlineKeyboardButton("📲 Telegram @suniy_tj", url="https://t.me/suniy_tj")],
        [InlineKeyboardButton("📸 Instagram @suniy.tj", url="https://www.instagram.com/suniy.tj")],
        [InlineKeyboardButton("⬅️ Бозгашт", callback_data="menu")],
    ])

def standard_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💳 Харид кардан", callback_data="pay_standard")],
        [InlineKeyboardButton("⬅️ Бозгашт", callback_data="tariffs")],
    ])

def vip_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💳 Харид кардан", callback_data="pay_vip")],
        [InlineKeyboardButton("⬅️ Бозгашт", callback_data="tariffs")],
    ])

def pay_menu(back):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📲 Ба @suniy_tj нависед", url="https://t.me/suniy_tj")],
        [InlineKeyboardButton("⬅️ Бозгашт", callback_data=back)],
    ])

# ===================== ХЕНДЛЕРЫ =====================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    users.add(user_id)
    await update.message.reply_text(WELCOME, reply_markup=main_menu())

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    await update.message.reply_text(f"👥 Ҷамъи корбарон: {len(users)} нафар")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    texts = {
        "menu": (WELCOME, main_menu()),
        "about": (ABOUT, back_menu()),
        "program": (PROGRAM, back_menu()),
        "results": (RESULTS, results_menu()),
        "reviews": (REVIEWS, reviews_menu()),
        "tariffs": (TARIFFS, tariffs_menu()),
        "standard": (STANDARD, standard_menu()),
        "vip": (VIP, vip_menu()),
        "buy": (BUY, buy_menu()),
        "pay_standard": (PAYMENT_STANDARD, pay_menu("standard")),
        "pay_vip": (PAYMENT_VIP, pay_menu("vip")),
        "contact": (CONTACT, contact_menu()),
        "vpn": (VPN, back_menu()),
    }

    if data in texts:
        text, keyboard = texts[data]
        await query.message.reply_text(text, reply_markup=keyboard)
        try:
            await query.message.delete()
        except Exception:
            pass


async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    if not context.args:
        await update.message.reply_text("❌ Напишите текст! Пример:\n/broadcast Ваш текст")
        return
    text = " ".join(context.args)
    success = 0
    fail = 0
    for user_id in users:
        try:
            await context.bot.send_message(chat_id=user_id, text=text)
            success += 1
        except Exception:
            fail += 1
    await update.message.reply_text(f"✅ Отправлено: {success} нафар\n❌ Не доставлено: {fail} нафар")

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    users.add(user_id)
    await update.message.reply_text(WELCOME, reply_markup=main_menu())

# ===================== ЗАПУСК =====================

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, unknown))
    print("✅ Бот SUNIY TJ ACADEMY запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
