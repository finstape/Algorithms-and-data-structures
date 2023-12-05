import random
import numpy as np
import tkinter as tk
from tkinter import ttk
from threading import Thread
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def calculate_function_result(function_choice, x1, x2):
    """ Вычисление значения выбранной функции """
    if function_choice == "x1^2 + 3x2^2 + 2x1x2":
        return x1 ** 2 + 3 * x2 ** 2 + 2 * x1 * x2
    elif function_choice == "4(x1 - 5)^2+(x2 - 6)^2":
        return 4 * (x1 - 5) ** 2 + (x2 - 6) ** 2


class Particle:
    """ Класс, представляющий частицу в рое """

    def __init__(self, num_dimensions):
        self.position = np.array([random.uniform(-5, 5) for _ in range(num_dimensions)])
        self.velocity = np.array([random.uniform(-1, 1) for _ in range(num_dimensions)])
        self.best_position = np.copy(self.position)
        self.best_value = float('inf')


class Swarm:
    """ Класс, представляющий рой частиц """

    def __init__(self, num_particles, num_dimensions, inertia, personal_coeff, global_coeff, calculate_function_result):
        self.particles = [Particle(num_dimensions) for _ in range(num_particles)]
        self.inertia = inertia
        self.personal_coeff = personal_coeff
        self.global_coeff = global_coeff
        self.calculate_function_result = calculate_function_result

    def update_particle(self, particle, global_best_position, iteration, max_iterations):
        """ Обновление положения и скорости частицы """
        current_inertia = self.inertia * (1 - iteration / max_iterations)

        inertia_term = current_inertia * particle.velocity
        personal_term = self.personal_coeff * random.random() * (particle.best_position - particle.position)
        global_term = self.global_coeff * random.random() * (global_best_position - particle.position)
        particle.velocity = inertia_term + personal_term + global_term

        particle.position += particle.velocity

        current_value = self.calculate_function_result(particle.position[0], particle.position[1])
        if current_value < particle.best_value:
            particle.best_value = current_value
            particle.best_position = np.copy(particle.position)


class ParticleSwarmOptimizationApp:
    """ Класс, отвечающий за интерфейс на библиотеке tkinter """

    def __init__(self, root):
        self.root = root
        self.root.title("Роевой интеллект")

        """ Переменные """
        self.num_particles_var = tk.StringVar(value="20")
        self.inertia_var = tk.StringVar(value="0.5")
        self.personal_coeff_var = tk.StringVar(value="1.5")
        self.global_coeff_var = tk.StringVar(value="1.5")
        self.num_iterations_var = tk.StringVar(value="50")
        self.function_choice_var = tk.StringVar(value="x1^2 + 3x2^2 + 2x1x2")
        self.result_labels = []

        """ Интерфейс """
        ttk.Label(self.root, text="Функция:").grid(row=0, column=0, columnspan=2, pady=10)
        self.test_function_combobox = ttk.Combobox(
            self.root, values=["x1^2 + 3x2^2 + 2x1x2", "4(x1 - 5)^2+(x2 - 6)^2"],
            textvariable=self.function_choice_var, state="readonly"
        )
        self.test_function_combobox.grid(row=0, column=2, columnspan=2, pady=10)
        ttk.Label(self.root, text="Количество частиц:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        ttk.Entry(self.root, textvariable=self.num_particles_var).grid(row=1, column=1, padx=10, pady=10, sticky="w")
        ttk.Label(self.root, text="Коэффициент текущей скорости:").grid(row=1, column=2, padx=10, pady=10, sticky="w")
        ttk.Entry(self.root, textvariable=self.inertia_var).grid(row=1, column=3, padx=10, pady=10, sticky="w")
        ttk.Label(self.root, text="Коэффициент собственного лучшего значения:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        ttk.Entry(self.root, textvariable=self.personal_coeff_var).grid(row=2, column=1, padx=10, pady=10, sticky="w")
        ttk.Label(self.root, text="Коэффициент глобального лучшего значения:").grid(row=2, column=2, padx=10, pady=10, sticky="w")
        ttk.Entry(self.root, textvariable=self.global_coeff_var).grid(row=2, column=3, padx=10, pady=10, sticky="w")
        ttk.Label(self.root, text="Количество итераций:").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        ttk.Entry(self.root, textvariable=self.num_iterations_var).grid(row=3, column=1, padx=10, pady=10, sticky="w")
        ttk.Button(self.root, text="Рассчитать", command=self.start_swarm).grid(row=4, column=0, columnspan=4, padx=10, pady=10)

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.grid(row=5, column=0, columnspan=4)

    def clear_results(self):
        """ Очистка результатов предыдущих вычислений """
        for label in self.result_labels:
            label.destroy()
        self.result_labels = []

    def start_swarm(self):
        """ Запуск роя в отдельном потоке """
        self.clear_results()
        num_particles = int(self.num_particles_var.get())
        inertia = float(self.inertia_var.get())
        personal_coeff = float(self.personal_coeff_var.get())
        global_coeff = float(self.global_coeff_var.get())
        num_iterations = int(self.num_iterations_var.get())
        function_choice = self.function_choice_var.get()

        # Start swarm in a separate thread
        swarm_thread = Thread(target=self.run_swarm, args=(num_particles, inertia, personal_coeff, global_coeff, num_iterations, function_choice))
        swarm_thread.start()

    def run_swarm(self, num_particles, inertia, personal_coeff, global_coeff, num_iterations, function_choice):
        """ Выполнение рассчетов и отображение результатов """
        self.clear_results()
        swarm = Swarm(num_particles, 2, inertia, personal_coeff, global_coeff, calculate_function_result)
        swarm.calculate_function_result = lambda x1, x2: calculate_function_result(function_choice, x1, x2)
        global_best_position = np.zeros(2)
        global_best_value = float('inf')

        for iteration in range(num_iterations):
            for particle in swarm.particles:
                swarm.update_particle(particle, global_best_position, iteration, num_iterations)
                current_value = calculate_function_result(function_choice, particle.position[0], particle.position[1])

                if current_value < global_best_value:
                    global_best_value = current_value
                    global_best_position = np.copy(particle.position)

            self.plot_swarm(swarm, iteration)

        """ Вывод результатов """
        ttk.Label(self.root, text=f"Лучшее решение: {global_best_position}").grid(row=6, column=0, columnspan=4)
        ttk.Label(self.root, text=f"Значение функции: {global_best_value}").grid(row=7, column=0, columnspan=4)

    def plot_swarm(self, swarm, iteration):
        """ Отображение текущего состояния роя на графике """
        self.ax.clear()
        positions = np.array([particle.position for particle in swarm.particles])
        self.ax.scatter(positions[:, 0], positions[:, 1], label=f'Итерация {iteration + 1}')
        self.ax.legend()
        self.canvas.draw()


if __name__ == "__main__":
    window = tk.Tk()
    ParticleSwarmOptimizationApp(window)
    window.mainloop()
