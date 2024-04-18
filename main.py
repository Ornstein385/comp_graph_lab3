import tkinter as tk
from tkinter import DoubleVar, Entry, Label, Scale, Frame

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Определение начальных координат четырех точек
initial_points = np.array([
    [0, 0, 0],
    [1, 0, 1],
    [0, 1, 1],
    [1, 1, 0]
])


class SurfacePlotApp:
    def __init__(self, master):
        self.master = master
        master.title("Билинейная поверхность")

        # Визуализация на matplotlib
        self.fig, self.ax = plt.subplots(subplot_kw={"projection": "3d"})
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Создание рамок для группировки ввода данных
        input_frame = Frame(master)
        input_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        # Поля для ввода координат точек
        self.entries = []
        labels = ['X1', 'Y1', 'Z1', 'X2', 'Y2', 'Z2', 'X3', 'Y3', 'Z3', 'X4', 'Y4', 'Z4']
        for i in range(2):  # Две строки
            for j in range(6):  # Шесть столбцов
                index = 6 * i + j
                Label(input_frame, text=labels[index]).grid(row=i, column=2 * j, sticky="w")
                entry = Entry(input_frame, width=10)
                entry.insert(0, str(initial_points[index // 3, index % 3]))
                entry.grid(row=i, column=2 * j + 1)
                self.entries.append(entry)

        # Ползунки для управления углами поворота
        self.angle_x = DoubleVar()
        self.angle_y = DoubleVar()

        self.slider_x = Scale(master, label="Вращение X", from_=-180, to=180, orient='horizontal',
                              variable=self.angle_x, command=self.update_plot)
        self.slider_x.pack(fill=tk.X)
        self.slider_y = Scale(master, label="Вращение Y", from_=-180, to=180, orient='horizontal',
                              variable=self.angle_y, command=self.update_plot)
        self.slider_y.pack(fill=tk.X)

        self.update_plot()

    def update_plot(self, event=None):
        points = np.array([float(entry.get()) for entry in self.entries]).reshape(4, 3)

        # Применение вращения к точкам
        angle_x_rad = np.radians(self.angle_x.get())
        angle_y_rad = np.radians(self.angle_y.get())

        # Матрицы вращения
        rotate_x = np.array([
            [1, 0, 0],
            [0, np.cos(angle_x_rad), -np.sin(angle_x_rad)],
            [0, np.sin(angle_x_rad), np.cos(angle_x_rad)]
        ])

        rotate_y = np.array([
            [np.cos(angle_y_rad), 0, np.sin(angle_y_rad)],
            [0, 1, 0],
            [-np.sin(angle_y_rad), 0, np.cos(angle_y_rad)]
        ])

        # Применяем вращение
        rotated_points = points.dot(rotate_y).dot(rotate_x)

        # Создаем билинейную поверхность
        u = np.linspace(0, 1, 10)
        v = np.linspace(0, 1, 10)
        u, v = np.meshgrid(u, v)
        x = (1 - u) * (1 - v) * rotated_points[0, 0] + u * (1 - v) * rotated_points[1, 0] + (1 - u) * v * \
            rotated_points[2, 0] + u * v * rotated_points[3, 0]
        y = (1 - u) * (1 - v) * rotated_points[0, 1] + u * (1 - v) * rotated_points[1, 1] + (1 - u) * v * \
            rotated_points[2, 1] + u * v * rotated_points[3, 1]
        z = (1 - u) * (1 - v) * rotated_points[0, 2] + u * (1 - v) * rotated_points[1, 2] + (1 - u) * v * \
            rotated_points[2, 2] + u * v * rotated_points[3, 2]

        # Очищаем текущие графики
        self.ax.clear()
        self.ax.plot_surface(x, y, z, rstride=1, cstride=1, color='b', edgecolor='k')

        # Обновляем холст
        self.canvas.draw()


def main():
    root = tk.Tk()
    app = SurfacePlotApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()