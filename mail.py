import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from config import *
from string import Template
import imaplib
from time import sleep

from_mail = FROM_MAIL  # Почта отправителя.
to_mail = TO_MAIL  # Почта принимающая.
password = PASSWORD  # Пароль отправителя.
host_smtp = HOST_SMTP  # Хост для исходящий сообщений.
port = PORT  # Порт для исходящих сообщений.
sender_name = SENDER_NAME  # Отображение имени отправителя рядом с почтой.
recipient_name = RECIPIENT_NAME  # Отображение имени почты кому приходит письмо.
subject = SUBJECT  # Тема письма.

# Сохранение не работает.
imap_server = IMAP_SERVER  # Хост для входящий сообщений.
port_out = PORT_OUT  # Порт для входящих сообщений.


def send_email(month: str, year: int, t1: int, t2: int, t3: int) -> str:
    s = smtplib.SMTP(host_smtp, port)
    s.starttls()

    try:
        with open('template.html', encoding='utf-8') as file:
            template = file.read()
            set_code_template = Template(template).safe_substitute(month=month, year=year,
                                                                   t1=t1, t2=t2, t3=t3)
    except IOError:
        return "Файл шаблона не найден!"

    try:
        s.login(from_mail, password)
        s.set_debuglevel(1)
        msg = MIMEText(set_code_template, 'html')
        msg['From'] = formataddr((sender_name, from_mail))

        # recipients - Email рассылка,
        # from_mail - присылаем себе для дальнейшего сохранения в Send.
        recipients = [to_mail, from_mail]
        for email in recipients:
            # msg['To'] = formataddr((recipient_name, ','.join(recipients)))
            msg['To'] = formataddr((recipient_name, email))
            msg['Subject'] = subject
            s.sendmail(from_mail, email, msg.as_string())
            sleep(5)

        save_email_send(imap_server, from_mail, password)
        return 'Сообщение отправлено успешно!'
    except Exception as _ex:
        return f"{_ex}\nПожалуйста, проверьте свой логин или пароль!"


def save_email_send(imap_server: str, from_mail: str, password: str) -> None:
    imap = imaplib.IMAP4_SSL(imap_server)
    imap.login(from_mail, password)
    imap.list()
    imap.select('Inbox', readonly=False)
    result, data = imap.search(None, 'ALL')
    ids = data[0]
    id_list = ids.split()

    copy_res = imap.copy(id_list[0], 'Sent')
    if copy_res[0] == 'OK':
        delete_res = imap.store(id_list[0], '+FLAGS', '\\Deleted')
        imap.expunge()


def main():
    month = 'октябрь'
    year = 2022
    t1 = 4545
    t2 = 3148
    t3 = 10299
    out = send_email(month, year, t1, t2, t3)
    print(out)


if __name__ == '__main__':
    main()
