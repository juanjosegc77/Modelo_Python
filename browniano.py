# -*- coding: utf-8 -*-
__author__ = 'I.B. Juan José Guzmán Cruz'


from pylab import *

p_inicial = 1		#valor inicial
H = 1				#parametro para el calculo de la cantidad de pasos
dt = 0.0027397			#tamaño del paso
sigma = 1		#volatilidad
mu = 1			#retono medio
nSimu = 1			#número de simulaciones

passos=round(H/dt); #pasos en días
S = zeros([nSimu, passos], dtype=float)
x = range(0, int(passos), 1)

f = open ('./browniano/browniano.txt','w')

for j in range(0, nSimu, 1):
        S[j,0]= p_inicial
        for i in x[:-1]:
                #S[j,i+1]=S[j,i]+S[j,i]*(mu-0.5*sigma*sigma)*dt+sigma*S[j,i]*sqrt(dt)*standard_normal();
                S[j, i + 1] = S[j, i] + S[j, i] * (mu - 0.5 * sigma * sigma) * dt + sigma * S[j, i] * sqrt(
                    dt) * standard_normal();
                f.write('%f,' % S[j, i + 1])
        plot(x, S[j])
        plt.savefig('./browniano/browniano.png', bbox_inches='tight')

f.close()

title('Simulación para %d días con valor inicial de %.2f' % (int(passos), p_inicial))
xlabel('Días')
ylabel('Valores permitidos')
show()