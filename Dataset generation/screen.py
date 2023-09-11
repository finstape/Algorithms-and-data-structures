import config
import customtkinter as ctk
from generator import generate_dataset

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

ctk.set_widget_scaling(0.7)
ctk.set_window_scaling(0.7)


def run_generator():
    N = int(N_entry.get())

    weights_ru_operators = [float(op_weight.get()) for op_weight in operator_weights_entries]
    operator_weights_spb = [float(spb_weight.get()) for spb_weight in spb_weights_entries]
    weights_job_titles = [float(job_weight.get()) for job_weight in job_weights_entries]

    WEIGHTS_FOR_RU_OPERATORS = dict(zip(config.OPERATOR_RU_CODES.keys(), weights_ru_operators))
    OPERATOR_WEIGHTS_FOR_SPB = dict(zip(config.OPERATOR_RU_CODES.keys(), operator_weights_spb))
    WEIGHTS_FOR_JOB_TITLES = dict(zip(config.WEIGHTS_FOR_JOB_TITLES.keys(), weights_job_titles))

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

text_under_col1 = 'Сумма вероятностей выбора всех операторов должна быть 1\nСумма вероятностей выбора Охранника, Уборщика, Коменданта, ' \
                  'Продавца должна быть 0.2\nСумма вероятностей выбора Программиста, Инженера, Медика, Маркетолога должна быть 0.4 '
label_under_col1 = ctk.CTkLabel(root, text=text_under_col1)
label_under_col1.grid(row=3, column=1, padx=10, pady=10)
default_color = label_under_col1.cget('fg_color')
frame_n.configure(fg_color=default_color)
frame_job_titles.configure(fg_color=default_color)
frame_ru_operators.configure(fg_color=default_color)
frame_spb_weights.configure(fg_color=default_color)

# Button for generation data
generate_button = ctk.CTkButton(root, text='Генерировать данные', command=run_generator)
generate_button.grid(row=4, column=1, padx=10, pady=10)

status_label = ctk.CTkLabel(root, text="")
status_label.grid(row=5, column=1, pady=10, padx=10)

root.mainloop()
