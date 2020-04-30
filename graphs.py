from tkinter import *
import Math
import matplotlib.pyplot as plt
import numexpr
import matplotlib.widgets as But
from tkinter import messagebox as mb

STOP = False


def p(event):
    global STOP
    STOP = True


def check_r(event):
    if float(a.get()) * (float(step_xi.get()) * float(lat.get()) / float(step_ti.get()) / (float(numexpr.evaluate(x1.get())) - numexpr.evaluate(x0.get()))) ** 2 <= 1:
        draw_graph()
    else:
        mb.showerror("Ошибка", 'Сетка не устойчива')


def draw_graph():
    global STOP
    max_x = numexpr.evaluate(x1.get())
    min_x = numexpr.evaluate(x0.get())
    data = Math.solveq(float(a.get()) ** 0.5, fi.get(), w.get(), gam1.get(), gam2.get(), min_x, max_x,
                       step_xi.get(), step_ti.get(), lat.get())
    x = data[0]
    plt.ion()
    n = 0
    y_min = data[2].min()
    y_max = data[2].max()
    if y_min == 0 and y_max == 0:
        y_min = -1
        y_max = 1
    elif y_min == 0:
        y_min = -0.1 * max_x
        y_max = y_max + abs(y_max * 0.1)
    elif y_max == 0:
        y_max = abs(y_min * 0.1)
        y_min = y_min - abs(y_min * 0.1)
    else:
        y_min = y_min - abs(y_min * 0.1)
        y_max = y_max + abs(y_max * 0.1)
    while not STOP and n < data[1] + 1:
        plt.clf()
        y = data[2][n]
        plt.plot(x, y)

        plt.xlim(min_x, max_x)
        plt.ylim(y_min, y_max)
        plt.figtext(0, 0, 't=' + str(round(n * data[4], 3)))

#        axcut = plt.axes([0.9, -0.01, 0.1, 0.07])
#        bcut = But.Button(axcut, 'Выход')
#        bcut.on_clicked(p)
        plt.draw()
        plt.pause(data[4])
        n += 1

    if STOP:
        STOP = False
        plt.close('all')

    plt.ioff()
    plt.show()


# настройки окна
root = Tk()
root.title("Колебания струны")
w = root.winfo_screenwidth()  # ширина экрана
h = root.winfo_screenheight()  # высота экрана
w = w // 2  # середина экрана
h = h // 2
w = w - 125  # смещение от середины
h = h - 175
root.geometry('250x350+{}+{}'.format(w, h))
data_frame = Frame(root, height=350, width=250)

# уравнение
u1 = Label(data_frame, text='U', font='arial 14')
u1.place(x=20, y=10)
u2 = Label(data_frame, text='U', font='arial 14')
u2.place(x=87, y=10)
xx = Label(data_frame, text='xx', font='arial 9')
xx.place(x=103, y=17)
tt = Label(data_frame, text='tt', font='arial 9')
tt.place(x=35, y=17)
raw = Label(data_frame, text='=', font='arial 14')
raw.place(x=45, y=10)
a = Entry(data_frame, width=3)
a.insert(0, '1')
a.place(x=65, y=15)
'''
plus = Label(data_frame, text='+', font='arial 14')
plus.place(x=123, y=10)
f = Entry(data_frame, width=10)
f.insert(0, '0')
f.place(x=145, y=15)
'''

# начальные условия 1
ny = Label(data_frame, text='н.у.: U(t=', font='arial 14')
ny.place(x=20, y=40)
tny = Entry(data_frame, width=3)
tny.insert(0, '0')
tny.place(x=100, y=45)
raw2 = Label(data_frame, text=')=', font='arial 14')
raw2.place(x=127, y=40)
fi = Entry(data_frame, width=10)
fi.insert(0, '0')
fi.place(x=155, y=45)

# начальные условия 2
ny2 = Label(data_frame, text='U', font='arial 14')
ny2.place(x=59, y=70)
t = Label(data_frame, text='t', font='arial 9')
t.place(x=74, y=77)
ys = Label(data_frame, text='(t=', font='arial 14')
ys.place(x=80, y=70)
t2 = Entry(data_frame, width='3')
t2.insert(0, '0')
t2.place(x=108, y=75)
raw3 = Label(data_frame, text=')=', font='arial 14')
raw3.place(x=133, y=70)
w = Entry(data_frame, width=10)
w.insert(0, '0')
w.place(x=161, y=75)

# граничные условия 1
gy = Label(data_frame, text='г.у.:  U(x=', font='arial 14')
gy.place(x=20, y=100)
x0 = Entry(data_frame, width='3')
x0.insert(0, '0')
x0.place(x=100, y=105)
raw4 = Label(data_frame, text=')=', font='arial 14')
raw4.place(x=125, y=100)
gam1 = Entry(data_frame, width=10)
gam1.insert(0, '0')
gam1.place(x=150, y=105)

# граничные условия 2
gy2 = Label(data_frame, text='U(x=', font='arial 14')
gy2.place(x=59, y=130)
x1 = Entry(data_frame, width='3')
x1.insert(0, '1')
x1.place(x=100, y=135)
raw5 = Label(data_frame, text=')=', font='arial 14')
raw5.place(x=125, y=130)
gam2 = Entry(data_frame, width=10)
gam2.insert(0, '0')
gam2.place(x=150, y=135)

# кнопки
draw_button = Button(data_frame, text='Нарисовать', width=10, height=1, font='arial 14')
draw_button.bind('<Button-1>', check_r)
draw_button.place(x=65, y=300)

# настройка сетки
srtka = Label(data_frame, text='Настрока сетки', font='arial 11')
srtka.place(x=20, y=160)
ti = Label(data_frame, text='Узлов по t', font='arial 14')
ti.place(x=20, y=180)
xi = Label(data_frame, text='Узлов по x', font='arial 14')
xi.place(x=20, y=210)
ti2 = Label(data_frame, text='Длительность', font='arial 14', )
ti2.place(x=20, y=240)
step_ti = Entry(data_frame, width=5)
step_ti.insert(0, '300')
step_ti.place(x=150, y=185)
step_xi = Entry(data_frame, width=5)
step_xi.insert(0, '50')
step_xi.place(x=150, y=215)
lat = Entry(data_frame, width=5)
lat.insert(0, '5')
lat.place(x=150, y=245)
rule = Label(data_frame, text='Усл. устойчивости (a*T*n/l/m)^2<1', font='arial 10')
rule.place(x=20, y=270)


data_frame.place(x=0, y=0)
root.mainloop()
