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


def calcMatriz_A(inicio, fin, factor):

    '''
    Lleva a cabo la estimación de parámetros e identificación de las señales originales contra
    la señal estimada.
    Se grafican para cada señal: coeficientes estimados (ak), error de estimación e identificación
    (comparación entre la señal original y la señal obtenida con los coeficientes estimados).
    Los imagenes en formato .png son guardadas en la carpeta /fitrado/imagenes/
    Los valores obtenidos son guardados en archivos de texto plano en la carpeta /filtrado/
    Las imagenes en formato .pdf son guardadas en la carpeta /filtrado/
    :param inicio: Desde que posición del vector de los datos originales se debe comenzar la estimación.
    :param fin: Hasta que posición del vector de los datos originales se debe realizar la estimación.
    :param factor: Factor de escalamiento de los valores originales.
    :return:
    '''

    # INICIALIZACIÓN DE VARIABLES
    # Obtiene el diccionario de la base de conocimientos
    bc = getData()
    # Referencia para guardar el archivo .pdf con los gráficos superpuestos de todos los marcadores.
    pdf_filtrado_todo = PdfPages('./filtrado/filtrado_todos.pdf')
    # Abre para escritura un archivo de texto plano para guardar todos los valores de estimación calculados.
    calculos = open('./filtrado/filtrado_calculos.txt', 'w')
    # Abre para escritura un archivo de texto plano para guardar todos los errores de estimación calculados.
    error_data = open('./filtrado/filtrado_calculos.txt', 'w')
    variables = []
    coef = []
    var_originales = []
    var_coeficientes = []
    unidades = []

    n = 0
    for marcador in bc:
        '''
        Repetir para cada marcador definido en la base de conocimientos: la estimación paramétrica,
        el error de estimación y la identificación de las señales. Guardar sus respectivos datos
        calculados y gráficos. 
        '''

        # Referencia para guardar el archivo .pdf con los gráficos de estimación, error e identificación
        # para el marcador en turno.
        pdf_filtrado_uno = PdfPages('./filtrado/filtrado_' + marcador + '.pdf')

        # Abre para escritura un archivo de texto plano para guardar los valores de estimación calculados
        # del marcador en turno.
        coeficientes_path = './filtrado/coeficientes_' + marcador + '.txt'
        coeficientes = open(coeficientes_path, 'w')
        # Abre para escritura un archivo de texto plano para guardar los valores de error calculados
        # del marcador en turno.
        error_path = './filtrado/error de ' + marcador + '.txt'
        error_data = open(error_path, 'w')

        calculos.write('Valores de ' + str(marcador) + '\n')
        variables.append(marcador)

        # Abre el archivo de texto plano con los valores originales del marcador en turno.
        valores = './valores/' + marcador + '.txt'
        f = open(valores, 'r')
        data = f.readline().split(',')

        # Obtiene de la base de conocimientos, las unidades correspondientes al marcador en turno.
        nr = len(bc[marcador])
        u = bc[marcador][nr-1][0]
        unidades.append(u)

        '''
        Distintos tipos de normalización para los valores originales de los marcadores.
        '''
        # valores sin modificación
        #y = [float(i) for i in data[0:]]

        # valores normalizados con log base 10 +1
        #y = [math.log1p(float(i)) for i in data[inicio:fin]]

        # valores divididos entre 1000
        #y = [(float(i)/100) for i in data[0:]]

        # valores divididos entre longitud de data
        #y = [(float(i)/len(data[0:])) for i in data[0:]]
        #y = [(float(i) / len(data[inicio:fin])) for i in data[inicio:fin]]

        # Valores originales desde un inicio a un final, normalizados con un valor elegido (factor).
        y = [(float(i) / factor) for i in data[inicio:fin]]

        # Vectores temporales para almacenar los coeficientes estimados (ak), el error de estimación,
        # y valores de identificación para el marcador en turno, respectivamente.
        ak = []
        error = []
        y_est = []

        # Valores iniciales para los vectores de estimación e identificación.
        ak.append(0)
        ak.append(0)
        y_est.append(0)
        y_est.append(0)

        # Estimación e identificación parámetrica (cálculo de los coeficientes de la matriz de transición
        # y cálculo de la señal estimada).
        for i in range(len(y)):
            if i > 0:
                y_est.append((ak[i] * y_est[i - 1] + y[i]))  # identificación
                a = (1 / len(y)) * ((y_est[i] - y[i]) * y_est[i] + (i - 1) * ak[i - 1])  # estimación
                ak.append(a)

        # Cálculo del error de estimación.
        sum_error = 0
        for i in range(len(y)):
            error.append(y[i] - y_est[i])
            sum_error += error[i]
        ecm = sum_error / len(y)  # error cuadrático medio

        # Escritura de los valores calculados en los respectivos archivo de texto plano.
        coeficientes.write(str(ak)[1:-1])
        error_data.write(marcador + '\n')
        error_data.write(str(error) + '\n')
        calculos.write('y ' + str(y) + '\n')
        calculos.write('y_est ' + str(y_est) + '\n')

        # Factor de escalamiento para mejorar la visualización de los gráficos de varianza
        var_originales.append(np.var(y) * 1000)
        var_coeficientes.append(np.var(ak) * 1000000000)

        # FIGURA 1
        # Gráfico de los coeficientes estimados del marcador en turno.
        plot1 = plt.figure(1)
        plt.grid(True)
        plt.plot(ak[inicio:fin], label="ak")
        plt.title('Coeficientes de la matriz de transición para ' + marcador + " f=" + str(factor))
        plt.legend(bbox_to_anchor=(1.105, 1), loc=1, borderaxespad=0.)
        plt.xlabel('días')
        plt.ylabel('$ak \ v_{} $'.format({str(n)}) + ' [' + u + ']')
        plt.savefig('./filtrado/imagenes/ak_' + marcador + '.png', bbox_inches='tight')
        plt.close()

        # FIGURA 2
        # Gráfico para la identificación paramétrica (comparativa entre la señal original y
        # la señal estimada) del marcador en turno.
        plot2 = plt.figure(2)
        plt.grid(True)
        plt.plot(y[inicio:fin], label=marcador + " orig")
        plt.plot(y_est[inicio:fin], '--', label=marcador + " est")
        plt.title('Comparación entre señal original y estimada para ' + marcador + " f=" + str(factor))
        plt.legend(bbox_to_anchor=(1.105, 1), loc=1, borderaxespad=0.)
        plt.xlabel('días')
        plt.ylabel('$v_{} $'.format({str(n)}) + ' [' + u + ']')
        plt.savefig('./filtrado/imagenes/comp_' + marcador + '.png', bbox_inches='tight')
        plt.close()

        # FIGURA 3
        # Gráfico de los errores calculados en la estimación parámetrica del marcador en turno.
        plot3 = plt.figure(3)
        plt.grid(True)
        plt.plot(error[inicio:fin], label="error")
        plt.title('Error de estimación para ' + marcador + " donde el LMS = " + str(ecm) + " f=" + str(factor))
        plt.legend(bbox_to_anchor=(1.105, 1), loc=1, borderaxespad=0.)
        plt.xlabel('días')
        plt.ylabel('error ' + ' [' + u + ']')
        plt.savefig('./filtrado/imagenes/error_' + marcador + '.png', bbox_inches='tight')
        plt.close()

        n += 1
        # Gráficos de estimación, identificación y error guardados en archivo .pdf para el marcador en turno.
        pdf_filtrado_uno.savefig(plot1, bbox_inches='tight')
        pdf_filtrado_uno.savefig(plot2, bbox_inches='tight')
        pdf_filtrado_uno.savefig(plot3, bbox_inches='tight')
        pdf_filtrado_uno.close()

        # FIGURA 4
        # Gráficos de estimación, identificación y error para ser guardados en archivo .pdf, aunque
        # se crean para el marcador en turno, se guardarán todos los gráficos en un solo archivo.
        plt.figure(4)
        plt.subplot(311)
        plt.grid(True)
        plt.plot(ak[inicio:fin], label="ak")
        plt.title('Coeficientes de la matriz de transición para ' + marcador + " f=" + str(factor))
        plt.legend(bbox_to_anchor=(1.105, 1), loc=1, borderaxespad=0.)
        plt.xlabel('días')
        plt.ylabel('$ak \ v{}$'.format({str(n)}) + ' [' + u + ']')

        plt.subplot(312)
        plt.grid(True)
        plt.plot(y[inicio:fin], label=marcador + " orig")
        plt.plot(y_est[inicio:fin], '--', label=marcador + " est")
        plt.title('Comparación entre señal original y estimada para ' + marcador + " f=" + str(factor))
        plt.legend(bbox_to_anchor=(1.105, 1), loc=1, borderaxespad=0.)
        plt.xlabel('días')
        plt.ylabel('$v_{}$'.format({str(n)}) + ' [' + u + ']')

        plt.subplot(313)
        plt.grid(True)
        plt.plot(error[inicio:fin], label="error")
        plt.title('Error de estimación para ' + marcador + " donde el LMS = " + str(ecm) + " f=" + str(factor))
        plt.legend(bbox_to_anchor=(1.105, 1), loc=1, borderaxespad=0.)
        plt.xlabel('días')
        plt.ylabel('error ' + ' [' + u + ']')
        plt.savefig('./filtrado/imagenes/filtrado_' + marcador + '.png', bbox_inches='tight')
        plt.close()

        # FIGURA 5
        # Gráfico con los coeficientes estimados sobrepuestos, de todos los marcadores.
        plot5 = plt.figure(5)
        plt.grid(True)
        plt.plot(ak[inicio:fin], label=marcador)
        plt.title('Coeficientes de la matriz de transición para el conjunto de señales' + " f=" + str(factor))
        plt.legend(bbox_to_anchor=(1.105, 1), loc=1, borderaxespad=0.)
        plt.xlabel('días')
        plt.ylabel('ak ' + ' [' + u + ']')

        # FIGURA 6
        # Gráfico de la identificación paramétrica sobrepuesta, de todos los marcadores.
        plot6 = plt.figure(6)
        plt.grid(True)
        plt.plot(y[inicio:fin], label=marcador + " orig")
        plt.plot(y_est[inicio:fin], '--', label=marcador + " est")
        plt.title('Comparación entre señales originales y estimadas ' + " f=" + str(factor))
        plt.legend(bbox_to_anchor=(1.105, 1), loc=1, borderaxespad=0.)
        plt.xlabel('días')
        plt.ylabel('$v_{}$'.format({str(n)}) + ' [' + u + ']')

        # FIGURA 7
        # Gráfico con los errores calculados sobrepuestos, de todos los marcadores.
        plot7 = plt.figure(7)
        plt.grid(True)
        plt.plot(error[inicio:fin], label=marcador)
        plt.title('Error de estimación para el conjunto de señales' + " f=" + str(factor))
        plt.legend(bbox_to_anchor=(1.105, 1), loc=1, borderaxespad=0.)
        plt.xlabel('días')
        plt.ylabel('error ' + ' [' + u + ']')

    # Gráficos de estimaciones, identificaciones y errores sobrepuestos, guardados en
    # sus respectivos archivos .pdf.
    plot5.savefig('./filtrado/imagenes/ak_f' + str(factor) + '.png', bbox_inches='tight')
    plot6.savefig('./filtrado/imagenes/comp_f' + str(factor) + '.png', bbox_inches='tight')
    plot7.savefig('./filtrado/imagenes/error_f' + str(factor) + '.png', bbox_inches='tight')

    # Gráficos de estimaciones, identificaciones y errores sobrepuestos, guardados en un solo archivo .pdf.
    pdf_filtrado_todo.savefig(plot5, bbox_inches='tight')
    pdf_filtrado_todo.savefig(plot6, bbox_inches='tight')
    pdf_filtrado_todo.savefig(plot7, bbox_inches='tight')
    plt.close()

    # FIGURA 8
    # Gráfico del cálculo de la varianza para los valores originales de cada uno de los marcadores.
    plt.figure(8)
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

    pdf_filtrado_todo.savefig(bbox_inches='tight')
    plt.close()

    # FIGURA 9
    # Gráfico del cálculo de la varianza para los coeficientes estimados de cada uno de los marcadores.
    plt.figure(9)
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

    # Gráficos guardados en un solo archivo .pdf.
    pdf_filtrado_todo.savefig(bbox_inches='tight')

    # Cierre de todos los gráficos y archivos.
    plt.close()
    pdf_filtrado_todo.close()
    error_data.close()
    calculos.close()
    coeficientes.close()

#calcMatriz_A(0, 345, 100)