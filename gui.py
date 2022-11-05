import tkinter as tk
from datetime import datetime
from tkinter import Label, Button, Entry, IntVar, StringVar, NORMAL
from tkinter.messagebox import askyesno, showinfo
from tkinter.ttk import Combobox

from mail import send_email

months = ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь',
          'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь']

month = months[datetime.today().month - 1]
year = datetime.today().year


def displays_message(dict_data):
    label = f'''
            Месяц:  {dict_data['месяц']}
            Год:    {dict_data['год']}
            T1:     {dict_data['T1']}
            T2:     {dict_data['T2']}
            T3:     {dict_data['T3']}
    '''
    return askyesno(title='Отправить показания?', message=label)


class Example(tk.Tk):

    def __init__(self):
        super().__init__()
        self.center_window()

        self.title('Показания электрического счетчика')
        Label(self, text='Введите показания:', font=('Arial', 24, 'bold')).grid(row=0, column=0,
                                                                                columnspan=4,
                                                                                sticky='we')

        Label(self, text='Месяц:', font=('Arial', 18, 'bold')).grid(row=1, column=0, padx=10, pady=10)

        self.var_month = StringVar()
        self.var_month.set(month)
        Combobox(self, values=months, textvariable=self.var_month, state='readonly', font=('Arial', 16),
                 width=10).grid(row=1, column=1)

        Label(self, text='Год:', font=('Arial', 18, 'bold')).grid(row=1, column=2, padx=5, pady=10)

        self.var_year = IntVar()
        self.var_year.set(year)
        Entry(self, textvariable=self.var_year, justify='center', font=('Arial', 18),
              width=10).grid(row=1, column=3)

        Label(self, text='T1:', font=('Arial', 18, 'bold')).grid(row=2, column=0, padx=10, pady=10,
                                                                 sticky='we')
        self.var_t1 = IntVar()
        Entry(self, textvariable=self.var_t1, font=('Arial', 18), justify='center').grid(row=2, column=1,
                                                                                         padx=10, pady=10,
                                                                                         columnspan=3)

        Label(self, text='T2:', font=('Arial', 18, 'bold')).grid(row=3, column=0, padx=10, pady=10)

        self.var_t2 = IntVar()
        Entry(self, textvariable=self.var_t2, font=('Arial', 18), justify='center').grid(row=3, column=1,
                                                                                         padx=10, pady=10,
                                                                                         columnspan=3)

        Label(self, text='T3:', font=('Arial', 18, 'bold')).grid(row=4, column=0, padx=10, pady=10)
        self.var_t3 = IntVar()
        Entry(self, textvariable=self.var_t3, font=('Arial', 18), justify='center').grid(row=4, column=1,
                                                                                         padx=10, pady=10,
                                                                                         columnspan=3)

        self.but = Button(self, text='Отправить', command=self.on_click, state=NORMAL,
                          font=('Arial', 24, 'bold'))
        self.but.grid(row=5, column=0, columnspan=4, padx=10, pady=5, sticky='we')

    def center_window(self, w=460, h=350) -> None:
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()

        x = (sw - w) / 2
        y = (sh - h) / 2
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def on_click(self):
        dict_data = {'месяц': self.var_month.get(),
                     'год': self.var_year.get(),
                     'T1': self.var_t1.get(),
                     'T2': self.var_t2.get(),
                     'T3': self.var_t3.get()}

        if displays_message(dict_data):
            self.del_button_set_label()
            self.update()
            self.sent_mail(dict_data)

    def del_button_set_label(self):
        self.but.destroy()
        Label(self, text='ОТПРАВЛЯЕТСЯ', font=('Arial', 32, 'bold')).grid(row=5, column=0,
                                                                          columnspan=4, padx=10,
                                                                          pady=15, sticky='we')

    def sent_mail(self, dict_data):
        # send_email() - отправка почты
        resoult = send_email(dict_data['месяц'],
                             dict_data['год'],
                             dict_data['T1'],
                             dict_data['T2'],
                             dict_data['T3'])
        self.displays_message_sent(resoult)

    def displays_message_sent(self, text):
        showinfo('Информация', text)
        self.quit()


def main():
    app = Example()
    app.mainloop()


if __name__ == "__main__":
    main()
