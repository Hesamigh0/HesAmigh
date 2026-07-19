# -*- coding: utf-8 -*-
"""
بات معرفی و پشتیبانی شخصی حسام
----------------------------------
نصب:
    pip install pyTelegramBotAPI openai

اجرا:
    1) از @BotFather یک بات بساز و توکن بگیر -> BOT_TOKEN
    2) (اختیاری ولی پیشنهادی) از platform.openai.com یک API key بگیر
       تا بات با هوش مصنوعی واقعی جواب بده -> OPENAI_API_KEY
    3) python hesam_bio_bot.py

میزبانی رایگان: Railway.app یا Render.com (از موبایل/آیپد هم قابل مدیریته)
"""

import os
import telebot

# ============ تنظیمات ============
BOT_TOKEN = os.environ.get("BOT_TOKEN", "TOKEN-خودت-رو-اینجا-بذار")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")  # اختیاری

# نکته امنیتی: شماره تماس رو پیش‌فرض مخفی نگه داشتم.
# چون بات عمومیه و هرکسی می‌تونه بهش پیام بده، بهتره فقط از طریق
# آیدی تلگرام باهات ارتباط بگیرن، نه شماره موبایل مستقیم.
SHOW_PHONE = False

BIO = {
    "نام": "حسام عمیق",
    "شهر": "بجنورد",
    "تحصیلات": "دانش‌آموز",
    "هدف": "یادگیری برنامه‌نویسی و ساخت برندهای حرفه‌ای",
    "پروژه‌ها": [
        "برندینگ و مارکتینگ یک کلینیک دندانپزشکی (وبسایت و افتتاحیه)",
        "پروژه‌ای در حوزه سینما و تولید محتوا",
        "همکاری در یک شرکت سرمایه‌گذاری خانوادگی",
    ],
    "مهارت‌ها": [
        "Graphic Design", "Logo Design", "Branding", "Video Editing",
        "DaVinci Resolve", "Barista", "Content Creation", "Marketing",
        "Photography", "Cinematic Filming", "Python", "n8n", "AI",
    ],
    "تلگرام": "@HesamAmigh",
    "تلفن": "09045197418",
}

SYSTEM_CONTEXT = f"""
تو دستیار شخصی {BIO['نام']} هستی. با لحن فارسی، صمیمی، خلاصه و دقیق جواب بده.
این اطلاعات درباره اونه:
شهر: {BIO['شهر']}
تحصیلات: {BIO['تحصیلات']}
هدف: {BIO['هدف']}
پروژه‌ها: {', '.join(BIO['پروژه‌ها'])}
مهارت‌ها و علایق: {', '.join(BIO['مهارت‌ها'])}
برای تماس بگو پیام بده به {BIO['تلگرام']} در تلگرام.
هیچ اطلاعات دیگه‌ای غیر از موارد بالا رو حدس نزن یا اضافه نکن.
جواب‌ها کوتاه و کاربردی باشن (حداکثر ۴-۵ خط).
"""

# ============ متن‌های آماده (حالت بدون AI) ============

def intro_text():
    return (
        f"سلام! من دستیار شخصی {BIO['نام']} هستم 👋\n\n"
        f"🎯 هدف: {BIO['هدف']}\n"
        f"📍 شهر: {BIO['شهر']}\n"
        f"💡 مهارت‌ها: {', '.join(BIO['مهارت‌ها'][:6])}...\n"
        f"🚀 پروژه‌ها: {len(BIO['پروژه‌ها'])} پروژه فعال\n\n"
        "هر سوالی درباره‌اش داری بپرس."
    )


def contact_text():
    txt = f"برای ارتباط با {BIO['نام']} پیام بده: {BIO['تلگرام']}"
    if SHOW_PHONE:
        txt += f"\nشماره تماس: {BIO['تلفن']}"
    return txt


def projects_text():
    return "پروژه‌های در دست اقدام:\n- " + "\n- ".join(BIO["پروژه‌ها"])


def skills_text():
    return "مهارت‌ها و علایق:\n- " + "\n- ".join(BIO["مهارت‌ها"])


KEYWORD_MAP = {
    contact_text: ["تماس", "ارتباط", "شماره", "آیدی", "پیام بدم"],
    projects_text: ["پروژه", "کار", "کسب و کار", "کسب‌وکار", "کلینیک", "سینما", "سرمایه"],
    skills_text: ["مهارت", "برنامه نویسی", "برنامه‌نویسی", "پایتون", "python",
                  "ai", "هوش مصنوعی", "n8n", "طراحی", "ادیت", "دیزاین"],
}


def rule_based_answer(text):
    t = text.lower()
    for func, keywords in KEYWORD_MAP.items():
        if any(k.lower() in t for k in keywords):
            return func()
    return (
        "دقیق متوجه نشدم چی می‌خوای بدونی 🙂\n"
        "می‌تونی بپرسی: پروژه‌ها چیه؟ مهارت‌هاش چیه؟ چطور تماس بگیرم؟"
    )


# ============ حالت هوش مصنوعی (اختیاری) ============

def ai_answer(question):
    """اگه OPENAI_API_KEY تنظیم شده باشه، از OpenAI برای جواب هوشمند استفاده می‌کنه."""
    if not OPENAI_API_KEY:
        return None
    try:
        from openai import OpenAI
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            max_tokens=300,
            messages=[
                {"role": "system", "content": SYSTEM_CONTEXT},
                {"role": "user", "content": question},
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"AI error: {e}")
        return None


def find_answer(text):
    ai_result = ai_answer(text)
    if ai_result:
        return ai_result
    return rule_based_answer(text)


# ============ راه‌اندازی بات ============
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")


@bot.message_handler(commands=["start", "help"])
def handle_start(message):
    bot.reply_to(message, intro_text())


@bot.message_handler(func=lambda m: True, content_types=["text"])
def handle_text(message):
    bot.reply_to(message, find_answer(message.text))


if __name__ == "__main__":
    print("بات در حال اجراست... (Ctrl+C برای توقف)")
    bot.infinity_polling()
