# -*- coding: utf-8 -*-
__author__ = 'I.B. Juan José Guzmán Cruz'

from base import getData
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
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


def valorar(inicio, fin):

    '''
    A partir de los valores originales de cada marcador se obtienen:
    1. la función de membresía correspondiente a cada marcador,
    2. la evaluación de los valores originales en la función de membresía (valores ponderados),
    3. la distribución de los valores originales respecto a los rangos de pertenencia de cada marcador,
    4. el promedio de los valores ponderados,
    5. la valoración difusa de los valores ponderados.
    6. Se realiza un análisis estadístico de los valores originales y ponderados que es guardado en un
       archivo de texto plano.
    Los valores originales junto con los resultados de los puntos 1, 2 y 3 se grafican en un archivo .pdf.
    Los valores obtenidos en los puntos 4 y 5 se grafican en un segundo archivo .pdf.
    :param inicio: Desde que posición del vector de los datos originales se debe comenzar la valoración difusa.
    :param fin: Hasta que posición del vector de los datos originales se debe realizar la valoración difusa.
    :return:
    '''

    # INICIALIZACIÓN DE VARIABLES
    # Obtiene el diccionario de la base de conocimientos
    bc = getData()
    # Referencia para guardar el archivo .pdf con los gráficos de fuzificación.
    pdf_fuzificacion = PdfPages('./valoracion_difusa/fuzificacion.pdf')
    # Referencia para guardar el archivo .pdf con los gráficos de valoración.
    pdf_valoracion = PdfPages('./valoracion_difusa/valoracion.pdf')
    # Abre para escritura un archivo de texto plano para guardar todos los valores
    # de análisis estadístico realizados sobre los valores originales y evaluados de los marcadores.
    calculos = open('./valoracion_difusa/estadistica.txt', 'w')
    # Abre para escritura un archivo de texto plano para guardar todos los valores
    # de valoración difusa calculados.
    valoracion_difusa = open('./valoracion_difusa/valoracion_difusa.txt', 'w')

    # Variables locales
    evaluados = []
    variables = []
    varianza = []
    varianza_evaluados = []
    unidades = []

    n = 1
    for marcador in bc:

        variables.append(marcador)
        calculos.write('Valores de ' + str(marcador) + '\n')

        # Abre el archivo de texto plano con los valores originales del marcador en turno.
        valores = './valores/' + marcador + '.txt'
        f = open(valores, 'r')
        data = f.readline().split(',')
        y = [float(i) for i in data[inicio:fin]]

        # Variables temporales para almacenar los valores evaluados, rangos de pertenencia (sticks),
        # distribuciones según el rango de pertenencia (group) y unidades, respectivamente.
        eval = np.zeros(len(y))
        sticks = [0]
        group = {}
        nr = len(bc[marcador])
        u = bc[marcador][nr - 1][0]
        unidades.append(u)
        mem_x = []
        mem_y = []

        # Fuzificación de los valores originales según el marcador en curso.
        # La fuzificación se lleva a cabo utilizando la ecuación de la recta para cada rango de pertenencia.
        for i in range(len(bc[marcador]) - 1):

            key = bc[marcador][i][0]
            group[key] = []

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
            for n in range(len(y)):
                if y[n] >= x1 and y[n]<=x2:
                    val = m*y[n] + b
                    eval[n] = val
                    group[key].append(val)

        evaluados.append(eval)
        np.savetxt('./valoracion_difusa/' + marcador + '_evaluado.txt', eval, fmt='%f', delimiter=',')

        # Calculo de la frecuencia para los valores de cada rango de pertenencia según el marcador en curso.
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

            calculos.write(str(title) + " = " + str(frecuency) + " ocurrencias" + '\n')

        # -------------
        # Cálculo estadístico
        # -------------

        maximo = max(y)
        minimo = min(y)
        mean = np.mean(y)
        desv = np.std(y)
        var = np.var(y)
        varianza.append(var)
        varianza_evaluados.append(np.var(eval)*1000)

        calculos.write('valores de referencia: ' + str(sticks) + '\n')
        calculos.write('máximo: ' + str(maximo) + '\n')
        calculos.write('mínimo: ' + str(minimo) + '\n')
        calculos.write('media  (valores) = ' + str(mean) + '\n')
        calculos.write('desviación estándar (valores) = ' + str(desv) + '\n')
        calculos.write('varianza (valores) = ' + str(var) + '\n')
        calculos.write('varianza (evaluación) = ' + str(np.var(eval)) + '\n')
        calculos.write('\n\n')

        # -------------
        # Gráficas
        # -------------

        # FIGURA 1
        # Primera gráfica
        # Grafico de los valores originales de acuerdo al marcador en curso.
        plt.figure(1)
        plt.subplot(221)
        st = sticks
        plt.yticks(st, t)
        plt.grid(True)
        plt.ylim(0, sticks[-1])
        plt.xlabel('días')
        plt.plot(y, label=marcador)
        plt.legend(loc='best')

        aux = plt.twinx()
        aux.set_yticks(sticks)
        aux.set_ylim(0, sticks[-1])
        aux.plot(y)

        plt.title("Valores de la variable " + marcador)
        plt.ylabel('$v_{}$'.format({str(n)}) + ' [' + u + ']')

        # Segunda gráfica
        # Grafico de la función de membresía de acuerdo al marcador en curso.
        plt.figure(1)
        plt.subplot(222)
        plt.title('Función de membresía para ' + marcador)
        plt.xlabel('Valores permitidos (y)')
        plt.ylabel('Ponderación (p) [U]')
        plt.grid(True)
        plt.plot(mem_x, mem_y)

        # Tercera gráfica
        # Grafico de los valores evaluado en la función de membresía de acuerdo al marcador en curso.
        plt.figure(1)
        plt.subplot(223)
        plt.title('Valores evaluados a través de la función de membresía de {}' .format(marcador))
        plt.xlabel('Valores permitidos (y)')
        plt.ylabel('Ponderación (p) [U]')
        plt.grid(True)
        plt.scatter(y, eval)

        # Cuarta gráfica
        # Grafico de la distribución de los  valores originales en los rangos de pertenencia
        # de acuerdo al marcador en curso.
        plt.figure(1)
        plt.subplot(224)
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

        n+=1
        # Se guardan los gráficos creados en el archivo .pdf y se cierra.
        pdf_fuzificacion.savefig()
        plt.close()

    # FIGURA 3
    # Gráfico de la varianza de los valores originales.
    plt.figure(3)
    plt.grid(True)
    pos = np.arange(len(varianza))
    plt.bar(pos, varianza)
    plt.xticks(pos, variables, rotation=90)
    plt.xlabel('Variables', fontsize=16)
    plt.ylabel('Varianza', fontsize=16)
    plt.title('Gráfico de la varianza de los valores originales', fontsize=20)

    # Texto sobre cada uno de los gráficos tipo barras.
    for i in range(len(varianza)):
        plt.text(x=float(pos[i]) - 0.3, y=varianza[i] + 10, s=float("{0:.2f}".format(varianza[i])), size=14)

    # Se guardan los gráficos creados en el archivo .pdf y se cierra.
    pdf_fuzificacion.savefig()
    plt.close()

    # FIGURA 4
    # Gráfico de la varianza de los valores evaluados en su respectiva función de membresía.
    plt.figure(4)
    plt.grid(True)
    pos_eval = np.arange(len(varianza_evaluados))
    plt.bar(pos_eval, varianza_evaluados)
    plt.xticks(pos_eval, variables, rotation=90)
    plt.xlabel('Variables', fontsize=16)
    plt.ylabel('Varianza e3', fontsize=16)
    plt.title('Gráfico de la varianza de los valores evaluados en su respectiva función de membresía', fontsize=20)

    # Texto sobre cada uno de los gráficos tipo barras.
    for i in range(len(varianza_evaluados)):
        plt.text(x=float(pos_eval[i]) - 0.3, y=varianza_evaluados[i] + 1, s=float("{0:.2f}".format(varianza_evaluados[i])), size=14)

    # Se guardan los gráficos creados en el archivo .pdf y se cierra.
    pdf_fuzificacion.savefig()
    plt.close()
    pdf_fuzificacion.close()
    calculos.close()

    # Crear matriz de coeficientes estimados de todas las variables.
    # Necesaria para llevar a cabo el promedio y la ponderación.
    matriz_evaluados = []
    for i in range(len(evaluados[0])):
        matriz_evaluados.append([])
        for j in range(len(evaluados)):
            matriz_evaluados[i].append(evaluados[j][i])

    # Calcular promedio.
    suma = []
    promedio = []
    for i in range(len(matriz_evaluados)):
        s = 0
        for j in range(len(matriz_evaluados[i])):
            s = s + matriz_evaluados[i][j]
        suma.append(s)
        prom = s / len(matriz_evaluados[1])

        promedio.append(prom)

    # Calcular ponderación.
    valoracion = []
    for p in promedio:
        if p >= 0.9 and p <= 1:
            v = 5
        elif p >= 0.8 and p < 0.9:
            v = 4
        elif p >= 0.7 and p < 0.8:
            v = 3
        elif p >= 0.6 and p < 0.7:
            v = 2
        elif p < 0.6:
            v = 1
        valoracion.append(v)

    for i in range(len(evaluados)):
        e = evaluados[i]

        # FIGURA 2
        # Primera gráfica
        # Grafico de lo valores evaluados en la respectiva función de membresía.
        plt.figure(2)
        plt.subplot(211)
        plt.grid(True)
        plt.plot(e, label=variables[i])
        plt.xlabel('días')
        plt.ylabel('p [U]')
        plt.title("Valores evaluados en función de membresía")
        plt.legend(bbox_to_anchor=(1.105, 1), loc=1, borderaxespad=0.)

    # FIGURA 2
    # Segunda gráfica
    # Grafico de lo valores ponderados en la respectiva función de membresía.
    plt.figure(2)
    plt.subplot(211)
    plt.grid(True)
    plt.plot(promedio, color='black', linestyle='dashed', label='promedio')
    plt.xlabel('días')
    plt.ylabel('p [U]')
    plt.title("Valores ponderados en función de membresía")
    plt.legend(bbox_to_anchor=(1.105, 1), loc=1, borderaxespad=0.)

    # FIGURA 2
    # Segunda gráfica
    # Grafico para representar la valoración difusa de los valores ponderados de todos los marcadores.
    plt.figure(2)
    plt.subplot(212)
    plt.grid(True)
    plt.plot(valoracion)
    plt.xlabel('días')
    plt.ylabel('escala de valoración [puntos]')
    plt.title("Valoración difusa")

    # Se guardan los gráficos creados en el archivo .pdf.
    plt.savefig('./valoracion_difusa/valoracion.png', bbox_inches='tight')
    pdf_valoracion.savefig(bbox_inches='tight')

    # Cierre de todos los gráficos y archivos.
    plt.close()
    pdf_valoracion.close()
    valoracion_difusa.write(str(valoracion)[1:-1])
    valoracion_difusa.close()

#valorar(0, 345)