import pandas as pd
import customtkinter as ctk


class DatasetDepersonalization:
    def __init__(self, file_path: str, status_label: ctk.CTkLabel, quasi_identifiers=None):
        self.file_path = file_path
        self.status_label = status_label
        self.quasi_identifiers = quasi_identifiers

        self.k_anonymity = 0

    def depersonalization(self) -> None:
        table = pd.read_excel(f"{self.file_path}",
                              dtype={"ФИО": str, "Номер телефона": str, "Адрес работы": str, "Должность": str, "З/П, в рублях": int})
        del table["Unnamed: 0"]
        full_names = table["ФИО"].to_numpy()
        phone_numbers = table["Номер телефона"].to_numpy()
        job_addresses = table["Адрес работы"].to_numpy()
        positions = table["Должность"].to_numpy()
        salary = table["З/П, в рублях"].to_numpy()

        for i in range(len(phone_numbers)):
            phone_numbers[i] = str(phone_numbers[i])[:6] + "******"

        self.status_label.configure(text="Выполнено!", text_color="green")

    def calc_k_anonymity(self) -> None:
        self.status_label.configure(text=f"k-anonymity={self.k_anonymity}", text_color="green")
