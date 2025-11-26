.. _versions:
.. _branchstatus:import csv
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler

CHOOSING_SERVICE, GET_QUANTITY, GET_LINK, CONFIRM_ORDER, GET_PAYMENT_NUMBER = range(5)

services = {
    "متابعين تيك توك": {"1k": 150},
    "لايكات تيك توك": {"1k": 30, "10k": 250},
    "مشاهدات تيك توك": {"10k": 20, "50k": 85, "100k": 150},
    "حفظ تيك توك": {"1k": 15},
    "اكسبلور تيك توك": {"1k": 20},
    "تعليقات تيك توك": {"10 مصري": 30, "100 أجنبي": 50}
}

order = {}

# رقمك في تيليجرام عشان توصلك إشعارات بالطلبات الجديدة
ADMIN_CHAT_ID = 7220556029

def save_order(order_data):
    with open('orders.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([
            order_data['service'], order_data['quantity'], order_data['link'], order_data['payment_number']
        ])

def start(update: Update, context: CallbackContext) -> int:
    keyboard = [list(services.keys())]
    update.message.reply_text(
        "أهلاً بك في ميسو استور لخدمات تيك توك!\n"
        "اختار الخدمة اللي عايزها:",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    )
    return CHOOSING_SERVICE

def choosing_service(update: Update, context: CallbackContext) -> int:
    service = update.message.text
    if service not in services:
        update.message.reply_text("من فضلك اختر خدمة صحيحة.")
        return CHOOSING_SERVICE

    order['service'] = service
    options = "\n".join([f"{qty} = {price} ج" for qty, price in services[service].items()])
    update.message.reply_text(
        f"اختر الكمية:\n{options}\n\nاكتب الكمية (مثلاً 1k أو 10k):"
    )
    return GET_QUANTITY

def get_quantity(update: Update, context: CallbackContext) -> int:
    quantity = update.message.text
    service = order['service']

    if quantity not in services[service]:
        update.message.reply_text("الكمية غير متوفرة، حاول تاني.")
        return GET_QUANTITY

    order['quantity'] = quantity
    update.message.reply_text(f"أدخل رابط الفيديو أو الحساب الخاص بالخدمة ({service}):")
    return GET_LINK

def get_link(update: Update, context: CallbackContext) -> int:
    order['link'] = update.message.text
    service = order['service']
    quantity = order['quantity']
    price = services[service][quantity]
    summary = (
        f"طلبك:\n"
        f"الخدمة: {service}\n"
        f"الكمية: {quantity}\n"
        f"الرابط: {order['link']}\n"
        f"السعر: {price} ج\n\n"
        f"هل تريد تأكيد الطلب؟ (نعم / لا)"
    )
    update.message.reply_text(summary)
    return CONFIRM_ORDER

def confirm_order(update: Update, context: CallbackContext) -> int:
    answer = update.message.text.lower()
    if answer == 'نعم':
        update.message.reply_text(
            "تمام، ادخل رقم فودافون كاش أو رقم الدفع اللي هتدفع منه:"
        )
        return GET_PAYMENT_NUMBER
    elif answer == 'لا':
        update.message.reply_text("تم إلغاء الطلب. إذا أردت طلب آخر ارسل /start.")
        return ConversationHandler.END
    else:
        update.message.reply_text("من فضلك اكتب نعم أو لا.")
        return CONFIRM_ORDER

def get_payment_number(update: Update, context: CallbackContext) -> int:
    payment_number = update.message.text
    order['payment_number'] = payment_number

    save_order(order)

    update.message.reply_text(
        "شكراً لطلبك! سيتم التواصل معك قريباً لتأكيد الدفع والمتابعة.\n\n"
        "ممكن تبعت لنا صورة إثبات الدفع في المحادثة."
    )

    context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=(
            f"طلب جديد:\n"
            f"الخدمة: {order['service']}\n"
            f"الكمية: {order['quantity']}\n"
            f"الرابط: {order['link']}\n"
            f"رقم الدفع: {payment_number}\n"
            f"السعر: {services[order['service']][order['quantity']]} ج"
        )
    )
    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("تم إلغاء العملية. تقدر تبدأ من جديد بكتابة /start")
    return ConversationHandler.END

def main():
    updater = Updater("8408770109:AAFtulDhB8VgknG-mwaUM_LeCv4YG8jCeLY")

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING_SERVICE: [MessageHandler(Filters.text & ~Filters.command, choosing_service)],
            GET_QUANTITY: [MessageHandler(Filters.text & ~Filters.command, get_quantity)],
            GET_LINK: [MessageHandler(Filters.text & ~Filters.command, get_link)],
            CONFIRM_ORDER: [MessageHandler(Filters.text & ~Filters.command, confirm_order)],
            GET_PAYMENT_NUMBER: [MessageHandler(Filters.text & ~Filters.command, get_payment_number)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher = updater.dispatcher
    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

=========================
Status of Python versions
=========================

The ``main`` branch is currently the future Python |main_version|, and is the only
branch that accepts new features.  The latest release for each Python
version can be found on the `download page <https://www.python.org/downloads/>`_.


.. raw:: html
   :file: include/release-cycle.svg

(See :ref:`below <full-chart>` for a chart with older versions.
Another useful visualization is `endoflife.date/python <https://endoflife.date/python>`_.)


Supported versions
==================

Dates shown in *italic* are scheduled and can be adjusted.

.. csv-table::
   :header-rows: 1
   :width: 100%
   :file: include/branches.csv

.. Remember to update main branch in the paragraph above too


Unsupported versions
====================

.. csv-table::
   :header-rows: 1
   :width: 100%
   :file: include/end-of-life.csv


.. _full-chart:

Full chart
==========

.. raw:: html
   :file: include/release-cycle-all.svg


Status key
==========

Python releases go through five phases, as described in :pep:`602`.  Release
managers can adjust specific dates as needed.

:feature: Before the first beta, the next full release can accept new features,
   bug fixes, and security fixes.

:prerelease: After the first beta, no new features can go in, but feature fixes
   (including significant changes to new features), bug fixes, and security fixes
   are accepted for the upcoming feature release.

:bugfix: Once a version has been fully released, bug fixes and security fixes are
   accepted. New binaries are built and released roughly every two months. This
   phase is also called **maintenance** mode or **stable** release.

:security: After two years (18 months for versions before 3.13), only security
   fixes are accepted and no more binaries are released.  New source-only versions
   can be released as needed.

:end-of-life: Five years after a release, support ends. The release cycle is
   frozen; no further changes are allowed.

See also the :ref:`devcycle` page for more information about branches and backporting.
   
