import config
import random
import pandas as pd
from typing import List

phone_numbers = set()


def generate_random_full_name(slavic_male_surnames: List[str], slavic_male_names: List[str], slavic_male_patronymics: List[str],
                              slavic_female_surnames: List[str], slavic_female_names: List[str], slavic_female_patronymics: List[str]) -> str:
    is_male = random.choices([True, False], weights=[0.453, 0.557], k=1)[0]
    if is_male:
        full_name = random.choice(slavic_male_surnames) + ' ' + random.choice(slavic_male_names) + ' ' + random.choice(slavic_male_patronymics)
    else:
        full_name = random.choice(slavic_female_surnames) + ' ' + random.choice(slavic_female_names) + ' ' + random.choice(slavic_female_patronymics)
    return full_name


def generate_random_phone_number(WEIGHTS_FOR_RU_OPERATORS, OPERATOR_WEIGHTS_FOR_SPB) -> str:
    operator = random.choices(list(config.OPERATOR_RU_CODES.keys()), weights=list(WEIGHTS_FOR_RU_OPERATORS.values()), k=1)[0]
    is_from_spb = \
        random.choices([True, False], weights=[OPERATOR_WEIGHTS_FOR_SPB[operator], 1 - OPERATOR_WEIGHTS_FOR_SPB[operator]], k=1)[0]
    if is_from_spb:
        operator_code = random.choice(config.OPERATOR_RU_CODES[operator])
    else:
        operator_code = random.choice(config.OPERATOR_SPB_CODES[operator])
    random_number = random.randint(0, 9999999)
    phone_number = '+7' + str(operator_code)
    phone_number += str(random_number) if random_number > 999999 else '0' * (7 - len(str(random_number))) + str(random_number)
    if phone_number in phone_numbers:
        return generate_random_phone_number(WEIGHTS_FOR_RU_OPERATORS, OPERATOR_WEIGHTS_FOR_SPB)
    else:
        phone_numbers.add(phone_number)
        return phone_number


def generate_dataset(N: int, status_label, WEIGHTS_FOR_RU_OPERATORS, OPERATOR_WEIGHTS_FOR_SPB, WEIGHTS_FOR_JOB_TITLES) -> None:
    try:
        # Getting the lists of male and female surnames, names, patronymics
        with open('datasets/slavic_male_surnames.txt', 'r', encoding='utf-8') as f:
            slavic_male_surnames = f.read().splitlines()

        with open('datasets/slavic_male_names.txt', 'r', encoding='utf-8') as f:
            slavic_male_names = f.read().splitlines()

        with open('datasets/slavic_male_patronymics.txt', 'r', encoding='utf-8') as f:
            slavic_male_patronymics = f.read().splitlines()

        with open('datasets/slavic_female_surnames.txt', 'r', encoding='utf-8') as f:
            slavic_female_surnames = f.read().splitlines()

        with open('datasets/slavic_female_names.txt', 'r', encoding='utf-8') as f:
            slavic_female_names = f.read().splitlines()

        with open('datasets/slavic_female_patronymics.txt', 'r', encoding='utf-8') as f:
            slavic_female_patronymics = f.read().splitlines()

        # Getting the dictionary of St. Petersburg addresses
        with open('datasets/saint_petersburg_addresses.txt', 'r', encoding='utf-8') as f:
            saint_petersburg_addresses_list = f.read().splitlines()
            saint_petersburg_addresses = {}
            for i in range(0, len(saint_petersburg_addresses_list), 2):
                saint_petersburg_addresses.update(
                    {saint_petersburg_addresses_list[i]: list(map(str, saint_petersburg_addresses_list[i + 1].split(', ')))})

        # The final result of a program
        dataset = [[] for _ in range(N)]

        current_amount = 0
        while current_amount != N:
            current_address = random.choice(list(saint_petersburg_addresses.keys()))
            current_address += ', д. ' + random.choice(saint_petersburg_addresses[current_address])

            number_of_employees = random.randint(50, 150)
            if N - current_amount - number_of_employees <= 50:
                number_of_employees = N - current_amount

            for i in range(number_of_employees):
                current_job_title = \
                    random.choices(list(WEIGHTS_FOR_JOB_TITLES.keys()), weights=list(WEIGHTS_FOR_JOB_TITLES.values()), k=1)[
                        0]
                if config.WEIGHTS_FOR_HALF_TIME[current_job_title] != 0:
                    is_job_half_time = random.choices([True, False], weights=[config.WEIGHTS_FOR_HALF_TIME[current_job_title],
                                                                              1 - config.WEIGHTS_FOR_HALF_TIME[current_job_title]], k=1)[0]
                else:
                    is_job_half_time = False
                salary = config.SALARY[current_job_title] // 2 if is_job_half_time else config.SALARY[current_job_title]
                dataset[current_amount] = [
                    generate_random_full_name(slavic_male_surnames, slavic_male_names, slavic_male_patronymics, slavic_female_surnames,
                                              slavic_female_names, slavic_female_patronymics),
                    generate_random_phone_number(WEIGHTS_FOR_RU_OPERATORS, OPERATOR_WEIGHTS_FOR_SPB), current_address,
                    current_job_title, salary]
                current_amount += 1

        random.shuffle(dataset)

        # Create table in pandas
        df = pd.DataFrame(dataset, columns=['ФИО', 'Номер телефона', 'Адрес работы', 'Должность', 'З/П, в рублях'])
        df.index = range(1, len(df) + 1)

        column_widths = {
            'ФИО': 50,
            'Номер телефона': 16,
            'Адрес работы': 45,
            'Должность': 15,
            'З/П, в рублях': 13
        }

        # Saving to excel
        with pd.ExcelWriter('dataset.xlsx', engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Job dataset', index=True)

            worksheet = writer.sheets['Job dataset']

            for col_idx, (column, width) in enumerate(column_widths.items()):
                worksheet.column_dimensions[chr(66 + col_idx)].width = width
        status_label.configure(text="Done", text_color="green")
    except:
        status_label.configure(text="Error", text_color="red")
