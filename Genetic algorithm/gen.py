import random
import numpy as np
import tkinter as tk
from tkinter import ttk, scrolledtext


def calculate_function_result(function_choice, x1, x2):
    if function_choice == "x1^2 + 3x2^2 + 2x1x2":
        return x1 ** 2 + 3 * x2 ** 2 + 2 * x1 * x2
    elif function_choice == "4(x1 - 5)^2+(x2 - 6)^2":
        return 4 * (x1 - 5) ** 2 + (x2 - 6) ** 2


class GeneticAlgorithm:
    """ Класс, отвечающий за генетический алгоритм """

    def __init__(self, function_choice, mutation_prob, num_chromosomes, min_gene, max_gene, num_generations, encoding_type):
        """ Инициализация параметров генетического алгоритма """
        self.function_choice = function_choice  # Выбранная функция
        self.mutation_prob = mutation_prob / 100.0  # Вероятность мутации (перевод в доли)
        self.num_chromosomes = num_chromosomes  # Количество хромосом в популяции
        self.min_gene = min_gene  # Минимальное значение гена
        self.max_gene = max_gene  # Максимальное значение гена
        self.num_generations = num_generations  # Количество поколений
        self.mutation_std_dev = 0.2  # Новый параметр для стратегии эволюционных стратегий
        self.population = []  # Хранение текущей популяции хромосом
        self.encoding_type = encoding_type  # Добавление параметра для хранения типа кодирования

    def run(self):
        """ Запуск генетического алгоритма """
        self.initialize_population()

        for generation in range(self.num_generations):
            self.calculate_fitness()
            self.selection()
            self.crossover()
            self.mutation()

    def binary_encoding(self):
        """ Binary encoding of chromosomes """
        self.population = []
        for i in range(self.num_chromosomes):
            gene1_binary = format(random.randint(int(self.min_gene), int(self.max_gene)), 'b')
            gene2_binary = format(random.randint(int(self.min_gene), int(self.max_gene)), 'b')
            gene1 = int(gene1_binary, 2)
            gene2 = int(gene2_binary, 2)
            self.population.append((gene1, gene2, 0))  # 0 - временное значение результата

    def real_encoding(self):
        """ Вещественное кодирование хромосом """
        self.population = []
        for i in range(self.num_chromosomes):
            gene1 = random.uniform(self.min_gene, self.max_gene)
            gene2 = random.uniform(self.min_gene, self.max_gene)
            result = calculate_function_result(self.function_choice, gene1, gene2)
            self.population.append((gene1, gene2, result))

    def initialize_population(self):
        """ Инициализация начальной популяции с учетом выбора кодирования """
        if self.encoding_type == "binary":
            self.binary_encoding()
        elif self.encoding_type == "real":
            self.real_encoding()

    def calculate_fitness(self):
        """ Расчет значения функции для каждой хромосомы в текущей популяции """
        for i, chromosome in enumerate(self.population):
            result = calculate_function_result(self.function_choice, chromosome[0], chromosome[1])
            self.population[i] = (chromosome[0], chromosome[1], result)

    def selection(self):
        """ Сортировка популяции по значению функции и выбор лучших хромосом """
        self.population = sorted(self.population, key=lambda x: x[2])[:self.num_chromosomes]

    def crossover(self):
        """ Скрещивание пар хромосом для создания новых потомков """
        new_population = []
        for i in range(0, self.num_chromosomes, 2):
            parent1 = np.array([self.population[i][0], self.population[i][1]])
            parent2 = np.array([self.population[i + 1][0], self.population[i + 1][1]])

            """ Используем стратегию эволюционных стратегий для скрещивания """
            alpha = np.random.rand(2)
            child1 = alpha * parent1 + (1 - alpha) * parent2
            child2 = alpha * parent2 + (1 - alpha) * parent1

            child1_result = calculate_function_result(self.function_choice, child1[0], child1[1])
            child2_result = calculate_function_result(self.function_choice, child2[0], child2[1])

            new_population.extend([(child1[0], child1[1], child1_result), (child2[0], child2[1], child2_result)])

        self.population = new_population

    def mutation(self):
        """ Мутация случайных хромосом в текущей популяции """
        for i in range(self.num_chromosomes):
            if random.random() < self.mutation_prob:
                parent = np.array([self.population[i][0], self.population[i][1]])

                """ Используем стратегию эволюционных стратегий для мутации """
                mutation_shift = np.random.normal(0, self.mutation_std_dev, 2)
                child = parent + mutation_shift

                child_result = calculate_function_result(self.function_choice, child[0], child[1])
                self.population[i] = (child[0], child[1], child_result)

    def get_best_solution(self):
        """ Получение лучшего решения из текущей популяции """
        best_solution = min(self.population, key=lambda x: x[2])
        return best_solution[0], best_solution[1], best_solution[2]

    def get_population(self):
        """ Получение информации о популяции для отображения в интерфейсе """
        return [(i + 1, chromosome[2], chromosome[0], chromosome[1]) for i, chromosome in enumerate(self.population)]


