# -*- coding: utf-8 -*-
__author__ = 'I.B. Juan José Guzmán Cruz'

from base import getData
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns
sns.set_style("white")


# Características para las gráficas
params = {'legend.fontsize': 10,
          'figure.figsize': (18, 12),
         'axes.labelsize': 12,
         'axes.titlesize': 12,
         'xtick.labelsize': 12,
         'ytick.labelsize': 12}
plt.rcParams.update(params)


def analizarFrecuencias(inicio, fin):

    '''
    Se forman 5 distintos suggrupos de muestras para el análisis de frecuencia de los valores originales
    por cada rango de referencia. Finalmente las frecuencias obtenidas se grafican y guardan en un archivo .pdf.
    :param inicio: Desde que posición del vector de los datos originales se debe comenzar el análisis de frecuencia.
    :param fin: Hasta que posición del vector de los datos originales se debe realizar el análisis de frecuencia.
    :return:
    '''

    # INICIALIZACIÓN DE VARIABLES
    # Obtiene el diccionario de la base de conocimientos
    bc = getData()
    # Referencia para guardar el archivo .pdf con los gráficos de distribuión de frecuencias.
    pdf_frecuencias = PdfPages('./analisis_frecuencias/frecuencias.pdf')
    distribucion = open('./analisis_frecuencias/distribucion.txt', 'w')

    evaluados = []
    variables = []

    colors_list = ["red", "green", "orange", "blue", "yellow", "grey", "cyan", "indigo", "beige", "brown"]

    for marcador in bc:

        variables.append(marcador)

        distribucion.write('Valores de ' + str(marcador) + '\n')

        # Abre el archivo de texto plano con los valores originales del marcador en turno.
        valores = './valores/' + marcador + '.txt'
        f = open(valores, 'r')
        data = f.readline().split(',')
        y = [float(i) for i in data[inicio:fin]]
        eval = np.zeros(len(y))
        sticks = [0]
        colors_dict = {}

        # Variables locales para almacenar los distintos rangos de pertenencia según el número de muestras.
        group1 = {}
        group7 = {}
        group30 = {}
        group90 = {}
        group180 = {}
        group345 = {}

        # Variables locales para almacenar los distintos números de muestras.
        data7 = []
        data30 = []
        data90 = []
        data180 = []
        data345 = []

        # Variables locales para almacenar los distintos colores a utilizar en los gráficos.
        color1 = []
        color7 = []
        color30 = []
        color90 = []
        color180 = []
        color345 = []

        mem_x = []
        mem_y = []

        # Se forma un vector de valores originales de acuerdo al número de muestras necesarias.
        for n in range(len(y)):
            if n % 7 == 0:
                data7.append(y[n])
            if n % 30 == 0:
                data30.append(y[n])
            if n % 90 == 0:
                data90.append(y[n])
            if n % 180 == 0:
                data180.append(y[n])
            if n % 344 == 0:
                data345.append(y[n])

        # Fuzificación de los valores originales según el marcador en curso.
        # La fuzificación se lleva a cabo utilizando la ecuación de la recta para cada rango de pertenencia.
        for i in range(len(bc[marcador])-1):

            key = bc[marcador][i][0]
            group1[key] = []
            group7[key] = []
            group30[key] = []
            group90[key] = []
            group180[key] = []
            group345[key] = []

            # Asociar un color a cada rango de pertenencia
            colors_dict[key] = (colors_list[i])

            x1 = bc[marcador][i][1]
            x2 = bc[marcador][i][2]
            y1 = bc[marcador][i][3]
            y2 = bc[marcador][i][4]

            m = (y2 - y1) / (x2 - x1)
            b = y1 - m * x1

            sticks.append(x2)
            mem_x.append(x1)
            mem_x.append(x2)
            mem_y.append(y1)
            mem_y.append(y2)

            # Evaluación de los valores originales en sus respectivas funciones de membresía
            # según el número de muestras requerido.
            for n in range(len(y)):
                if y[n] >= x1 and y[n]<=x2:
                    val = m*y[n] + b
                    eval[n] = val
                    group1[key].append(val)
                    if n % 7 == 0:
                        group7[key].append(val)
                    if n % 30 == 0:
                        group30[key].append(val)
                    if n % 90 == 0:
                        group90[key].append(val)
                    if n % 180 == 0:
                        group180[key].append(val)
                    if n % 344 == 0:
                        group345[key].append(val)


        evaluados.append(eval)
        np.savetxt('./valoracion_difusa/' + marcador + '_evaluado.txt', eval, fmt='%f', delimiter=',')

        _y1 = []
        _y7 = []
        _y30 = []
        _y90 = []
        _y180 = []
        _y345 = []
        t1 = []
        t7 = []
        t30 = []
        t90 = []
        t180 = []
        t345 = []

        distribucion.write("Para un número de muestras = " + str(len(y)) + '\n')
        for g in group1:
            frecuency = len(group1[g])
            _y1.append(frecuency)
            t1.append(g)
            # Condición para utilizar un color haciendo referencia al rango de pertenencia
            if frecuency > 0: color1.append(colors_dict[g])
            distribucion.write(str(g) + " = " + str(frecuency) + " ocurrencias" + '\n')

        distribucion.write("Para un número de muestras = " + str(len(data7)) + '\n')
        for g in group7:
            frecuency = len(group7[g])
            _y7.append(frecuency)
            t7.append(g)
            # Condición para utilizar un color haciendo referencia al rango de pertenencia
            if frecuency > 0: color7.append(colors_dict[g])
            distribucion.write(str(g) + " = " + str(frecuency) + " ocurrencias" + '\n')

        distribucion.write("Para un número de muestras = " + str(len(data30)) + '\n')
        for g in group30:
            frecuency = len(group30[g])
            _y30.append(frecuency)
            t30.append(g)
            # Condición para utilizar un color haciendo referencia al rango de pertenencia
            if frecuency > 0: color30.append(colors_dict[g])
            distribucion.write(str(g) + " = " + str(frecuency) + " ocurrencias" + '\n')

        distribucion.write("Para un número de muestras = " + str(len(data90)) + '\n')
        for g in group90:
            frecuency = len(group90[g])
            _y90.append(frecuency)
            t90.append(g)
            # Condición para utilizar un color haciendo referencia al rango de pertenencia
            if frecuency > 0: color90.append(colors_dict[g])
            distribucion.write(str(g) + " = " + str(frecuency) + " ocurrencias" + '\n')

        distribucion.write("Para un número de muestras = " + str(len(data180)) + '\n')
        for g in group180:
            frecuency = len(group180[g])
            _y180.append(frecuency)
            t180.append(g)
            # Condición para utilizar un color haciendo referencia al rango de pertenencia
            if frecuency > 0: color180.append(colors_dict[g])
            distribucion.write(str(g) + " = " + str(frecuency) + " ocurrencias" + '\n')

        distribucion.write("Para un número de muestras = " + str(len(data345)) + '\n')
        for g in group345:
            frecuency = len(group345[g])
            _y345.append(frecuency)
            t345.append(g)
            # Condición para utilizar un color haciendo referencia al rango de pertenencia
            if frecuency > 0: color345.append(colors_dict[g])
            distribucion.write(str(g) + " = " + str(frecuency) + " ocurrencias" + '\n')

        # -------------
        # Estadística
        # -------------
        distribucion.write('valores de referencia: ' + str(sticks) + '\n')
        distribucion.write('varianza (valores) = ' + str(np.var(y)) + '\n')
        distribucion.write('varianza (evaluación) = ' + str(np.var(eval)) + '\n')
        distribucion.write('\n\n')

        # -------------
        # Gráficas
        # -------------

        # Primera gráfica
        # Gráfico de los valores originales con el total de muestras.
        plt.figure(1)
        plt.subplot2grid((3, 4), (0, 0))
        st = sticks
        plt.yticks(st, t1)
        plt.grid(True)
        plt.ylim(0, sticks[-1])
        plt.plot(y)

        aux = plt.twinx()
        aux.set_yticks(sticks)
        aux.set_ylim(0, sticks[-1])
        aux.plot(y)
        plt.title(marcador + " con " + str(len(y)) + " muestras.")

        # Segunda gráfica
        # Gráfico para la distribución del total de los valores originales según los rangos de pertenencia.
        plt.subplot2grid((3, 4), (0, 1))
        pv1 = []
        pt1 = []
        for j, k in zip(_y1, t1):
            if j != 0:
                pv1.append(j)
                pt1.append(k)
        plt.pie(pv1, wedgeprops={'linewidth': 3, 'edgecolor': 'white'}, autopct='%1.2f%%',
                shadow=True, startangle=90, colors=color1)
        plt.legend(pt1, loc=3)

        my_circle = plt.Circle((0, 0), 0.5, color='white')
        p = plt.gcf()
        p.gca().add_artist(my_circle)
        plt.axis('equal')
        plt.title(marcador + " evaluados con " + str(len(y)) + " muestras.")


        '''
        Los siguientes gráficos muestran los valores originales con el total de muestras requerido
        junto con su distribución.
        Por ejemplo, data7 significa que el vector resultante se formó, tomando un valor cada 7 muestras
        del vector original.
        '''

        # Tercera gráfica datos data7
        plt.subplot2grid((3, 4), (0, 2))
        st = sticks
        plt.yticks(st)
        plt.grid(True)
        plt.ylim(0, sticks[-1])
        plt.plot(data7, marker='o', linestyle=':', linewidth=1, markersize=3)
        plt.title(marcador + " con " + str(len(data7)) + " muestras.")

        # Cuarta gráfica distribución data7
        plt.subplot2grid((3, 4), (0, 3))
        pv7 = []
        pt7 = []
        for j, k in zip(_y7, t7):
            if j != 0:
                pv7.append(j)
                pt7.append(k)
        plt.pie(pv7, wedgeprops={'linewidth': 3, 'edgecolor': 'white'}, autopct='%1.2f%%',
                shadow=True, startangle=90, colors=color7)
        plt.legend(pt7, loc=3)

        my_circle = plt.Circle((0, 0), 0.5, color='white')
        p = plt.gcf()
        p.gca().add_artist(my_circle)

        plt.axis('equal')
        plt.title(marcador + " evaluados con " + str(len(data7)) + " muestras.")

        # Quinta gráfica datos data30
        plt.subplot2grid((3, 4), (1, 0))
        st = sticks
        plt.yticks(st)
        plt.grid(True)
        plt.ylim(0, sticks[-1])
        plt.plot(data30, marker='o', linestyle=':', linewidth=1, markersize=3)
        plt.title(marcador + " con " + str(len(data30)) + " muestras.")

        # Sexta gráfica distribución data30
        plt.subplot2grid((3, 4), (1, 1))
        pv30 = []
        pt30 = []
        for j, k in zip(_y30, t30):
            if j != 0:
                pv30.append(j)
                pt30.append(k)
        plt.pie(pv30, wedgeprops={'linewidth': 3, 'edgecolor': 'white'}, autopct='%1.2f%%',
                shadow=True, startangle=90, colors=color30)
        plt.legend(pt30, loc=3)

        my_circle = plt.Circle((0, 0), 0.5, color='white')
        p = plt.gcf()
        p.gca().add_artist(my_circle)

        plt.axis('equal')
        plt.title(marcador + " evaluados con " + str(len(data30)) + " muestras.")

        # Séptima gráfica datos data90
        plt.subplot2grid((3, 4), (1, 2))
        st = sticks
        plt.yticks(st)
        plt.grid(True)
        plt.ylim(0, sticks[-1])
        plt.plot(data90, marker='o', linestyle=':', linewidth=1, markersize=3)
        plt.title(marcador + " con " + str(len(data90)) + " muestras.")

        # Octava gráfica datos data90
        plt.subplot2grid((3, 4), (1, 3))
        pv90 = []
        pt90 = []
        for j, k in zip(_y90, t90):
            if j != 0:
                pv90.append(j)
                pt90.append(k)
        plt.pie(pv90, wedgeprops={'linewidth': 3, 'edgecolor': 'white'}, autopct='%1.2f%%',
                shadow=True, startangle=90, colors=color90)
        plt.legend(pt90, loc=3)

        my_circle = plt.Circle((0, 0), 0.5, color='white')
        p = plt.gcf()
        p.gca().add_artist(my_circle)

        plt.axis('equal')
        plt.title(marcador + " evaluados con " + str(len(data90)) + " muestras.")

        # Novena gráfica datos data180
        plt.subplot2grid((3, 4), (2, 0))
        st = sticks
        plt.yticks(st)
        plt.grid(True)
        plt.ylim(0, sticks[-1])
        plt.plot(data180, marker='o', linestyle=':', linewidth=1, markersize=3)
        plt.title(marcador + " con " + str(len(data180)) + " muestras.")

        # Décima gráfica distribución data180
        plt.subplot2grid((3, 4), (2, 1))
        pv180 = []
        pt180 = []
        for j, k in zip(_y180, t180):
            if j != 0:
                pv180.append(j)
                pt180.append(k)
        plt.pie(pv180, wedgeprops={'linewidth': 3, 'edgecolor': 'white'}, autopct='%1.2f%%',
                shadow=True, startangle=90, colors=color180)
        plt.legend(pt180, loc=3)

        my_circle = plt.Circle((0, 0), 0.5, color='white')
        p = plt.gcf()
        p.gca().add_artist(my_circle)

        plt.axis('equal')
        plt.title(marcador + " evaluados con " + str(len(data180)) + " muestras.")

        # Décima primera gráfica datos data345
        plt.subplot2grid((3, 4), (2, 2))
        st = sticks
        plt.yticks(st)
        plt.grid(True)
        plt.ylim(0, sticks[-1])
        plt.plot(data345, marker='o', linestyle=':', linewidth=1, markersize=3)
        plt.title(marcador + " con " + str(len(data345)) + " muestras.")

        # Décima segunda gráfica distribución data345
        plt.subplot2grid((3, 4), (2, 3))
        pv345 = []
        pt345 = []
        for j, k in zip(_y345, t345):
            if j != 0:
                pv345.append(j)
                pt345.append(k)
        plt.pie(pv345, wedgeprops={'linewidth': 3, 'edgecolor': 'white'}, autopct='%1.2f%%',
                shadow=True, startangle=90, colors=color345)
        plt.legend(pt345, loc=3)

        my_circle = plt.Circle((0, 0), 0.5, color='white')
        p = plt.gcf()
        p.gca().add_artist(my_circle)

        plt.axis('equal')
        plt.title(marcador + " evaluados con " + str(len(data345)) + " muestras.")

        #plt.show()
        pdf_frecuencias.savefig()
        plt.close()

    pdf_frecuencias.close()
    distribucion.close()

#analizarFrecuencias(0, 345)


