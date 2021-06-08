from tkinter import *
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from genAlgo import GenAlgo
import numpy as np

answers = []


def updatePlot(minX, maxX, minY, maxY):
    x = np.linspace(int(minX - 1), int(maxX + 1), 5 * int(maxX - minX))
    y = np.linspace(int(minY - 1), int(maxY + 1), 5 * int(maxY - minY))

    X, Y = np.meshgrid(x, y)
    Z = GenAlgo.objectiveFunction(X, Y)

    ax.clear()
    ax.plot_wireframe(X, Y, Z, color='black')

    for tmp in answers:
        ax.scatter(tmp.x, tmp.y, tmp.f, color="red", linewidth=2)
    canvasChart.draw()


def newPlot():
    x = np.linspace(-6, 6, 30)
    y = np.linspace(-6, 6, 30)

    X, Y = np.meshgrid(x, y)
    Z = GenAlgo.objectiveFunction(X, Y)

    answers.clear()
    ax.clear()
    ax.plot_wireframe(X, Y, Z, color='black')
    canvasChart.draw()


def btnFindClick():
    try:
        minX = float(entMinX.get())
    except ValueError:
        messagebox.showerror(message="Введите рациональное число через точку в поле минимального значения X")
        entMinX.delete(0, END)
        return

    try:
        maxX = float(entMaxX.get())
    except ValueError:
        messagebox.showerror(message="Введите рациональное число через точку в поле максимального значения X")
        entMaxX.delete(0, END)
        return

    if minX >= maxX:
        messagebox.showerror(message="Поле минмального значения X должно быть меньше поля максимального значения X")
        return

    try:
        minY = float(entMinY.get())
    except ValueError:
        messagebox.showerror(message="Введите рациональное число через точку в поле минимального значения Y")
        entMinY.delete(0, END)
        return

    try:
        maxY = float(entMaxY.get())
    except ValueError:
        messagebox.showerror(message="Введите рациональное число через точку в поле максимального значения Y")
        entMaxY.delete(0, END)
        return

    if minY >= maxY:
        messagebox.showerror(message="Поле минмального значения Y должно быть меньше поля максимального значения Y")
        return

    try:
        population = int(entPopulation.get())
        if population <= 0:
            raise Exception("Введите натуральное число в поле численности популяции")
    except ValueError:
        messagebox.showerror(message="Введите натуральное число в поле численности популяции")
        entPopulation.delete(0, END)
        return
    except Exception as e:
        messagebox.showerror(message=e)
        entPopulation.delete(0, END)
        return

    try:
        children = int(entChildren.get())
        if children <= 0:
            raise Exception("Введите натуральное число в поле количества скрещиваний")
    except ValueError:
        messagebox.showerror(message="Введите натуральное число в поле количества скрещиваний")
        entChildren.delete(0, END)
        return
    except Exception as e:
        messagebox.showerror(message=e)
        entChildren.delete(0, END)
        return

    try:
        mutation = float(entMutation.get())
        if mutation < 0 or mutation > 1:
            raise Exception("Введите рациональное число от 0 до 1 через точку в поле вероятности мутации")
    except ValueError:
        messagebox.showerror(message="Введите рациональное число от 0 до 1 через точку в поле вероятности мутации")
        entMutation.delete(0, END)
        return
    except Exception as e:
        messagebox.showerror(message=e)
        entMutation.delete(0, END)
        return

    try:
        generation = int(entGeneration.get())
        if generation <= 0:
            raise Exception("Введите натуральное число в поле числа поколней")
    except ValueError:
        messagebox.showerror(message="Введите натуральное число в поле числа поколней")
        entGeneration.delete(0, END)
        return
    except Exception as e:
        messagebox.showerror(message=e)
        entGeneration.delete(0, END)
        return

    algo = GenAlgo(minX, maxX, minY, maxY, population, generation, children, mutation)
    answer = algo.genetic()

    txtAnswer.config(text=str(answer.f))
    txtResultX.config(text=str(answer.x))
    txtResultY.config(text=str(answer.y))

    answers.append(answer)

    updatePlot(minX, maxX, minY, maxY)


