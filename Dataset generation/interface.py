import config
import tkinter as tk
from tkinter import ttk
from generator import generate_dataset


def run_generator():
    N = int(N_entry.get())
    # Получение настроек от пользователя
    weights_ru_operators = [float(op_weight.get()) for op_weight in operator_weights_entries]
    operator_weights_spb = [float(spb_weight.get()) for spb_weight in spb_weights_entries]
    weights_job_titles = [float(job_weight.get()) for job_weight in job_weights_entries]

    # Здесь вы можете обновить словари с настройками
    WEIGHTS_FOR_RU_OPERATORS = dict(zip(config.OPERATOR_RU_CODES.keys(), weights_ru_operators))
    OPERATOR_WEIGHTS_FOR_SPB = dict(zip(config.OPERATOR_RU_CODES.keys(), operator_weights_spb))
    WEIGHTS_FOR_JOB_TITLES = dict(zip(config.WEIGHTS_FOR_JOB_TITLES.keys(), weights_job_titles))

    # Остальной код программы остается без изменений
    generate_dataset(N)


root = tk.Tk()
root.title('Генератор данных')

frame_n = ttk.Frame(root)
frame_n.grid(row=0, column=1, padx=10, pady=10)

N_label = ttk.Label(frame_n, text="Введите число N")
N_label.pack()
N_entry = ttk.Entry(frame_n, justify='center')  # Добавляем выравнивание по центру
N_entry.insert(0, '50000')  # Устанавливаем начальное значение 50000
N_entry.pack()

# Фрейм для настройки WEIGHTS_FOR_RU_OPERATORS
frame_ru_operators = ttk.Frame(root)
frame_ru_operators.grid(row=1, column=0, padx=10, pady=10, sticky='n')

weights_ru_operators_label = ttk.Label(frame_ru_operators, text='Настройка вероятности \nвыбора кода поставщика услуг', justify='center')
weights_ru_operators_label.pack()

operator_weights_entries = []
for operator, weight in config.WEIGHTS_FOR_RU_OPERATORS.items():
    op_label = ttk.Label(frame_ru_operators, text=operator)
    op_label.pack()
    op_entry = ttk.Entry(frame_ru_operators, justify='center')
    op_entry.insert(0, weight)
    op_entry.pack()
    operator_weights_entries.append(op_entry)

# Фрейм для настройки OPERATOR_WEIGHTS_FOR_SPB
frame_spb_weights = ttk.Frame(root)
frame_spb_weights.grid(row=1, column=1, padx=10, pady=10, sticky='n')

operator_weights_spb_label = ttk.Label(frame_spb_weights, text='Настройка вероятности внутреннего \nрегионального кода поставщика услуг',
                                       justify='center')
operator_weights_spb_label.pack()

spb_weights_entries = []
for operator, weight in config.OPERATOR_WEIGHTS_FOR_SPB.items():
    spb_label = ttk.Label(frame_spb_weights, text=operator)
    spb_label.pack()
    spb_entry = ttk.Entry(frame_spb_weights, justify='center')
    spb_entry.insert(0, weight)
    spb_entry.pack()
    spb_weights_entries.append(spb_entry)

# Фрейм для настройки WEIGHTS_FOR_JOB_TITLES
frame_job_titles = ttk.Frame(root)
frame_job_titles.grid(row=1, column=2, padx=10, pady=10, sticky='n')

weights_job_titles_label = ttk.Label(frame_job_titles, text='Настройки вероятности выбора профессий', justify='center')
weights_job_titles_label.pack()

job_weights_entries = []
for job_title, weight in config.WEIGHTS_FOR_JOB_TITLES.items():
    job_label = ttk.Label(frame_job_titles, text=job_title)
    job_label.pack()
    job_entry = ttk.Entry(frame_job_titles, justify='center')
    job_entry.insert(0, weight)
    job_entry.pack()
    job_weights_entries.append(job_entry)

text_under_col1 = 'Сумма вероятностей выбора всех операторов должна быть 1\nСумма вероятностей выбора Охранника, Уборщика, Коменданта, ' \
                  'Продавца должна быть 0.2\nСумма вероятностей выбора Программиста, Инженера, Медика, Маркетолога должна быть 0.4 '
label_under_col1 = ttk.Label(root, text=text_under_col1)
label_under_col1.grid(row=2, column=1, padx=10, pady=10)

# Button for generation data
generate_button = ttk.Button(root, text='Генерировать данные', command=run_generator)
generate_button.grid(row=4, column=1, padx=10, pady=10)

root.mainloop()
