import threading
import customtkinter as ctk
from tkinter import filedialog


class InterfaceApp:
    def __init__(self, root: ctk.CTk):
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.root = root
        self.root.title("Обезличивание данных")

        self.input_file = ""
        self.button_ds_anon = None
        self.button_k_anon_calc = None
        self.input_file_button = None
        self.input_file_label = None
        self.checkboxes = None
        self.checkbox_labels = None
        self.status_label = None

        self.create_interface()

    def create_interface(self) -> None:
        """ Create a label to show the selected input file """
        self.input_file_label = ctk.CTkLabel(self.root, text="Входной файл: Не выбран")
        self.input_file_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        """ Create a button to select the input file """
        self.input_file_button = ctk.CTkButton(self.root, text="Выбрать", command=self.select_input_file)
        self.input_file_button.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        """ Create a text about instances """
        self.status_label = ctk.CTkLabel(self.root, text="Квази-идентификаторы в К-анонимити:")
        self.status_label.grid(row=1, column=0, columnspan=2, padx=10)

        """ Create CTkCheckBox instances with default state set to True """
        self.checkbox_labels = ["Номер", "ФИО", "Номер телефона", "Адрес работы", "Должность", "З/П, в рублях"]
        self.checkboxes = [ctk.CTkCheckBox(self.root, text=label) for label in self.checkbox_labels]
        for i, checkbox in enumerate(self.checkboxes):
            checkbox.grid(row=i // 2 + 2, column=i % 2, padx=10, pady=10, sticky="w")

        """ Create a button to start dataset anonymization """
        self.button_ds_anon = ctk.CTkButton(self.root, text="Обезличивание данных", command=self.start_ds_anon)
        self.button_ds_anon.grid(row=5, column=0, padx=10, pady=10, sticky="w")

        """ Create a button to start calculating k-anonymity """
        self.button_k_anon_calc = ctk.CTkButton(self.root, text="Вычисление К-анонимити", command=self.start_k_anon_calc)
        self.button_k_anon_calc.grid(row=5, column=1, padx=10, pady=10, sticky="e")

        """ Create a status label """
        self.status_label = ctk.CTkLabel(self.root, text="")
        self.status_label.grid(row=6, column=0, columnspan=2, pady=10, padx=10)

    def select_input_file(self) -> None:
        self.input_file = filedialog.askopenfilename()
        if self.input_file:
            self.input_file_label.configure(text="Входной файл: Выбран")

    def threading_run_ds_anon(self) -> None:
        t = threading.Thread(target=self.start_ds_anon)
        t.start()

    def threading_run_k_anon_calc(self) -> None:
        t = threading.Thread(target=self.start_k_anon_calc)
        t.start()

    def start_ds_anon(self) -> None:
        pass

    def start_k_anon_calc(self) -> None:
        pass


if __name__ == "__main__":
    window = ctk.CTk()
    InterfaceApp(window)
    window.mainloop()
