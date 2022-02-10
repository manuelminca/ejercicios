Para este ejercicio, revisar:
* [el concepto de una transacción](https://en.wikipedia.org/wiki/Database_transaction)
* [with statement](https://docs.python.org/3/whatsnew/2.6.html#pep-343-the-with-statement), el mecanismo de context management de python
* [los context managers son una buena forma de gestionar transacciones](https://docs.python.org/3/library/sqlite3.html#using-the-connection-as-a-context-manager)

### ejercicio

Estamos a cargo del backend de una empresa que copia el modelo de [Bizum](https://bizum.es/en/): permite hacer transferencias de dinero entre usuarios.

El código está escrito en python y se encuentra en el directorio [backend](backend).

Nuestro backend está escrito en sqlite y además no usa multithreading, así que su comportamiento debería ser fácil de analizar. Tenemos una cobertura de tests unitarios decente:

```bash
python3 -m unittest discover backend
```

Pese a que todo parece sencillo y normal, observamos de vez en cuando un comportamiento raro: hay quejas de usuarios que mandan dinero que nunca llega a su destino. El dinero sí que desaparece de la cuenta del usuario que lo envía y nos acusan de robárselo.

Hemos observado que el número de quejas de este tipo está muy correlado con los apagones de luz. Nuestro CTO decidió ahorrar costes, y nuestro server de backend está hospedado en un datacenter que regularmente sufre interrupciones en el suministro eléctrico.

Nuestro CTO también decidió ahorrar al contratar programadores, y la verdad es que ninguno sabe mucho de SQL pero a uno le suena que había un concepto llamado **transacción** que igual tenía que ver con el comportamiento observado.

Creemos que el problema se encuentra en la función `savings_backend.transfer(conn, user_a, user_b, transfer_amount)`

#### pregunta 1

¿Qué crees que está pasando?

Lo que está pasando es que el usuario 1 está enviando el dinero, se hace la transacción de quitar el dinero en la cuenta al usuario 1 correctamente pero cuando
va a insertar el dinero en el usuario 2 se pierde la conexión por la caída de la luz. Por lo que el primer usuario pierde el dinero y el segundo no lo recibe.

#### pregunta 2

¿Cómo reescribirías la función `savings_backend.transfer(conn, user_a, user_b, transfer_amount)` para eliminar el bug sin tener que cambiar a un datacenter bueno?

Asegúrate de que sigue pasando los tests unitarios con `python3 -m unittest discover backend`




### Cursor vs Connection
1. The connection has one purpose: controlling access to the database.

3. The cursor has one purpose: keeping track of where we are in the database so that if several programs are accessing the database at the same time, the database can keep track of who is trying to do what.
