import math
import config
import threading
import customtkinter as ctk
from tkinter import messagebox as mb
from generator import generate_dataset

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

ctk.set_widget_scaling(0.7)
ctk.set_window_scaling(0.7)


def threaded_run_generator():
    t = threading.Thread(target=run_generator)
    t.start()


def run_generator():
    N = int(N_entry.get())

    weights_ru_operators = [float(op_weight.get()) for op_weight in operator_weights_entries]
    operator_weights_spb = [float(spb_weight.get()) for spb_weight in spb_weights_entries]
    weights_job_titles = [float(job_weight.get()) for job_weight in job_weights_entries]

    WEIGHTS_FOR_RU_OPERATORS = dict(zip(config.OPERATOR_RU_CODES.keys(), weights_ru_operators))

    if not math.isclose(sum(WEIGHTS_FOR_RU_OPERATORS.values()), 1.0):
        for entry in operator_weights_entries:
            entry.configure(fg_color='red')
        mb.showerror('Ошибка', 'Сумма вероятностей выбора всех операторов должна быть 1')
        return
    else:
        for entry in operator_weights_entries:
            entry.configure(fg_color='#343638')

    OPERATOR_WEIGHTS_FOR_SPB = dict(zip(config.OPERATOR_RU_CODES.keys(), operator_weights_spb))

    i = 0
    for value in OPERATOR_WEIGHTS_FOR_SPB.values():
        if value > 1.0:
            for num, entry in enumerate(spb_weights_entries):
                if num == i:
                    entry.configure(fg_color='red')
                    mb.showerror('Ошибка', 'Сумма каждой вероятности выбора внутренного регионального кода поставщика услуг должен быть от 0 до 1')
                    return
        else:
            for entry in spb_weights_entries:
                entry.configure(fg_color='#343638')
        i += 1

    WEIGHTS_FOR_JOB_TITLES = dict(zip(config.WEIGHTS_FOR_JOB_TITLES.keys(), weights_job_titles))

    if not math.isclose(
            WEIGHTS_FOR_JOB_TITLES['Охранник'] + WEIGHTS_FOR_JOB_TITLES['Уборщик'] + WEIGHTS_FOR_JOB_TITLES['Комендант'] + WEIGHTS_FOR_JOB_TITLES[
                'Продавец'], 0.2):
        for num, entry in enumerate(job_weights_entries):
            if 2 <= num <= 5:
                entry.configure(fg_color='red')
        mb.showerror('Ошибка', 'Сумма вероятностей выбора Охранника, Уборщика, Коменданта, Продавца должна быть 0.2')
        return
    else:
        for entry in job_weights_entries:
            entry.configure(fg_color='#343638')

    if not math.isclose(
            WEIGHTS_FOR_JOB_TITLES['Программист'] + WEIGHTS_FOR_JOB_TITLES['Инженер'] + WEIGHTS_FOR_JOB_TITLES['Медик'] + WEIGHTS_FOR_JOB_TITLES[
                'Маркетолог'], 0.4):
        for num, entry in enumerate(job_weights_entries):
            if 8 <= num <= 11:
                entry.configure(fg_color='red')
        mb.showerror('Ошибка', 'Сумма вероятностей выбора Программиста, Инженера, Медика, Маркетолога должна быть 0.4')
        return
    else:
        for entry in job_weights_entries:
            entry.configure(fg_color='#343638')

    status_label.configure(text='Генерация...', text_color='white')
    generate_dataset(N, status_label, WEIGHTS_FOR_RU_OPERATORS, OPERATOR_WEIGHTS_FOR_SPB, WEIGHTS_FOR_JOB_TITLES)


root = ctk.CTk()
root.title('Генератор данных')

frame_n = ctk.CTkFrame(root)
frame_n.grid(row=0, column=1, padx=10, pady=10)

N_label = ctk.CTkLabel(frame_n, text="Введите число N")
N_label.pack()
N_entry = ctk.CTkEntry(frame_n, justify='center')
N_entry.insert(0, '50000')
N_entry.pack()

# Frame for settings WEIGHTS_FOR_RU_OPERATORS
frame_ru_operators = ctk.CTkFrame(root)
frame_ru_operators.grid(row=1, column=0, padx=10, pady=10, sticky='n')

weights_ru_operators_label = ctk.CTkLabel(frame_ru_operators, text='Настройка вероятности \nвыбора кода поставщика услуг', justify='center')
weights_ru_operators_label.pack()

operator_weights_entries = []
for operator, weight in config.WEIGHTS_FOR_RU_OPERATORS.items():
    op_label = ctk.CTkLabel(frame_ru_operators, text=operator)
    op_label.pack()
    op_entry = ctk.CTkEntry(frame_ru_operators, justify='center')
    op_entry.insert(0, weight)
    op_entry.pack()
    operator_weights_entries.append(op_entry)

# Frame for settings OPERATOR_WEIGHTS_FOR_SPB
frame_spb_weights = ctk.CTkFrame(root)
frame_spb_weights.grid(row=1, column=1, padx=5, pady=5, sticky='n')

operator_weights_spb_label = ctk.CTkLabel(frame_spb_weights, text='Настройка вероятности внутреннего \nрегионального кода поставщика услуг',
                                          justify='center')
operator_weights_spb_label.pack()

spb_weights_entries = []
for operator, weight in config.OPERATOR_WEIGHTS_FOR_SPB.items():
    spb_label = ctk.CTkLabel(frame_spb_weights, text=operator)
    spb_label.pack()
    spb_entry = ctk.CTkEntry(frame_spb_weights, justify='center')
    spb_entry.insert(0, weight)
    spb_entry.pack()
    spb_weights_entries.append(spb_entry)

# Frame for settings WEIGHTS_FOR_JOB_TITLES
frame_job_titles = ctk.CTkFrame(root, fg_color='black')
frame_job_titles.grid(row=1, column=2, padx=10, pady=10, sticky='n')

weights_job_titles_label = ctk.CTkLabel(frame_job_titles, text='Настройки вероятности выбора профессий', justify='center')
weights_job_titles_label.pack()

job_weights_entries = []
for job_title, weight in config.WEIGHTS_FOR_JOB_TITLES.items():
    job_label = ctk.CTkLabel(frame_job_titles, text=job_title)
    job_label.pack()
    job_entry = ctk.CTkEntry(frame_job_titles, justify='center')
    job_entry.insert(0, weight)
    job_entry.pack()
    job_weights_entries.append(job_entry)

text_under_col1 = 'Сумма вероятностей выбора всех операторов должна быть 1\nСумма каждой вероятности выбора внутренного регионального кода ' \
                  'поставщика ' \
                  'услуг должен быть от 0 до 1\nСумма вероятностей выбора Охранника, Уборщика, Коменданта, Продавца должна быть 0.2\nСумма ' \
                  'вероятностей выбора Программиста, Инженера, Медика, Маркетолога должна быть 0.4'
label_under_col1 = ctk.CTkLabel(root, text=text_under_col1)
label_under_col1.grid(row=3, column=1, padx=10, pady=10)
default_color = label_under_col1.cget('fg_color')
frame_n.configure(fg_color=default_color)
frame_job_titles.configure(fg_color=default_color)
frame_ru_operators.configure(fg_color=default_color)
frame_spb_weights.configure(fg_color=default_color)

# Button for generation data
generate_button = ctk.CTkButton(root, text='Генерировать данные', command=threaded_run_generator)
generate_button.grid(row=4, column=1, padx=10, pady=10)

status_label = ctk.CTkLabel(root, text="")
status_label.grid(row=5, column=1, pady=10, padx=10)

root.mainloop()
