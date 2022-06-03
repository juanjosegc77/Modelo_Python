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


def graficar(inicio, fin):
    '''
    Se grafican los valores originales de los marcadores instanciados en la base de conocimientos.
    :param inicio: Desde que posición del vector de los datos originales se debe comenzar la graficación.
    :param fin: Hasta que posición del vector de los datos originales se debe realizar la graficación.
    :return:
    '''

    # INICIALIZACIÓN DE VARIABLES
    # Obtiene el diccionario de la base de conocimientos
    bc = getData()
    # Referencia para guardar el archivo .pdf con los gráficos creados.
    pdf_originales = PdfPages('./originales/originales.pdf')
    # Abre para escritura un archivo de texto plano para guardar cálculo estadísticos realizados con los
    # valores originales.
    estadistica = open('./originales/estadistica.txt', 'w')

    for marcador in bc:

        # Abre el archivo de texto plano con los valores originales del marcador en turno.
        valores = './valores/' + marcador + '.txt'
        f = open(valores, 'r')
        data = f.readline().split(',')
        y = [float(i) for i in data[inicio:fin]]

        # -------------
        # Estadística
        # -------------
        maximo = max(y)
        minimo = min(y)
        mean = np.mean(y)
        desv = np.std(y)
        var = np.var(y)

        estadistica.write('Valores estadísticos de : ' + marcador + '\n')
        estadistica.write('máximo = ' + str(maximo) + '\n')
        estadistica.write('mínimo = ' + str(minimo) + '\n')
        estadistica.write('media = ' + str(mean) + '\n')
        estadistica.write('desviación estándar = ' + str(desv) + '\n')
        estadistica.write('varianza = ' + str(var) + '\n')
        estadistica.write('\n\n')

        # Figura 1
        # Gráfico de los valores originales correspondientes al marcador en curso.
        plt.figure(1)
        plt.grid(True)
        plt.plot(y, label=marcador + " orig")
        plt.title('Valores originales de ' + marcador)
        plt.legend(bbox_to_anchor=(1.105, 1), loc=1, borderaxespad=0.)
        plt.savefig('./originales/' + marcador + '.png')

        pdf_originales.savefig(bbox_inches='tight')
        plt.close()

    plt.close()
    pdf_originales.close()

#graficar(0, 345)