class GeneticAlgorithmInterface:
    """ Класс, отвечающий за интерфейс на библиотеке tkinter """

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Генетический алгоритм")

        """ Добавление элементов интерфейса (выбор функции, вероятность мутации и т.д.) """
        self.function_label = ttk.Label(self.root, text="Функция:")
        self.function_combobox = ttk.Combobox(self.root, values=["x1^2 + 3x2^2 + 2x1x2", "4(x1 - 5)^2+(x2 - 6)^2"], state="readonly")
        self.mutation_label = ttk.Label(self.root, text="Вероятность мутации (%):")
        self.mutation_entry = ttk.Entry(self.root)
        self.mutation_entry.insert(0, "5")
        self.num_chromosomes_label = ttk.Label(self.root, text="Количество хромосом:")
        self.num_chromosomes_entry = ttk.Entry(self.root)
        self.num_chromosomes_entry.insert(0, "50")
        self.min_gene_label = ttk.Label(self.root, text="Минимальное значение гена:")
        self.min_gene_entry = ttk.Entry(self.root)
        self.min_gene_entry.insert(0, "-10")
        self.max_gene_label = ttk.Label(self.root, text="Максимальное значение гена:")
        self.max_gene_entry = ttk.Entry(self.root)
        self.max_gene_entry.insert(0, "10")
        self.num_generations_label = ttk.Label(self.root, text="Количество поколений:")
        self.num_generations_entry = ttk.Entry(self.root)
        self.num_generations_entry.insert(0, "50")
        self.calculate_button = ttk.Button(self.root, text="Рассчитать", command=self.run_genetic_algorithm)
        self.result_label = ttk.Label(self.root, text="Результат:")
        self.result_text = scrolledtext.ScrolledText(self.root, width=30, height=5)
        self.result_text.config(state=tk.DISABLED)
        self.encoding_label = ttk.Label(self.root, text="Тип кодирования:")
        self.encoding_combobox = ttk.Combobox(self.root, values=["Бинарное", "Вещественное"], state="readonly")
        self.encoding_combobox.current(0)

        self.table_label = ttk.Label(self.root, text="Таблица хромосом:")
        self.tree = ttk.Treeview(self.root, columns=('Number', 'Result', 'Gene1', 'Gene2'), show='headings', height=15)
        self.tree.heading('Number', text='Номер')
        self.tree.heading('Result', text='Результат')
        self.tree.heading('Gene1', text='Ген 1')
        self.tree.heading('Gene2', text='Ген 2')
        self.tree.column('Number', width=50)
        self.tree.column('Result', width=100)
        self.tree.column('Gene1', width=80)
        self.tree.column('Gene2', width=80)

        """ Размещение элементов в окне """
        self.function_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.function_combobox.grid(row=0, column=1, padx=10, pady=10)
        self.mutation_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.mutation_entry.grid(row=1, column=1, padx=10, pady=10)
        self.num_chromosomes_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.num_chromosomes_entry.grid(row=2, column=1, padx=10, pady=10)
        self.min_gene_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.min_gene_entry.grid(row=3, column=1, padx=10, pady=10)
        self.max_gene_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.max_gene_entry.grid(row=4, column=1, padx=10, pady=10)
        self.num_generations_label.grid(row=5, column=0, padx=10, pady=10, sticky="w")
        self.num_generations_entry.grid(row=5, column=1, padx=10, pady=10)
        self.calculate_button.grid(row=6, column=0, columnspan=2, pady=20)
        self.result_label.grid(row=7, column=0, padx=10, pady=10, sticky="w")
        self.result_text.grid(row=7, column=1, padx=10, pady=10, columnspan=1)
        self.table_label.grid(row=0, column=2, padx=10, pady=10, sticky="w")
        self.tree.grid(row=0, column=2, padx=10, pady=10, columnspan=2, rowspan=9)
        self.encoding_label.grid(row=8, column=0, padx=10, pady=10, sticky="w")
        self.encoding_combobox.grid(row=8, column=1, padx=10, pady=10)

    def run_genetic_algorithm(self):
        """ Получение параметров из интерфейса """
        function_choice = self.function_combobox.get()
        mutation_prob = float(self.mutation_entry.get())
        num_chromosomes = int(self.num_chromosomes_entry.get())
        min_gene = float(self.min_gene_entry.get())
        max_gene = float(self.max_gene_entry.get())
        num_generations = int(self.num_generations_entry.get())
        encoding_type = "binary" if self.encoding_combobox.get() == "Бинарное" else "real"

        """ Создание экземпляра генетического алгоритма и запуск """
        genetic_algorithm = GeneticAlgorithm(function_choice, mutation_prob, num_chromosomes, min_gene, max_gene, num_generations, encoding_type)
        genetic_algorithm.run()

        """ Получение и вывод результатов """
        best_solution = genetic_algorithm.get_best_solution()
        population_data = genetic_algorithm.get_population()

        """ Отображение результатов в таблице """
        self.fill_table(population_data)

        """ Отображение результатов в виде x1 и x2 """
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"Лучшее решение:\nx1={best_solution[0]}\nx2={best_solution[1]}\n")
        self.result_text.insert(tk.END, f"Значение функции:\n{best_solution[2]}")
        self.result_text.config(state=tk.DISABLED)

    def fill_table(self, results):
        """ Очистка текущих данных в таблице """
        for item in self.tree.get_children():
            self.tree.delete(item)

        """ Заполнение таблицы новыми данными """
        for result in results:
            self.tree.insert('', tk.END, values=result)


if __name__ == "__main__":
    window = tk.Tk()
    GeneticAlgorithmInterface(window)
    window.mainloop()
