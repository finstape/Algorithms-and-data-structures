import pandas as pd
import customtkinter as ctk


class DatasetDepersonalization:
    def __init__(self, file_path: str, status_label: ctk.CTkLabel, quasi_identifiers=None):
        self.file_path = file_path
        self.status_label = status_label
        self.quasi_identifiers = quasi_identifiers

        self.k_anonymity = 0

    def depersonalization(self) -> None:
        table = pd.read_excel(f"{self.file_path}")
        ids = table["Номер"].to_numpy()
        full_names = table["ФИО"].to_numpy()
        phone_numbers = table["Номер телефона"].to_numpy()
        job_addresses = table["Адрес работы"].to_numpy()
        positions = table["Должность"].to_numpy()
        salary = table["З/П, в рублях"].to_numpy()

        self.status_label.configure(text="Выполнено!", text_color="green")

    def calc_k_anonymity(self) -> None:
        self.status_label.configure(text=f"k-anonymity={self.k_anonymity}", text_color="green")
