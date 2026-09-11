from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ConversationHandler,
    filters,
    ContextTypes,
)

# معرف حسابك الشخصي لاستقبال الإشعارات
ADMIN_CHAT_ID = 1765522064

# مراحل المحادثة
WAITING_PHONE = 1

# القائمة الرئيسية
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📶 المشغل", callback_data='menu_operators')],
        [InlineKeyboardButton("🛠️ الدعم", callback_data='support')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = "مرحباً بك في Malik-Store 👋\nيرجى اختيار القسم المناسب من القائمة أدناه:"

    if update.message:
        await update.message.reply_text(text, reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.message.edit_text(text, reply_markup=reply_markup)

    return ConversationHandler.END

# التعامل مع الأزرار
async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # قائمة المشغلين
    if data == 'menu_operators':
        keyboard = [
            [InlineKeyboardButton("🔴 أوريدو (Ooredoo)", callback_data='op_ooredoo')],
            [InlineKeyboardButton("🟠 أورونج (Orange)", callback_data='op_orange')],
            [InlineKeyboardButton("🔵 تيليكوم (TT)", callback_data='op_telecom')],
            [InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data='back_home')]
        ]
        await query.edit_message_text("اختر المشغل الخاص بك:", reply_markup=InlineKeyboardMarkup(keyboard))
        return ConversationHandler.END

    # باقات أوريدو
    elif data == 'op_ooredoo':
        keyboard = [
            [InlineKeyboardButton("1 GO - 5 DT", callback_data='pkg_أوريدو 1GO (5DT)'), InlineKeyboardButton("4 GO - 12 DT", callback_data='pkg_أوريدو 4GO (12DT)')],
            [InlineKeyboardButton("25 GO - 30 DT", callback_data='pkg_أوريدو 25GO (30DT)')],
            [InlineKeyboardButton("100 GO - 80 DT", callback_data='pkg_أوريدو 100GO (80DT)'), InlineKeyboardButton("200 GO - 100 DT", callback_data='pkg_أوريدو 200GO (100DT)')],
            [InlineKeyboardButton("🔙 رجوع للمشغلين", callback_data='menu_operators')]
        ]
        await query.edit_message_text("🔴 باقات وأسعار أوريدو (Ooredoo):", reply_markup=InlineKeyboardMarkup(keyboard))
        return ConversationHandler.END

    # باقات أورونج
    elif data == 'op_orange':
        keyboard = [
            [InlineKeyboardButton("1 GO - 5 DT", callback_data='pkg_أورونج 1GO (5DT)'), InlineKeyboardButton("4 GO - 12 DT", callback_data='pkg_أورونج 4GO (12DT)')],
            [InlineKeyboardButton("25 GO - 30 DT", callback_data='pkg_أورونج 25GO (30DT)'), InlineKeyboardButton("30 GO - 35 DT", callback_data='pkg_أورونج 30GO (35DT)')],
            [InlineKeyboardButton("100 GO - 80 DT", callback_data='pkg_أورونج 100GO (80DT)'), InlineKeyboardButton("200 GO - 100 DT", callback_data='pkg_أورونج 200GO (100DT)')],
            [InlineKeyboardButton("🔙 رجوع للمشغلين", callback_data='menu_operators')]
        ]
        await query.edit_message_text("🟠 باقات وأسعار أورونج (Orange):", reply_markup=InlineKeyboardMarkup(keyboard))
        return ConversationHandler.END

    # باقات تيليكوم
    elif data == 'op_telecom':
        keyboard = [
            [InlineKeyboardButton("1 GO - 5 DT", callback_data='pkg_تيليكوم 1GO (5DT)'), InlineKeyboardButton("4 GO - 12 DT", callback_data='pkg_تيليكوم 4GO (12DT)')],
            [InlineKeyboardButton("25 GO - 30 DT", callback_data='pkg_تيليكوم 25GO (30DT)')],
            [InlineKeyboardButton("🔙 رجوع للمشغلين", callback_data='menu_operators')]
        ]
        await query.edit_message_text("🔵 باقات وأسعار تيليكوم (TT):", reply_markup=InlineKeyboardMarkup(keyboard))
        return ConversationHandler.END

    # اختيار الباقة وحفظها
    elif data.startswith('pkg_'):
        selected_pkg = data.replace('pkg_', '')
        context.user_data['selected_package'] = selected_pkg

        await query.edit_message_text(
            f"✅ لقد اخترت: {selected_pkg}\n\n"
            "📱 الرجاء الآن كتابة رقم الهاتف الذي تريد إرسال الرصيد إليه:"
        )
        return WAITING_PHONE

    # الدعم الفني
    elif data == 'support':
        keyboard = [[InlineKeyboardButton("🔙 رجوع للقائمة الرئيسية", callback_data='back_home')]]
        await query.edit_message_text(
            "🛠️ الدعم الفني:\nلأي استفسار أو مساعدة بخصوص الخدمات، يرجى التواصل مع المسؤول مباشرة.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return ConversationHandler.END

    # الرجوع للقائمة الرئيسية
    elif data == 'back_home':
        await start(update, context)
        return ConversationHandler.END

# استقبال رقم الهاتف وإرسال التنبيه
async def receive_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone_number = update.message.text.strip()
    selected_pkg = context.user_data.get('selected_package', 'غير محددة')
    user = update.effective_user
    username = f"@{user.username}" if user.username else "بدون معرف"

    # رسالة التأكيد للزبون
    keyboard = [[InlineKeyboardButton("🔙 العودة للقائمة الرئيسية", callback_data='back_home')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"🎉 تم تسجيل طلبك بنجاح!\n\n"
        f"📦 الباقة: {selected_pkg}\n"
        f"📱 رقم الهاتف: {phone_number}\n\n"
        f"⏳ سيتم إرسال الرصيد إلى الرقم فور إتمام المعالجة.",
        reply_markup=reply_markup
    )

    # إرسال التنبيه إلى حسابك الشخصي
    admin_alert = (
        f"🔔 طلب إنترنت جديد وارد!\n\n"
        f"👤 الزبون: {user.first_name} ({username})\n"
        f"🆔 معرف الزبون: {user.id}\n"
        f"📦 الباقة: {selected_pkg}\n"
        f"📱 رقم الهاتف: {phone_number}"
    )

    try:
        await context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=admin_alert
        )
        print(f"تم إرسال التنبيه بنجاح للطلب الخاص برقم: {phone_number}")
    except Exception as e:
        print(f"خطأ أثناء إرسال التنبيه للمشرف: {e}")

    return ConversationHandler.END

if __name__ == '__main__':
    TOKEN = "8759526020:AAEORGrmhQJ3qF3wWesrx-oujNdtPkfZa1I"

    app = (
        ApplicationBuilder()
        .token(TOKEN)
        .proxy("http://proxy.server:3128")
        .get_updates_proxy("http://proxy.server:3128")
        .build()
    )

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            CallbackQueryHandler(button_click)
        ],
        states={
            WAITING_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_phone)]
        },
        fallbacks=[
            CommandHandler("start", start),
            CallbackQueryHandler(button_click)
        ],
        allow_reentry=True
    )

    app.add_handler(conv_handler)

    print("البوت بدأ العمل بنجاح مع استقبال التنبيهات...")
    app.run_polling()
