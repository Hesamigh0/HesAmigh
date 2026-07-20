# -*- coding: utf-8 -*-
"""
بات معرفی و پشتیبانی شخصی حسام
----------------------------------
نصب:
    pip install pyTelegramBotAPI google-genai

اجرا:
    1) از @BotFather یک بات بساز و توکن بگیر -> BOT_TOKEN
    2) (اختیاری ولی پیشنهادی) از aistudio.google.com یک API key رایگان بگیر
       تا بات با هوش مصنوعی واقعی جواب بده -> GEMINI_API_KEY
    3) python hesam_bio_bot.py

میزبانی رایگان: Railway.app یا Render.com (از موبایل/آیپد هم قابل مدیریته)
"""

import os
import telebot

# ============ تنظیمات ============
BOT_TOKEN = os.environ.get("BOT_TOKEN", "TOKEN-خودت-رو-اینجا-بذار")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")  # اختیاری

# نکته امنیتی: شماره تماس رو پیش‌فرض مخفی نگه داشتم.
# چون بات عمومیه و هرکسی می‌تونه بهش پیام بده، بهتره فقط از طریق
# آیدی تلگرام باهات ارتباط بگیرن، نه شماره موبایل مستقیم.
SHOW_PHONE = False

BIO = {
    "نام": "حسام عمیق",
    "شهر": "بجنورد",
    "تحصیلات": "دانش‌آموز",
    "هدف": "کارآفرین شدن، ساخت چند شرکت، و تسلط بر برنامه‌نویسی و هوش مصنوعی",
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
    "مسیر یادگیری": [
        "Python", "Backend Development", "Frontend Development",
        "AI Agents", "Automation", "Networking", "Linux", "Business Systems",
    ],
    "علایق": [
        "هوش مصنوعی", "اتوماسیون", "استارتاپ", "برندینگ",
        "قهوه و اسپرسو", "موکتل", "مدیریت کافه", "UI Design", "System Design",
    ],
    "ارزش‌ها": [
        "هوش مصنوعی آینده‌ست",
        "برنامه‌نویسی یکی از ارزشمندترین مهارت‌هاست",
        "ساختن کسب‌وکار بهتر از کارمندی‌ست",
        "سیستم‌سازی مهم‌تر از درآمد موقتیه",
        "یادگیری مداوم ضروریه",
    ],
    "تلگرام": "@HesamAmigh",
    "تلفن": "09045197418",
}

SYSTEM_CONTEXT = f"""
تو دستیار شخصی {BIO['نام']} هستی و به سوالات آدم‌های غریبه که پیام میدن جواب میدی.
این پس‌زمینه رو کامل بدون که جواب‌های بهتر و دقیق‌تری بدی، ولی همه‌ی جزئیات رو یکجا
تو یک پیام ندون - فقط چیزی که مرتبط با سوال طرفه رو بگو، خلاصه و کاربردی.

شهر: {BIO['شهر']}
تحصیلات: {BIO['تحصیلات']}
هدف: {BIO['هدف']}
پروژه‌ها: {', '.join(BIO['پروژه‌ها'])}
مهارت‌ها: {', '.join(BIO['مهارت‌ها'])}
مسیر یادگیری فعلی: {', '.join(BIO['مسیر یادگیری'])}
علایق: {', '.join(BIO['علایق'])}
ارزش‌ها و نگرش: {', '.join(BIO['ارزش‌ها'])}

برای تماس بگو پیام بده به {BIO['تلگرام']} در تلگرام.
هیچ اطلاعات دیگه‌ای غیر از موارد بالا رو حدس نزن یا اضافه نکن.
درباره جزئیات شخصی/خانوادگی که اینجا نیومده (مثل مسائل خانوادگی یا مالی) چیزی نگو.
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
    """اگه GEMINI_API_KEY تنظیم شده باشه، از Google Gemini برای جواب هوشمند استفاده می‌کنه."""
    if not GEMINI_API_KEY:
        return None
    try:
        from google import genai
        from google.genai import types
        client = genai.Client(api_key=GEMINI_API_KEY)
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=question,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_CONTEXT,
                max_output_tokens=300,
            ),
        )
        return response.text
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
