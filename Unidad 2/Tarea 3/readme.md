detectorDeSpam.py funciona con un DataSet que contiene mensajes más cortos por lo que se ejecuta más rápido; pero la relación entre mensajes spam (747) y no spam  (4827) es muy grande, por lo que es menos preciso y más probable que clasifique erroneamente mensajes de spam como no spam.

detectorDeSpamConAssasin.py utiliza el DataSet de spam_assassin, cuyos mensajes son muy largos, por lo que tarda más tiempo en entrenar el modelo y ejecutarse, pero la relación entre correos spam (1896) y no spam (3900) es más equilibrada, por lo que su modelo es más preciso.

detectorDeSpamConAssasinManual.py es una prueba inconclusa en la que intentamos calcular el método de Bayes de forma manual.
