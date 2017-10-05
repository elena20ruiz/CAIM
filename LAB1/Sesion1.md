# Sessión 1: ElasticSearch and Zipf's and Heaps' laws
> Elena Ruiz Cano.

## 1. Resultados del Zipf's and Heaps tests.

### 1.1 Tests para Zipf's law

**PREPARACIÓN DEL TEST**

Para obtener un conjunto de resultados que tendrán como objetivo ser analizados para comprobar si la ley de Zipf se cumple, se ha modificado el fichero original _CountWords.py_.  Este script ordena alfabéticamente las palabras más usadas, ignorando términos que no forman parte de un diccionario.

**MODIFICACIÓN DE COUNTWORDS.PY**

En la modificación del fichero se hacen dos cosas. Por una banda se filtran las palabras que contienen números o puntos, dejando el for original que calcula las frecuencias de la siguiente manera:

>       for v in voc:
>            if not (v == int) and not contains_dots(v) and not contains_numbers(v):
>                if len(v)> 1:
>                    lpal.append((v.encode("utf8", "ignore"), voc[v]))

Por otra banda se ordenan las palabras por frecuencia de manera que el output será una lista ordenada por frecuencia de palabras.

>        results = {}
>        for pal, cnt in sorted(lpal, key=lambda x: x[0 if args.alpha else 1]):
>            #Es guarda per a cada paraula cuants cops esta
>            results[pal] = cnt
>        sortedWords = sorted(results, key=results.get, reverse = True)

**TRATANDO LOS RESULTADOS DEL TEST**

Una vez guardados los resultados en un fichero de texto, se pasa a analizar mediante R. Generando los siguientes gráficos que representa las palabras más usadas y la distribución según la ley de Zipf.

Observamos las plabras más reproducidas:
![Top 20 palabras más usadas](https://i.imgur.com/elZfysI.png)

**APROXIMANDO LOS PARAMETROS**

El objetivo es encontrar los mejores coeficientes de la fórmula de Zipf, que consta como la siguiente:

> f = c / (rank+b)^a

Se hace un seguido de transformaciones sobre la fórmula original para poder estimar los parámetros a,b y c. Para la estimación se decide tomar como valor b = 0, de manera que se puede hacer una estimación de la siguiente formula equivalente:

> log(f) = log( c) + a*log(rank)

Sabiendo que log(f) y log(rank) son unos valores conocidos, mediante el problema de mínimos cuadrados se resuelve con el siguiente procedimiento vía R:

>plot(res$logfreq, res$logrank, main = "Alpha distribution", xlab = "log rank", ylab = "log frequency")

>res.lm <- lm(logfreq ~ logrank, weights = freq, data = res)

>abline(res.lm)

>summary(res.lm)

![Distribución Freq vs Rank](https://i.imgur.com/MPOYKk7.png)

Con este procedimiento además se ha aconsegudo un R-squared de 0.9849 un valor que hace que la estimación se pueda considerar válida.

>             Estimate Std. Error t value Pr(>|t|)    
>       (Intercept) 18.8089194  0.0061551    3056   <2e-16 ***
>       logrank     -1.0937273  0.0009159   -1194   <2e-16 ***

>       Residual standard error: 5.937 on 21801 degrees of freedom
>       Multiple R-squared:  0.9849,	Adjusted R-squared:  0.9849 
>       F-statistic: 1.426e+06 on 1 and 21801 DF,  p-value: < 2.2e-16


**ANÁLISIS DE LOS RESULTADOS**

Transformando los coeficientes obtenidos a nuestra fórmula, se ha estimado finalmente los siguientes valores:

> a = log(18.808)
> b = 0
> c = -1.093

### 1.2 Tests para Heap's Law

**PREPARACIÓN DEL TEST**

Se quiere buscar los mejores parametros _k_ y _b_ para conseguir los valores tal que los resultados se distribuyan según la ley de Heap. La distribución se define de la siguiente manera:

> Ndifwords = k*Nwords^b

**MODIFICACIÓN DEL FICHERO**

El fichero se ha modificado de manera que para cada ejecución del fichero CountWords.py saque como resultado el total de palabras del documento y el total de palabras diferentes del documento.

**MUESTRA DE LOS RESULTADOS**

Los resultados conseguidos ejecutando el script desde los n documentos que tenemos a 1 documento són los siguientes:

**APROXIMACIÓN DE LOS PARÁMETROS**

De la fórmula original se transforma de la siguiente manera con el objetivo de estimar los parametros k y b con el mismo método que se ha hecho para la fórmula de Zipf.

> log(Ndifwords) = b*log(k*Nwords)

> (1/b)*log(Ndifwords) = log(k) + log(Nwords)

> log(Nwords) = -log(k) + (1/b)*log(Ndifwords)

Con el procedimiento de los mínimos cuadrados mediante R se ha conseguido los siguientes resultados:

>    plot(res2$logNw, res2$logNdifw, main = "Alpha distribution", xlab = "log rank", ylab = "log frequency")

>    res2.lm <- lm(logNw ~ logNdifw, weights = freq, data = res2)

>    abline(res2.lm)

>    summary(res2.lm)


**ANÁLISIS DE LOS RESULTADOS**
Transformando los coeficientes obtenidos a nuestra fórmula, se ha estimado finalmente los siguientes valores:

> k = 

> b = 




