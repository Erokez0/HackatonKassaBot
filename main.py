import telebot
from Request import get_qr_status, reg_test_qr
from Keys import TelegramBotKey


bot = telebot.TeleBot(TelegramBotKey)
bot.set_webhook()
state: int = 0

qr_possible_statuses: dict[str:str] = {"NEW": "Заказ не оплачен  ❌",
                                       "IN_PROGRESS": "Заказ в процессе оплаты ❌",
                                       "CANCELLED": "Заказ отменён  ❌",
                                       "EXPIRED": "Заказ устарел  ❌",
                                       "PAID": "Заказ оплачен  ✅"}


@bot.message_handler(commands=['qr_reg'])
def qr_reg_test(message) -> None:
    """
    Регистрирует QR-кода для тестировки и отправляет пользователю qrId и qrUrl
    :param message: Сообщение ТГ
    :return: Ничего
    """
    rdict: dict = reg_test_qr()
    bot.send_message(message.chat.id, f"QRID:\n{rdict.get('qrId')}\nQRURL:\n{rdict.get('qrUrl')}")


def get_status(nomer_zakaza: str) -> str:
    """
    Получает статус заказа по qrId
    :param nomer_zakaza: qrId
    :return: Строка с отформатированным статусом оплаты
    """

    if get_qr_status(nomer_zakaza) in qr_possible_statuses:
        return qr_possible_statuses.get(get_qr_status(nomer_zakaza))
    else:
        return "Заказ не действителен ❌"


@bot.message_handler(commands=['start', 'help'])
def start_message(message) -> None:
    """
    Стартовое сообщение
    :param message: Сообщение ТГ
    :return: Ничего
    """
    bot.send_message(message.chat.id, "<b>Как пользоваться ботом?</b> \n\n"
                                      "1. Нажать /get_status\n"
                                      "2. Отправить ID QR-кода транзакции\n", parse_mode="HTML")


@bot.message_handler(commands=['get_status'])
def get_status_to_get_nomer(message) -> None:
    """
    Получает статус
    :param message: Сообщение ТГ
    :return: Ничего
    """
    global state
    state = 1
    bot.send_message(message.chat.id, "Введите номер заказа")


@bot.message_handler(content_types=['text', 'help'])
def get_status_to_user(message) -> None:
    """
    Отправляет статус оплаты пользователю
    :param message: Сообщение ТГ
    :return: Ничего
    """
    global state
    if state == 1:
        bot.send_message(message.chat.id, get_status(message.text))
        state = 0


bot.infinity_polling()
