genero=table(policia$GENERO)
n=31265
pm=22972/n
pm



### Hallar la probabilidad de que las denuncias de violencia intrafamiliar por genero femenino,
## superen el 80%


Z=(0.8-pm)/sqrt(n*pm*(1-pm))
pnorm(Z)


### Hallar el intervalo de confianza al 85% 

errorest=sqrt(pm*(1-pm)/n)
alpha=0.15/2

intder=pm-errorest*qnorm(alpha)
intizp=pm+errorest*qnorm(alpha)