if __name__ == '__main__':
    root = Tk()

    root['bg'] = "#ffffff"
    root.title("Генетический алгоритм")
    root.wm_attributes('-alpha', 0.99)
    root.geometry('1000x600')

    root.resizable(width=False, height=False)

    canvas = Canvas(root, height=1000, width=600)
    canvas.pack()

    # Блок графика
    frameChart = Frame(root, bg="white", borderwidth=4, relief="groove")
    frameChart.place(relx=0.425, rely=0.05, relwidth=0.54, relheight=0.9)

    title = Label(frameChart, text="График функции")
    title.pack()

    fig = plt.figure(figsize=(25, 25))
    ax = plt.axes(projection='3d')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('f(x,y)')

    canvasChart = FigureCanvasTkAgg(fig, master=frameChart)
    canvasChart.get_tk_widget().pack()
    newPlot()

    btnFind = Button(frameChart, text="Очистить график", command=newPlot)
    btnFind.place(rely=0.925, relx=0.375)

    # Блок входных данных
    frameInput = Frame(root, bg="white", borderwidth=4, relief="groove")
    frameInput.place(relx=0.025, rely=0.05, relwidth=0.375, relheight=0.575)

    title = Label(master=frameInput, text="Входные данные", font=40)
    title.pack()

    lblInputX = Label(master=frameInput, text="Интервал поиска по X:")
    lblInputX.place(rely=0.1, relx=0.018)

    frameInputX = Frame(frameInput)
    frameInputX.place(rely=0.15, relx=0.14)

    lblMinX = Label(master=frameInputX, text="от:")
    entMinX = Entry(master=frameInputX, width=10, borderwidth=1, relief="groove", justify="right")
    lblMaxX = Label(master=frameInputX, text="до:")
    entMaxX = Entry(master=frameInputX, width=10, borderwidth=1, relief="groove", justify="right")
    lblMinX.grid(row=0, column=0, pady=8, padx=5, )
    entMinX.grid(row=0, column=1, padx=5)
    lblMaxX.grid(row=0, column=2, padx=5)
    entMaxX.grid(row=0, column=3, padx=5)

    lblInputY = Label(master=frameInput, text="Интервал поиска по Y:")
    lblInputY.place(rely=0.25, relx=0.018)

    frameInputY = Frame(frameInput)
    frameInputY.place(rely=0.3, relx=0.14)

    lblMinY = Label(master=frameInputY, text="от:")
    entMinY = Entry(master=frameInputY, width=10, borderwidth=1, relief="groove", justify="right")
    lblMaxY = Label(master=frameInputY, text="до:")
    entMaxY = Entry(master=frameInputY, width=10, borderwidth=1, relief="groove", justify="right")
    lblMinY.grid(row=0, column=0, pady=8, padx=5, )
    entMinY.grid(row=0, column=1, padx=5)
    lblMaxY.grid(row=0, column=2, padx=5)
    entMaxY.grid(row=0, column=3, padx=5)

    frameInputData = Frame(frameInput)
    frameInputData.place(rely=0.42, relx=0.018)

    lblPopulation = Label(master=frameInputData, text="Численность популяции:")
    entPopulation = Entry(master=frameInputData, width=10, borderwidth=1, relief="groove", justify="right")
    lblPopulation.grid(row=0, column=0, sticky="w", pady=5)
    entPopulation.grid(row=0, column=1, padx=40, )

    lblChildren = Label(master=frameInputData, text="Колличество скрещиваний\n в одном поколнии:")
    entChildren = Entry(master=frameInputData, width=10, borderwidth=1, relief="groove", justify="right")
    lblChildren.grid(row=1, column=0, sticky="w", pady=5)
    entChildren.grid(row=1, column=1, padx=40, )

    lblMutation = Label(master=frameInputData, text="Вероятность мутации:")
    entMutation = Entry(master=frameInputData, width=10, borderwidth=1, relief="groove", justify="right")
    lblMutation.grid(row=2, column=0, sticky="w", pady=5)
    entMutation.grid(row=2, column=1, padx=40, )

    lblGeneration = Label(master=frameInputData, text="Число поколений:")
    entGeneration = Entry(master=frameInputData, width=10, borderwidth=1, relief="groove", justify="right")
    lblGeneration.grid(row=3, column=0, sticky="w", pady=5)
    entGeneration.grid(row=3, column=1, padx=40, )

    btnFind = Button(frameInput, text="Поиск решения", command=btnFindClick)
    btnFind.place(rely=0.875, relx=0.3)

    # Блок результата
    frameOutput = Frame(root, bg="white", borderwidth=4, relief="groove")
    frameOutput.place(relx=0.025, rely=0.65, relwidth=0.375, relheight=0.3)

    title = Label(master=frameOutput, text="Разультат", font=40)
    title.pack()

    frameRes = Frame(frameOutput)
    frameRes.place(rely=0.15)

    lblResultX = Label(master=frameRes, text="Значение X:")
    txtResultX = Label(master=frameRes, bg="grey", width=30, relief="sunken")
    lblResultX.grid(row=0, column=0, pady=10, padx=5, sticky="e")
    txtResultX.grid(row=0, column=1, padx=5)

    lblResultY = Label(master=frameRes, text="Значение Y:")
    txtResultY = Label(master=frameRes, bg="grey", width=30, relief="sunken")
    lblResultY.grid(row=1, column=0, sticky="e", padx=5)
    txtResultY.grid(row=1, column=1, padx=5)

    lblAnswer = Label(master=frameOutput, text="Значение функции в данной точке:")
    lblAnswer.place(rely=0.6, relx=0.018)

    txtAnswer = Label(master=frameOutput, bg="grey", width=30, relief="sunken")
    txtAnswer.place(rely=0.75, relx=0.268)

    root.bind('<Return>', lambda event: btnFindClick())
    root.bind("<Escape>", lambda event: root.destroy())
    root.mainloop()
