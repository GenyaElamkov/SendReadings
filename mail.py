import smtplib
import ssl
from email.mime.text import MIMEText
from email.utils import formataddr, make_msgid
from string import Template
import imaplib
from time import sleep
import configparser

config = configparser.ConfigParser()
config.read('settings.ini', encoding='utf-8')

from_mail = config['EMAIL_FROM']['FROM_MAIL']  # Почта отправителя.
password = config['EMAIL_FROM']['PASSWORD']  # Пароль отправителя.
sender_name = config['EMAIL_FROM']['SENDER_NAME']  # Отображение имени отправителя рядом с почтой.

to_mail = config['EMAIL_TO']['TO_MAIL']  # Почта принимающая.
recipient_name = config['EMAIL_TO']['RECIPIENT_NAME']  # Отображение имени почты кому приходит письмо.

host_smtp = config['SMTP_SSL']['HOST_SMTP']  # Хост для исходящий сообщений.
port = int(config['SMTP_SSL']['PORT'])  # Порт для исходящих сообщений.

subject = config['SUBJECT']['SUBJECT']  # Тема письма.

# # For read mail.
imap_server = config['IMAP']['IMAP_SERVER']  # Хост для входящий сообщений.
# port_out = config['IMAP']['PORT_OUT']  # Порт для входящих сообщений.


def send_email(month: str, year: int, t1: int, t2: int, t3: int) -> str:
    """Sent mail"""
    # SMTP
    # s = smtplib.SMTP(host_smtp, port)
    # s.starttls()
    context = ssl.create_default_context()

    try:
        with open('template.html', encoding='utf-8') as file:
            template = file.read()
            set_code_template = Template(template).safe_substitute(month=month, year=year, t1=t1, t2=t2, t3=t3)

    except IOError:
        return "Файл шаблона не найден!"

    try:
        # SMTP
        # s.login(from_mail, password)
        # s.set_debuglevel(1)

        # SSL
        with smtplib.SMTP_SSL(host_smtp, port, context=context) as s:
            s.login(from_mail, password)
            # Включение Дебагера.
            # s.set_debuglevel(1)
            msg = MIMEText(set_code_template, 'html')

            # recipients - Email рассылка,
            # from_mail - присылаем себе для дальнейшего сохранения в Send.
            recipients = [to_mail, from_mail]

            # Без паузы отправляет сообщения.
            # msg['To'] = formataddr((recipient_name, ','.join(recipients)))
            # msg['Subject'] = subject
            # msg['Message-ID'] = make_msgid()
            # s.sendmail(from_mail, recipients, msg.as_string())

            # Добавляет паузу между отправку сообщений на разные адреса.
            for email in recipients:
                msg['From'] = formataddr((sender_name, from_mail))
                msg['To'] = formataddr((recipient_name, email))
                msg['Subject'] = subject
                msg['Message-ID'] = make_msgid()
                s.sendmail(from_mail, email, msg.as_string())
                sleep(3)

        save_email_send(imap_server, from_mail, password)

        return 'Сообщение отправлено успешно!'
    except Exception as _ex:
        return f"{_ex}\nПожалуйста, проверьте свой логин или пароль!"


def save_email_send(imap_server: str, from_mail: str, password: str) -> None:
    """Save mail"""
    imap = imaplib.IMAP4_SSL(imap_server)
    imap.login(from_mail, password)

    imap.select('INBOX', readonly=False)
    result, data = imap.search(None, 'ALL')
    ids = data[0]

    id_list = ids.split()
    copy_res = imap.copy(id_list[-1], 'Sent')

    if copy_res[0] == 'OK':
        imap.store(id_list[-1], '+FLAGS', '\\Deleted')
        imap.expunge()


def main():
    month = 'октябрь'
    year = 2022
    t1 = 4545
    t2 = 3148
    t3 = 10299
    out = send_email(month, year, t1, t2, t3)
    print(out)
    # save_email_send(imap_server, from_mail, password)


if __name__ == '__main__':
    main()
