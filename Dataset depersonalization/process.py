import pandas as pd
import customtkinter as ctk


class DatasetDepersonalization:
    def __init__(self, file_path: str, status_label: ctk.CTkLabel, quasi_identifiers=None):
        self.file_path = file_path
        self.status_label = status_label
        self.quasi_identifiers = quasi_identifiers

    def depersonalization(self) -> None:
        table = pd.read_excel(f"{self.file_path}",
                              dtype={"ФИО": str, "Номер телефона": str, "Адрес работы": str, "Должность": str, "З/П, в рублях": str})
        del table["Unnamed: 0"]
        full_names = table["ФИО"].to_numpy()
        phone_numbers = table["Номер телефона"].to_numpy()
        job_addresses = table["Адрес работы"].to_numpy()
        positions = table["Должность"].to_numpy()
        salary = table["З/П, в рублях"].to_numpy()

        streets_to_districts = dict()
        with open("saint_petersburg_districts.txt", "r", encoding="utf-8") as file:
            for num in range(0, 3008, 2):
                street = file.readline()[:-1]
                district = file.readline()[:-1]
                streets_to_districts[street] = district

        for i in range(len(phone_numbers)):
            full_names[i] = ""  # Удаление атрибутов
            phone_numbers[i] = str(phone_numbers[i])[:5] + "******"  # Маскеризация
            job_addresses[i] = streets_to_districts[list(job_addresses[i].split(', д. '))[0]]
            salary[i] = "10000-50000" if 10000 <= int(salary[i]) <= 50000 else "50000-125000"  # Локальное обобщение

        """ Создание таблице в pandas """
        df = pd.DataFrame(
            {"ФИО": full_names, "Номер телефона": phone_numbers, "Адрес работы": job_addresses, "Должность": positions, "З/П, в рублях": salary})
        df.index = range(1, len(df) + 1)

        column_widths = {
            "ФИО": 50,
            "Номер телефона": 16,
            "Адрес работы": 45,
            "Должность": 15,
            "З/П, в рублях": 14
        }

        """ Сохранение таблицы в Excel """
        with pd.ExcelWriter("dataset anonymized.xlsx", engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name="Job dataset", index=True)

            worksheet = writer.sheets["Job dataset"]

            for col_idx, (column, width) in enumerate(column_widths.items()):
                worksheet.column_dimensions[chr(66 + col_idx)].width = width

        self.status_label.configure(text="Выполнено!", text_color="green")

    def calc_k_anonymity(self) -> None:
        table = pd.read_excel("dataset anonymized.xlsx",
                              dtype={"ФИО": str, "Номер телефона": str, "Адрес работы": str, "Должность": str, "З/П, в рублях": str})
        del table["Unnamed: 0"]

        output_text = f"Колонки в исходной таблице:\n{list(table)}\n\nКвази-идентификаторы:\n{list(self.quasi_identifiers)}\n\nПлохие значения " \
                      f"К-анонимити\n"
        for column in list(table):
            if column not in self.quasi_identifiers:
                del table[column]

        data = table.to_numpy()
        unique_rows_count = {}

        for row in data:
            concatenated_row = " ".join(map(str, row))
            try:
                unique_rows_count[concatenated_row] += 1
            except KeyError:
                unique_rows_count[concatenated_row] = 1

        k_anonimyty = len(data)
        min_occurrences_list = sorted([count for count in unique_rows_count.values()])
        for row, count in unique_rows_count.items():
            if count in min_occurrences_list[:5]:
                percentage = round(count / len(data) * 100, 3)
                output_text += f"{row}, к={count}, {percentage}%\n"
            k_anonimyty = min(k_anonimyty, unique_rows_count[row])

        output_text += f"\nКоличество уникальных строк в датасете = {len(unique_rows_count)}\n"
        if k_anonimyty == 1:
            output_text += "\nК-анонимити = 1\nУникальные строки:\n"
            output_text += "".join([f"{row}\n" for row in unique_rows_count if unique_rows_count[row] == 1])
        else:
            output_text += f"\nК-анонимити = {k_anonimyty}"

        """ Сохранение нужного текста для вывода """
        with open("output.txt", "w", encoding="utf-8") as file:
            file.write(output_text)

        self.status_label.configure(text=f"k-anonymity={k_anonimyty}", text_color="green")
