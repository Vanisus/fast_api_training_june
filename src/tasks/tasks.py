import ssl
import smtplib
import logging
from email.message import EmailMessage
from celery import Celery
from config import SMTP_USER, SMTP_PASSWORD

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587  # Порт для TLS

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

celery = Celery('tasks', broker='redis://localhost:6379')


def get_email_template_dashboard(username: str):
    email = EmailMessage()
    email['Subject'] = 'Натрейдил Отчет Дашборд'
    email['From'] = SMTP_USER
    email['To'] = SMTP_USER

    email.set_content(
        '<div>'
        f'<h1 style="color: red;">Здравствуйте, {username}, а вот и ваш отчет. Зацените 😊</h1>'
        '<img src="https://static.vecteezy.com/system/resources/previews/008/295/031/original/custom-relationship'
        '-management-dashboard-ui-design-template-suitable-designing-application-for-android-and-ios-clean-style-app'
        '-mobile-free-vector.jpg" width="600">'
        '</div>',
        subtype='html'
    )
    return email


@celery.task
def send_email_report_dashboard(username: str):
    try:
        email = get_email_template_dashboard(username)
        context = ssl.create_default_context()
        logger.debug("Создаем SSL-контекст")

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            logger.debug("Устанавливаем соединение с SMTP сервером")
            server.set_debuglevel(1)  # Включение отладочного вывода
            server.starttls(context=context)
            logger.debug("Начинаем TLS")
            server.login(SMTP_USER, SMTP_PASSWORD)
            logger.debug("Проходим аутентификацию")
            server.send_message(email)
            logger.debug("Сообщение отправлено")
    except Exception as e:
        logger.error("Ошибка при отправке email: %s", e)
