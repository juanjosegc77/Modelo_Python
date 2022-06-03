# -*- coding: utf-8 -*-
__author__ = 'I.B. Juan José Guzmán Cruz'

import time
import originales
import filtrado_estocastico
import graficar_coeficientes
import analisis_coeficientes
import valoracion_difusa
import analisis_frecuencias
import graficas

start_time = time.time()

# El total de datos para los ejemplos utilizados es 345
inicio = 0
fin = 345
factor = 100

originales.graficar(inicio, fin)
filtrado_estocastico.calcMatriz_A(inicio, fin, factor)
graficar_coeficientes.graficarCoeficientes(inicio, fin)
analisis_coeficientes.analizarCoeficientes(inicio, fin, factor)
valoracion_difusa.valorar(inicio, fin)
analisis_frecuencias.analizarFrecuencias(inicio, fin)
graficas.graficar(inicio, fin)

print("--- %s segundos de tiempo de ejecución ---" % (time.time() - start_time))