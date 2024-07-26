# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import Menu
from tkinter import ttk
from tkinter import Tk
import re
from tkinter.messagebox import showinfo
import pandas as pd
import csv
import matplotlib.pyplot as plt


class Application(tk.Tk):

    def __init__(self):
        super(Application, self).__init__()
        self.summ_result = {}

        root.title("Домашний бухгалтер")
        root.geometry("960x600")
        """Создаем меню"""
        main_menu = Menu()
        root.config(menu=main_menu)
        file_menu = Menu()
        # file_menu.add_command(label="Новый", command=self.creat_new_file)
        file_menu.add_command(label="Сохранить", command=self.save_button)
        file_menu.add_command(label="Открыть", command=self.open_file)
        file_menu.add_command(label="Помощь", command=self.help_info)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.exit_programm)
        main_menu.add_cascade(label="Файл", menu=file_menu)
        frame_info = ttk.Frame(root, borderwidth=1, padding=10)
        frame_info.pack(anchor="nw")
        lbl_data = ttk.Label(frame_info, text="Дата:")
        lbl_data.grid(row=1, column=0, columnspan=1, padx=30, ipadx=30, ipady=2)
        lbl_cost = ttk.Label(frame_info, text="Наименование затрат:")
        lbl_cost.grid(row=1, column=1, columnspan=1, padx=20, ipadx=15, ipady=2)
        lbl_money_cost = ttk.Label(frame_info, text="Стоимость траты:")
        lbl_money_cost.grid(row=1, column=2, columnspan=1, padx=5, ipadx=15, ipady=2)
        lbl_incomig = ttk.Label(frame_info, text="Приход:")
        lbl_incomig.grid(row=1, column=3, columnspan=1, padx=10, ipadx=20, ipady=2)
        """Создаем Фрэйм с полями ввода"""
        frame_entry = ttk.Frame(root, borderwidth=1, padding=10)
        frame_entry.pack(anchor="nw")
        """Прописываем поля ввода значений"""
        self.data_e = tk.StringVar()
        self.entry_data = ttk.Entry(frame_entry, width=20, textvariable=self.data_e)
        self.entry_data.grid(row=1, column=0, columnspan=1, padx=6)
        self.entry_data.insert(0, "ГГГГ-ММ-ЧЧ")

        self.cost_ = tk.StringVar()
        self.entry_cost = ttk.Entry(frame_entry, width=20, textvariable=self.cost_)
        self.entry_cost.grid(row=1, column=1, columnspan=1, padx=6)

        self.cost_money = tk.StringVar()
        self.entry_money_cost = ttk.Entry(frame_entry, width=20, textvariable=self.cost_money)
        self.entry_money_cost.focus()
        self.entry_money_cost.grid(row=1, column=2, columnspan=1, padx=6)

        self.income = tk.StringVar()
        self.entry_incoming = ttk.Entry(frame_entry, width=20, textvariable=self.income)
        self.entry_incoming.focus()
        self.entry_incoming.grid(row=1, column=3, columnspan=1, padx=6)
        """Создаем кнопку"""
        bttn0_save = ttk.Button(frame_entry, text="Сохранить",
                                command=self.save_button)
        bttn0_save.grid(row=1, column=4, columnspan=1, padx=6)
        bttn_draw = ttk.Button(frame_entry, text="Показать график", command=self.draw_graf)
        bttn_draw.grid(row=1, column=5, columnspan=1, padx=6)
        """Создаем текстовое поле"""
        self.text_pool = tk.Text(root, state='normal')
        self.text_pool.pack(fill='both', expand=1)


    def open_file(self):
        """Открываем имеющийся файл. Так как первоначально
        операции с данными проводятся в словаре, то тут
        создается словарь, который будет обновляться в других функциях,
         а в последствии записываться в файл."""
        with open('data.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            d_keys = []
            d_keys_res = []
            d_val = []
            for row in reader:
                d_val.append(row)
            d_keys.append(d_val[0])
            for kkey in range(len(d_keys[0])):
                d_keys_res.append(d_keys[0][kkey])
        for i in range(len(d_keys_res)):
            d_f = []
            # dict_0 = {}
            with open('data.csv') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    d_f.append(row[d_keys_res[i]])
                dict_0 = {d_keys_res[i]: d_f}
            self.summ_result.update(dict_0)
        show_read = pd.DataFrame(self.summ_result, index=['Дата', 'Стоимость траты', 'Приход', 'Баланс'])
        self.text_pool.insert('1.0', show_read)
        print("summ_result", self.summ_result)


    def save_button(self):
        self.text_pool.delete('1.0', 'end')
        data = self.data_e.get()
        cost = self.cost_.get()
        cost_money = self.cost_money.get()
        incoming = self.income.get()
        regular = re.compile(r"^[0-9]+\.[0-9]+$")
        reg_data = re.compile(r"^[12][09][0-9][0-9]\-[01][0-9]\-[0-9][0-9]$")
        print(regular.search(cost_money))
        print("summ_result in button_save", self.summ_result)
        if regular.search(cost_money) != None and regular.search(incoming) != None and reg_data.search(data) != None:
            row_result = {cost: [data, float(cost_money), float(incoming), (float(incoming) - float(cost_money))]}
            """Если словарь доходов не пустой то баланс считаем c учетом уже имеющихся данных"""
            if self.summ_result != {}:
                keys_sum = []
                for key in self.summ_result.keys():
                    keys_sum.append(key)
                balance = float(self.summ_result[keys_sum[-1]][3]) + float(incoming) - float(cost_money)
                row_result2 = {cost: [data, float(cost_money), float(incoming), balance]}
                self.summ_result.update(row_result2)
            else:
                self.summ_result.update(row_result)
        else:
            self.open_info()
        """Выводим результат в текстовое поле"""
        result_to_Text = pd.DataFrame(self.summ_result, index=['Дата', 'Стоимость траты', 'Приход', 'Баланс'])
        self.text_pool.insert('1.0', result_to_Text)
        """Сохраняем в файл"""
        self.save_to_file()


    def open_info(self):
        showinfo(title="ВНИМАНИЕ!", message='Введены недопустимые значения в '
                                             '"Приход" и "Стоимость" - должны быть цифры и точка.'
                                            'или неправильно введена дата (нарушен формат).')

    def help_info(self):
        showinfo(title="Как работает программа.", message="""В поля ввода вводите значения, 
        затем нажимаете 'Сохранить' и программа сразу записывает данные в файл data.cvs, 
        если он не существует, то она его создает. Программа позволяет накапливать информацию
        и делать общий график расходов-доходов. В поле 'Наименвание затрат' можно вводить
        любой текст, но желательно емко и коротко. В поля 'Стоимость траты' и 'Приход' вводятся
        только цифры в формате 'ЧЧЧЧЧ.ЧЧЧ' (разделитель дробной и целой части точка). Сохранение производится 
        правильно введенных значений. График строится либо после открытия файла с данными
        и нажатии кнопки 'Посмотреть график' или после сохранения всех введенных значений.
        ВНИМАНИЕ! После каждого ввода значений одной траты необходимо сохранять!""")

    def save_to_file(self):
        df = pd.DataFrame(self.summ_result)
        df.to_csv("data.csv", mode="w", index=False)

    def exit_programm(self):
        exit()

    def draw_graf(self):
        self.text_pool.delete('1.0', 'end')
        plt.style.use("classic")
        to_graf_1 = pd.DataFrame(self.summ_result, index=['Дата', 'Стоимость траты', 'Приход', 'Баланс']).T
        self.text_pool.insert('1.0', to_graf_1)
        to_graf_1['Стоимость траты'] = to_graf_1['Стоимость траты'].astype(float)
        to_graf_1['Приход'] = to_graf_1['Приход'].astype(float)
        to_graf_1['Баланс'] = to_graf_1['Баланс'].astype(float)
        to_graf_1.plot(title="Сводный график", xlabel="Наименвание затрат", ylabel="Средства")
        plt.show()


if __name__ == '__main__':
    root = Tk()
    app = Application()
    app.mainloop()
