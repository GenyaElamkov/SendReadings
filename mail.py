# import imaplib
# import time
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from config import *
from string import Template

from_addr = FROM_MAIL  # Почта отправителя.
to_addrs = TO_MAIL  # Почта принимающая.
password = PASSWORD  # Пароль отправителя.
host_smtp = HOST_SMTP  # Хост для исходящий сообщений.
port = PORT  # Порт для исходящих сообщений.
sender_name = SENDER_NAME  # Отображение имени отправителя рядом с почтой.
recipient_name = RECIPIENT_NAME  # Отображение имени почты кому приходит письмо.
subject = SUBJECT  # Тема письма.


# Сохранение не работает.
# mail_host_out = MAIL_HOST_OUT   # Хост для входящий сообщений.
# port_out = PORT_OUT             # Порт для входящих сообщений.

def send_email(month: str, year: int, t1: int, t2: int, t3: int) -> str:
    s = smtplib.SMTP(host_smtp, port)
    s.starttls()

    try:
        with open('template.html', encoding='utf-8') as file:
            template = file.read()
            set_code_template = Template(template).safe_substitute(month=month, year=year,
                                                                   t1=t1, t2=t2, t3=t3)
    except IOError:
        return "The template file doesn't found!"

    try:
        s.login(from_addr, password)
        msg = MIMEText(set_code_template, 'html')
        msg['From'] = formataddr((sender_name, from_addr))
        msg['To'] = formataddr((recipient_name, to_addrs))
        msg['Subject'] = subject
        s.sendmail(from_addr, to_addrs, msg.as_string())

        # Не работает, выводит ошибку с encoding
        # text = msg.as_string()

        # imap = imaplib.IMAP4_SSL(mail_host_out, port_out)
        # imap.login(from_addr, password)
        # imap.append('Входящие', 'Отправленные', imaplib.Time2Internaldate(time.time()),
        #             text.encode('utf-8'))
        # imap.logout()

        return 'Сообщение отправлено успешно!'
    except Exception as _ex:
        return f"{_ex}\nПожалуйста, проверьте свой логин или пароль!"


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
