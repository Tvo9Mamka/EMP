import numpy
import numexpr


# функция расчета уравнения
def solveq(a, fi, eta, mu1, mu2, x_min, x_max, step_x, step_t, late):
    n = int(step_x)  # число узлов решетка по оси x
    m = int(step_t)  # число узлов решетка по оси t
    l = float(x_max) - float(x_min)  # длина интервала по оси x
    T = float(late)  # длительность колебаний
    h = l / n  # шаг по оси x
    k = T / m  # шаг по времени
    r = a * k / h  # промежуточная переменная
    u_tj_0 = []
    u_tj_1 = []
    for i in range(n + 1):
        x = i * h + x_min
        u_tj_0.append(numexpr.evaluate(fi))  # расчет 0-го слоя сетки
        u_tj_1.append(u_tj_0[i] + k * numexpr.evaluate(eta))  # расчет 1-го слоя сетки
    array = numpy.zeros((m + 1, n + 1))
    array[0] = numpy.array(u_tj_0)
    array[1] = numpy.array(u_tj_1)
    for i in range(m + 1):
        t = i * k
        x = x_min
        array[i][0] = numexpr.evaluate(mu1)  # заполнение массива граничными точками слева
        x = x_max
        array[i][-1] = numexpr.evaluate(mu2)  # заполнение массива граничными точками справо
    for i in range(1, m):
        for j in range(1, n):
            # расчет j + 1 слоя
            array[i + 1][j] = 2 * (1 - r * r) * array[i][j] + r * r * (array[i][j + 1] + array[i][j - 1]) \
                              - array[i - 1][j]
    x = numpy.arange(x_min, x_max + h, h)
    return x[:n + 1], m, array, h, k
