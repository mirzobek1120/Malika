from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os

TOKEN = os.environ["BOT_TOKEN"]
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Qurilmalar, rasm va matn
DATA = {
    "🧠 RAM": ("images/ram.jpg",
               "🧠 Operativ xotira (RAM)\n\nOperativ xotira (RAM) — kompyuter ishlayotgan vaqtda dasturlar va ma’lumotlarni vaqtincha saqlaydi.\nKompyuter o‘chirilsa, RAM dagi ma’lumotlar yo‘qoladi.\nRAM qancha katta bo‘lsa, kompyuter shuncha tez ishlaydi."),
    "💾 HDD / SSD": ("images/hdd.jpg",
                     "💾 Qattiq disk (HDD / SSD)\n\nQattiq disk — kompyuterda barcha fayllar, dasturlar va operatsion tizim saqlanadigan qurilma.\nHDD mexanik, SSD esa tez ishlaydigan elektron xotiradir.\nSSD kompyuterni tezroq ishga tushiradi."),
    "🧩 Ona plata": ("images/motherboard.jpg",
                     "🧩 Ona plata (Motherboard)\n\nOna plata — kompyuterning asosiy platasi.\nBarcha qurilmalar (CPU, RAM, video karta) shu plataga ulanadi.\nU kompyuter qismlarining o‘zaro ishlashini ta’minlaydi."),
    "📦 Keys": ("images/case.jpg",
                "📦 Keys (Case)\n\nKeys — kompyuter qismlarini joylashtiradigan korpus.\nU qismlarni chang va zarbalardan himoya qiladi.\nShuningdek, havo aylanishiga yordam beradi."),
    "⚙️ CPU": ("images/cpu.jpg",
               "⚙️ Protsessor (CPU)\n\nProtsessor — kompyuterning miyasi.\nU barcha buyruqlarni bajaradi va hisob-kitob qiladi.\nProtsessor qanchalik kuchli bo‘lsa, kompyuter tez ishlaydi."),
    "🎮 Video karta": ("images/gpu.jpg",
                       "🎮 Video karta (GPU)\n\nVideo karta — grafik ma’lumotlarni qayta ishlaydi.\nO‘yinlar, video va rasmlar sifati video kartaga bog‘liq.\nKuchli video karta dizayn va o‘yinlar uchun kerak."),
    "🔌 Quvvat manbai": ("images/psu.jpg",
                         "🔌 Quvvat manbai (PSU)\n\nQuvvat manbai — kompyuterni elektr energiyasi bilan ta’minlaydi.\nU tokni barcha qismlarga tarqatadi.\nSifatli quvvat manbai kompyuterni himoya qiladi."),
    "❄️ Cooler": ("images/cooler.jpg",
                  "❄️ Sovutish tizimi (Cooler)\n\nSovutish tizimi — kompyuter qismlarini sovitadi.\nAyniqsa protsessor qizib ketmasligi uchun kerak.\nU ventilyator va radiatorlardan iborat bo‘ladi."),
    "🖥 Monitor": ("images/monitor.jpg",
                  "🖥 Monitor\n\nMonitor — kompyuter ma’lumotlarini ekranda ko‘rsatadi.\nMatn, rasm va videolar monitorda aks etadi.\nMonitor sifati ko‘rishga qulaylik beradi."),
    "⌨️ Klaviatura": ("images/keyboard.jpg",
                      "⌨️ Klaviatura (Keyboard)\n\nKlaviatura — matn va buyruqlar kiritish uchun ishlatiladi.\nHarflar, raqamlar va maxsus tugmalardan iborat.\nU kompyuter bilan muloqot qilish vositasidir."),
    "🖱 Sichqoncha": ("images/mouse.jpg",
                     "🖱 Sichqoncha (Mouse)\n\nSichqoncha — kursorni boshqarish uchun ishlatiladi.\nU tanlash, bosish va surish vazifalarini bajaradi.\nGrafik ishlar uchun juda qulay."),
    "📠 Skaner": ("images/scanner.jpg",
                  "📠 Skaner (Scanner)\n\nSkaner — qog‘oz hujjatlarni kompyuterga kiritadi.\nRasm va matnlarni raqamlashtiradi.\nOfis va maktablarda ishlatiladi."),
    "🖨 Printer": ("images/printer.jpg",
                   "🖨 Printer\n\nPrinter — kompyuterdagi ma’lumotlarni qog‘ozga chiqaradi.\nMatn va rasmlarni chop etadi.\nU lazerli yoki siyohli bo‘lishi mumkin."),
    "ℹ️ Bot haqida": (None,
                      "ℹ️ Bu bot 9-maktab o‘quvchisi Faridova Malika tomonidan yaratildi.")
}

# Pastki panel tugmalari (doimiy)
keyboard_buttons = [
    ["🧠 RAM", "💾 HDD / SSD", "🧩 Ona plata", "📦 Keys"],
    ["⚙️ CPU", "🎮 Video karta", "🔌 Quvvat manbai", "❄️ Cooler"],
    ["🖥 Monitor", "⌨️ Klaviatura", "🖱 Sichqoncha", "📠 Skaner"],
    ["🖨 Printer", "ℹ️ Bot haqida"]
]

reply_markup = ReplyKeyboardMarkup(keyboard_buttons, resize_keyboard=True)

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name
    await update.message.reply_text(
        f"Salom {name} 😊\n"
        f"Bu botni Faridova Malika ishga tushirdi.\n\n"
        f"Quyidagi menyudan tanlang 👇",
        reply_markup=reply_markup
    )

# Matn xabarlarini qayta ishlash (rasm + matn)
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text in DATA:
        img_path, info_text = DATA[text]
        if img_path:
            with open(os.path.join(BASE_DIR, img_path), "rb") as photo:
                await update.message.reply_photo(photo=photo, caption=info_text)
        else:
            await update.message.reply_text(info_text)
    else:
        await update.message.reply_text("Iltimos, pastki menyudan tanlang 👇")
    
    # Tugmalarni yana pastki panelda chiqarish
    await update.message.reply_text("🔽 Tanlang:", reply_markup=reply_markup)

# Bot ishga tushirish
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
app.run_polling()
