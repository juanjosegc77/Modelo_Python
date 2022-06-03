# -*- coding: utf-8 -*-
__author__ = 'I.B. Juan José Guzmán Cruz'

from base import getData
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
sns.set_style("white")

# Características para las gráficas
params = {'legend.fontsize': 20,
          'figure.figsize': (20, 12),
         'axes.labelsize': 20,
         'axes.titlesize': 24,
         'xtick.labelsize': 20,
         'ytick.labelsize': 20,
          'font.size': 20}
plt.rcParams.update(params)

def graficar(inicio, fin):

    '''
    Crea y guarda las gráficas de: los valores originales, la función de membresía, los valores evaluados en la
    respectiva función de membresía (valores ponderados) y la distribución de los valores originales con base
    a los rangos de pertenencia.
    :param inicio: Desde que posición del vector de los datos originales se debe comenzar la graficación.
    :param fin: Hasta que posición del vector de los datos originales se debe realizar la graficación.
    :return:
    '''

    # INICIALIZACIÓN DE VARIABLES
    # Obtiene el diccionario de la base de conocimientos
    bc = getData()
    evaluados = []
    variables = []
    unidades = []
    num_graf = 0

    for marcador in bc:

        variables.append(marcador)

        # Abre el archivo de texto plano con los valores originales del marcador en turno.
        valores = './valores/' + marcador + '.txt'
        f = open(valores, 'r')
        data = f.readline().split(',')
        y = [float(i) for i in data[inicio:fin]]
        eval = np.zeros(len(y))

        # Obtiene de la base de conocimientos, las unidades correspondientes al marcador en turno.
        nr = len(bc[marcador])
        u = bc[marcador][nr - 1][0]
        unidades.append(u)

        # Variables locales
        sticks = [0]
        group = {}
        mem_x = []
        mem_y = []

        # Fuzificación de los valores originales según el marcador en curso.
        # La fuzificación se lleva a cabo utilizando la ecuación de la recta para cada rango de pertenencia.
        for i in range(len(bc[marcador])-1):

            key = bc[marcador][i][0]
            group[key] = []

            x1 = bc[marcador][i][1]
            x2 = bc[marcador][i][2]
            y1 = bc[marcador][i][3]
            y2 = bc[marcador][i][4]

            m = (y2 - y1) / (x2 - x1)
            b = y1 - m * x1

            if len(sticks) == 1:
                sticks.pop(0)
                sticks.append(x1)

            sticks.append(x2)
            mem_x.append(x1)
            mem_x.append(x2)
            mem_y.append(y1)
            mem_y.append(y2)
            for n in range(len(y)):
                if y[n] >= x1 and y[n]<=x2:
                    val = m*y[n] + b
                    eval[n] = val
                    group[key].append(val)

        evaluados.append(eval)

        _y = []
        r = []
        s = []
        t = []
        x = []
        i=0
        for g in group:
            x.append(i+1)
            frecuency = len(group[g])
            area = np.pi*((frecuency/2)**2)
            title = g

            _y.append(frecuency)
            s.append(area)
            r.append(frecuency/2)
            t.append(title)
            i+=1

        # -------------
        # Gráficas
        # -------------

        # FIGURA 1
        # Gráfico de los valores originales correspondientes al marcador en curso.
        # Primera gráfica
        plt.figure(1)
        st = sticks
        plt.yticks(st, t)
        plt.grid(True)
        plt.ylim(0, sticks[-1])
        plt.xlabel('días')
        plt.plot(y, label=marcador)
        plt.legend(loc='best')
        plt.ylim(min(sticks), max(sticks))

        aux = plt.twinx()
        aux.set_yticks(sticks)
        aux.set_ylim(0, sticks[-1])
        aux.set_ylim(min(sticks), max(sticks))
        aux.plot(y)

        plt.title("Valores de la señal " + marcador)
        plt.ylabel('$v_{}$'.format({num_graf}) + ' [' + u + ']')

        plt.savefig('./graficas/' + marcador.replace(" ", '_') + '_orig.png', bbox_inches='tight')
        plt.close()

        # Segunda gráfica
        # Gráfico de la función de membresía para el marcador en turno.
        plt.figure(2)
        plt.title('Función de membresía para ' + marcador)
        plt.xlabel('Valores permitidos (y)')
        plt.ylabel('Ponderación (p) [U]')
        plt.grid(True)
        plt.plot(mem_x, mem_y)
        plt.savefig('./graficas/' + marcador.replace(" ", '_') + '_mem.png', bbox_inches='tight')
        plt.close()

        # Tercera gráfica
        # Gráfico de los valores originales evaluados en la función de membresía (valores ponderados).
        plt.figure(3)
        plt.title('Valores evaluados a través de la función de membresía. {}' .format(marcador))
        plt.xlabel('Valores permitidos (y)')
        plt.ylabel('Ponderación (p) [U]')
        plt.grid(True)
        plt.scatter(y, eval)
        plt.savefig('./graficas/' + marcador.replace(" ", '_') + '_pond.png', bbox_inches='tight')
        plt.close()

        # Cuarta gráfica
        # Gráfico de la distribución de los valores originales con base a los rangos de pertenencia.
        plt.figure(4)
        pv = []
        pt = []
        for j, k in zip(_y, t):
            if j != 0:
                pv.append(j)
                pt.append(k)
        plt.pie(pv, labels=pt, wedgeprops={'linewidth': 3, 'edgecolor': 'white'}, autopct='%1.2f%%',
                shadow=True, startangle=90)

        my_circle = plt.Circle((0, 0), 0.5, color='white')
        p = plt.gcf()
        p.gca().add_artist(my_circle)

        plt.axis('equal')
        plt.title("Distribución tipo dona de {}".format(marcador))

        plt.savefig('./graficas/' + marcador.replace(" ", '_') + '_dist.png', bbox_inches='tight')
        plt.close()

        num_graf+=1

graficar(0, 345)