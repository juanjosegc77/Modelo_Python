# -*- coding: utf-8 -*-
__author__ = 'I.B. Juan José Guzmán Cruz'

from base import getData
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages

# Características para las gráficas
params = {'legend.fontsize': 20,
          'figure.figsize': (20, 12),
         'axes.labelsize': 20,
         'axes.titlesize': 24,
         'xtick.labelsize': 20,
         'ytick.labelsize': 20}
plt.rcParams.update(params)


def analizarCoeficientes(inicio, fin, factor):

    '''
    Grafica los valores originales de los marcadores de la base de conocimientos
    sobrepuestos, utilizando distintos colores y marcas.
    Grafica los coeficientes estimados por el filtro estocástico sobrepuestos, utilizando
    distintos colores y marcas.
    Grafica los coeficientes estimados por el filtro estocástico elevados al cuadrado sobrepuestos,
    utilizando distintos colores y marcas.
    Grafica la superposición y convolución de los coeficientes estimados.
    Grafica la superposición y convolución de los coeficientes estimados al cuadrado.
    Grafica la varianza de los valores originales.
    Grafica la varianza de los coeficientes estimados.
    :param inicio: Desde que posición del vector de los coeficientes estimados se debe comenzar a graficar.
    :param fin: Hasta que posición del vector de los coeficientes estimados se debe graficar.
    :param factor: Factor de escalamiento de los valores originales.
    :return:
    '''

    # INICIALIZACIÓN DE VARIABLES
    # Obtiene el diccionario de la base de conocimientos
    bc = getData()
    # Referencia para guardar el archivo .pdf con los gráficos de todos los coeficientes estimados.
    pdf = PdfPages('./analisis_coeficientes/analisis_coeficientes.pdf')
    variables = []
    coef = []
    coef2 = []
    var_originales = []
    var_coeficientes = []

    colors_list = ["blue", "lightcoral", "maroon", "red", "darkorange", "chocolate", "yellow",
                   "lightgreen", "green", "turquoise", "deepskyblue", "violet", "darkorchid", "black"]
    marker_list = ['.', 'o', 'v', '_', 's', 'p', '*', 'h', '+', 'x', 'd', '<',
                   '.', 'o', 'v', '_', 's', 'p', '*', 'h', '+', 'x', 'd', '<']
    count = 0

    for marcador in bc:

        '''
        Se crea los gráficos para cada uno de los marcadores instanciados en la base de conocimientos.
        '''

        # Abre el archivo de texto plano con los valores originales del marcador en turno.
        valores = './valores/' + marcador + '.txt'
        f = open(valores, 'r')
        data = f.readline().split(',')

        # Normalización de los valores originales de los marcadores.
        y = [(float(i) / factor) for i in data[inicio:fin]]

        variables.append(marcador)

        # Abre el archivo de texto plano con los coeficientes estimados del marcador en turno.
        coeficientes_path = './filtrado/coeficientes_' + marcador + '.txt'
        coeficientes = open(coeficientes_path, 'r')
        data = coeficientes.readline().split(',')
        # Almacena de forma temporal los valores de los coeficientes estimados del marcador en turno.
        ak = [float(i) for i in data[0:]]
        coef.append(ak)
        # Almacena de forma temporal los valores de los coeficientes estimados al cuadrado del marcador en turno.
        ak2 = [float(i)*float(i) for i in data[0:]]
        coef2.append(ak2)

        # Factor de escalamiento para mejorar la visualización de los gráficos de varianza
        var_originales.append(np.var(y) * 1000)
        var_coeficientes.append(np.var(ak) * 1000000000)

        # FIGURA 1
        # Grafico para los valores originales sobrepuestos de todos los marcadores.
        plot1 = plt.figure(1)
        plt.grid(True)
        plt.plot(y, label=marcador, color=colors_list[count], marker=marker_list[count])
        plt.title('Valores originales del conjunto de señales' + " f=" + str(factor))
        plt.legend(bbox_to_anchor=(1.105, 1), loc=1, borderaxespad=0.)

        # FIGURA 2
        # Grafico para los coeficientes estimados sobrepuestos de todos los marcadores.
        plot2 = plt.figure(2)
        plt.grid(True)
        plt.plot(ak, label='coeficientes de ' + marcador, color=colors_list[count], marker=marker_list[count])
        plt.title('Coeficientes de la matriz de transición para el conjunto de señales' + " f=" + str(factor))
        plt.legend(bbox_to_anchor=(0.15, 1), loc=1, borderaxespad=0.)

        # FIGURA 3
        # Grafico para los coeficientes estimados al cuadrado sobrepuestos de todos los marcadores.
        plot3 = plt.figure(3)
        plt.grid(True)
        plt.plot(ak2, label='coeficientes de ' + marcador, color=colors_list[count], marker=marker_list[count])
        plt.title('Coeficientes al cuadrado de la matriz de transición para el conjunto de señales' + " f=" + str(factor))
        plt.legend(bbox_to_anchor=(0.15, 1), loc=1, borderaxespad=0.)

        count += 1

    # Se guardan los gráficos creados en el mismo archivo .pdf.
    pdf.savefig(plot1, bbox_inches='tight')
    pdf.savefig(plot2, bbox_inches='tight')
    pdf.savefig(plot3, bbox_inches='tight')
    plt.close()


    # Crear matriz de coeficientes de todas las variables.
    # Necesaria para graficar superposición y convolución.
    matriz_a = []
    for i in range(len(coef[0])):
        matriz_a.append([])
        for j in range(len(coef)):
            matriz_a[i].append(coef[j][i])

    # Obtener los valores de superposición (suma) y convolución (producto) de los coeficientes estimados.
    suma = []
    producto = []
    for i in range(len(matriz_a)):
        s = 0
        p = 1
        for j in range(len(matriz_a[i])):
            s = s+matriz_a[i][j]
            p = p*matriz_a[i][j]
        suma.append(s)
        producto.append(p)

    # FIGURA 4
    # Grafico de la superposición de los coeficientes estimados.
    plt.figure(4)
    plt.subplot(211)
    plt.grid(True)
    plt.plot(suma, label="superposición")
    plt.title('Análisis de coeficientes' + " f=" + str(factor))
    plt.legend(bbox_to_anchor=(1.105, 1), loc=1, borderaxespad=0.)

    # Grafico de la convolución de los coeficientes estimados.
    plt.figure(4)
    plt.subplot(212)
    plt.grid(True)
    plt.plot(producto, label="convolución")
    plt.title('Análisis de coeficientes' + " f=" + str(factor))
    plt.legend(bbox_to_anchor=(1.105, 1), loc=1, borderaxespad=0.)

    # Se guardan los gráficos creados en el mismo archivo .pdf.
    pdf.savefig(bbox_inches='tight')
    plt.close()

    # Crear matriz de coeficientes estimados al cuadrado.
    matriz_a2 = []
    for i in range(len(coef2[0])):
        matriz_a2.append([])
        for j in range(len(coef2)):
            matriz_a2[i].append(coef2[j][i])

    # Obtener los valores de superposición (suma) y convolución (producto) de los coeficientes estimados al cuadrado.
    suma2 = []
    producto2 = []
    for i in range(len(matriz_a2)):
        s2 = 0
        p2 = 1
        for j in range(len(matriz_a2[i])):
            s2 = s2 + matriz_a2[i][j]
            p2 = p2 * matriz_a2[i][j]
        suma2.append(s2)
        producto2.append(p2)

    # FIGURA 5
    # Grafico de la superposición de los coeficientes estimados al cuadrado.
    plt.figure(5)
    plt.subplot(211)
    plt.grid(True)
    plt.plot(suma2, label="superposición")
    plt.title('Análisis de coeficientes al cuadrado' + " f=" + str(factor))
    plt.legend(bbox_to_anchor=(1.105, 1), loc=1, borderaxespad=0.)

    # Grafico de la convolución de los coeficientes estimados al cuadrado.
    plt.figure(5)
    plt.subplot(212)
    plt.grid(True)
    plt.plot(producto2, label="convolución")
    plt.title('Análisis de coeficientes al cuadrado' + " f=" + str(factor))
    plt.legend(bbox_to_anchor=(1.105, 1), loc=1, borderaxespad=0.)

    # Se guardan los gráficos creados en el mismo archivo .pdf.
    pdf.savefig(bbox_inches='tight')
    plt.close()

    # FIGURA 6
    # Grafico de la varianza de los valores originales de todos los marcadores.
    plt.figure(6)
    plt.grid(True)
    pos = np.arange(len(var_originales))
    plt.bar(pos, var_originales)
    plt.xticks(pos, variables, rotation=90)
    plt.xlabel('Variables', fontsize=16)
    plt.ylabel('Varianza e+3', fontsize=16)
    plt.title('Gráfico de varianzas de los valores originales' + " f=" + str(factor), fontsize=20)

    # Texto sobre cada uno de los gráficos tipo barras
    for i in range(len(var_originales)):
        plt.text(x=float(pos[i]) - 0.3, y=var_originales[i] + 0.1, s=float("{0:.2f}".format(var_originales[i])),
                 size=14)

    # Se guardan los gráficos creados en el mismo archivo .pdf.
    pdf.savefig(bbox_inches='tight')
    plt.close()

    # FIGURA 7
    # Grafico de la varianza de los coeficientes estimados de todos los marcadores.
    plt.figure(7)
    plt.grid(True)
    pos = np.arange(len(var_coeficientes))
    plt.bar(pos, var_coeficientes)
    plt.xticks(pos, variables, rotation=90)
    plt.xlabel('Variables', fontsize=16)
    plt.ylabel('Varianza e+9', fontsize=16)
    plt.title('Gráfico de varianzas de los coeficientes estimados' + " f=" + str(factor), fontsize=20)

    # Texto sobre cada uno de los gráficos tipo barras
    for i in range(len(var_coeficientes)):
        plt.text(x=float(pos[i]) - 0.3, y=var_coeficientes[i] + 0.1, s=float("{0:.2f}".format(var_coeficientes[i])),
                 size=14)

    # Se guardan los gráficos creados en el mismo archivo .pdf.
    pdf.savefig(bbox_inches='tight')
    # Cierre de todos los gráficos y archivos.
    plt.close()
    pdf.close()

#analizarCoeficientes(0,345,100)