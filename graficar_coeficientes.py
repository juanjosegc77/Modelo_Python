# -*- coding: utf-8 -*-
__author__ = 'I.B. Juan José Guzmán Cruz'

from base import getData
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Características para las gráficas
params = {'legend.fontsize': 20,
          'figure.figsize': (20, 12),
         'axes.labelsize': 20,
         'axes.titlesize': 24,
         'xtick.labelsize': 20,
         'ytick.labelsize': 20}
plt.rcParams.update(params)


def graficarCoeficientes(inicio, fin):

    '''
    Grafica los coeficientes estimados por el filtro estocástico. Los valores deben estar
    disponibles en archivos de texto plano en la carpeta /filtrado/coeficientes/.
    :param inicio: Desde que posición del vector de los coeficientes estimados se debe comenzar a graficar.
    :param fin: Hasta que posición del vector de los coeficientes estimados se debe graficar.
    :return:
    '''

    # INICIALIZACIÓN DE VARIABLES
    # Obtiene el diccionario de la base de conocimientos
    bc = getData()
    # Referencia para guardar el archivo .pdf con los gráficos de todos los coeficientes estimados.
    pdf = PdfPages('./analisis_coeficientes/coeficientes.pdf')
    labels = []

    n = 0
    for marcador in bc:

        '''
        Se crea un gráfico de los coeficientes estimados para cada uno de los marcadores en la
        base de conocimientos y un gráfico con los coeficientes estimados sobrepuestos de todos
        los marcadores.
        '''

        labels.append(marcador)

        # Se abre el archivo de texto plano con los valores de los coeficientes estimados para el
        # marcador en curso y se almacenan en un vector de tipo float.
        coeficientes_path = './filtrado/coeficientes_' + marcador + '.txt'
        coeficientes = open(coeficientes_path, 'r')
        data = coeficientes.readline().split(',')
        ak = [float(i) for i in data[0:]]

        # Gráfico de los coeficientes estimados del marcador en turno.
        plt.figure(1)
        plt.grid(True)
        plt.plot(ak, label="coeficientes")
        plt.title('Coeficientes estimados para ' + marcador)
        plt.legend(bbox_to_anchor=(1.105, 1), loc=1, borderaxespad=0.)

        n += 1
        # Gráficos de coeficientes estimados guardados en el .pdf.
        pdf.savefig(bbox_inches='tight')
        plt.close()

        # Gráfico de los coeficientes estimados del marcador en turno para ser guardados
        # en forma sobrepuesta en el archivo .pdf.
        plt.figure(2)
        plt.grid(True)
        plt.plot(ak, label='coeficientes de ' + marcador)
        plt.title('Coeficientes de la matriz de transición para el conjunto de señales')
        plt.legend(bbox_to_anchor=(1.105, 1), loc=1, borderaxespad=0.)

    # Gráfico de los coeficientes estimados sobrepuestos guardados en el archivo .pdf.
    pdf.savefig(bbox_inches='tight')

    # Cierre de todos los gráficos y archivos.
    plt.close()
    pdf.close()
    coeficientes.close()

graficarCoeficientes(0,345)