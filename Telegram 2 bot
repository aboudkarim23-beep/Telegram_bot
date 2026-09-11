import logging
import re
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    filters,
    ContextTypes,
)

# تفعيل سجلات التتبع لمراقبة أداء البوت في Render
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# بيانات التوكن ومعرّف حساب الأدمن
BOT_TOKEN = "ضع_توكن_البوت_هنا"
ADMIN_CHAT_ID = 1765522064

# مراحل المحادثة
WAITING_PHONE = 1

# القائمة الرئيسية
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("طلب جديد 📦", callback_data="new_order")],
        [InlineKeyboardButton("تواصل معنا 💬", callback_data="support")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        await update.message.reply_text("أهلاً بك! الرجاء الاختيار من القائمة:", reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.message.reply_text("أهلاً بك! الرجاء الاختيار من القائمة:", reply_markup=reply_markup)

# استقبال الضغط على الأزرار
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "new_order":
        await query.edit_message_text("الرجاء إدخال رقم الهاتف لإتمام الطلب:")
        return WAITING_PHONE
    elif query.data == "support":
        await query.edit_message_text("للتواصل والدعم، أرسل استفسارك هنا مباشرة.")
        return ConversationHandler.END

# استخراج رقم الهاتف وإرسال التنبيهات
async def handle_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    
    # فحص الرقم التونسي المكون من 8 أرقام
    match = re.search(r"\b[2459]\d{7}\b", text)
    
    if match:
        phone = match.group(0)
        
        # الرد على المستخدم
        await update.message.reply_text(f"تم إرسال التنبيه بنجاح للطلب الخاص برقم: {phone}")
        
        # إرسال إشعار فوري لحساب الأدمن
        admin_message = f"🔔 طلب جديد وارد:\nالرقم: {phone}"
        try:
            await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=admin_message)
            print(f"تم إرسال التنبيه بنجاح للطلب الخاص برقم: {phone}")
        except Exception as e:
            print(f"خطأ أثناء الإرسال للأدمن: {e}")
            
        return ConversationHandler.END
    else:
        await update.message.reply_text("رقم غير صالح. يرجى كتابة رقم هاتف مكوّن من 8 أرقام يبدأ بـ (2, 4, 5, 9):")
        return WAITING_PHONE

# أمر الإلغاء
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("تم إلغاء العملية.")
    return ConversationHandler.END

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            CallbackQueryHandler(button_handler, pattern="^new_order$"),
        ],
        states={
            WAITING_PHONE: [
                MessageHandler(filters.TEXT & (~filters.COMMAND), handle_phone)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("البوت يعمل الآن على السحابة...")
    app.run_polling()

if __name__ == "__main__":
    main()
