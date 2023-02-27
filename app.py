from flask import Flask, jsonify, request, render_template
from datetime import datetime
from hashlib import sha256
import time
import json

tiempo = time.time()

class Bloque:
    def __init__(self, index, transacciones, timestamp, hash_anterior, nonce=0):
        self.index = index
        self.transacciones = transacciones
        self.timestamp = timestamp
        self.hash_anterior = hash_anterior
        self.nonce = nonce
        
    def hasheador(self):
        bloque_string = json.dumps(self.__dict__, sort_keys=True)
        
        return sha256(bloque_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.transacciones_pendientes = []
        self.cadena = []
        # creamos el bloque genesis
        self.crear_bloque_genesis()

    #Lo siguiente seria crear una funcion que nos permita crear el bloque genesis. 
    #Para llamarlo al iniciar la blockchain.

    def crear_bloque_genesis(self):
        bloque_genesis = Bloque(0, ["Genesis"], tiempo, '0')
        bloque_genesis.hash = bloque_genesis.hasheador()
        self.cadena.append(bloque_genesis)


    # Agregamos una propiedad a la cadena. 
    # Esta propiedad nos permite acceder al ultimo bloque

    @property
    def ultimo_bloque(self):
        return self.cadena[-1]
    
    
    # Creamos la dificultad de la blockchain
    dificultad = 2
    def prueba_de_trabajo(self, bloque):
        bloque.nonce = 0
        bloque_hasheado = bloque.hasheador()
        while not bloque_hasheado.startswith('0' * Blockchain.dificultad):
            bloque.nonce += 1
            bloque_hasheado = bloque.hasheador()
        return bloque_hasheado
    
    # Luego creamos una funcion que nos permita agregar bloques a la cadena
    def agregar_bloque(self, bloque, prueba):
        hash_anterior = self.ultimo_bloque.hash
        if hash_anterior != bloque.hash_anterior:
            return False
        if not self.prueba_de_trabajo_validada(bloque, prueba):
            return False
        bloque.hash = prueba
        self.cadena.append(bloque)
        return True
    

    # valida la prueba de trabajo
    def prueba_de_trabajo_validada(self, bloque, hash_del_bloque):
        return(hash_del_bloque.startswith('0' * Blockchain.dificultad) and
               hash_del_bloque == bloque.hasheador())

    # Una funcion que agregue las transacciones al bloque que queremos agregar
    def agregar_transaccion(self, transaccion):
        self.transacciones_pendientes.append(transaccion)

    # Por ultimo lo que debemos hacer es cerrar un bloque, para ello creamos una funcion
    # que cree un bloque con las transacciones pendientes y luego los agregue a la cadena de bloques.
    def cerrar_bloque(self):
        if not self.transacciones_pendientes:
            return False
        
        ultimo_bloque = self.ultimo_bloque

        nuevo_bloque = Bloque(ultimo_bloque.index + 1, transacciones=self.transacciones_pendientes, timestamp=tiempo, hash_anterior=ultimo_bloque.hash)

        prueba = self.prueba_de_trabajo(nuevo_bloque)

        self.agregar_bloque(nuevo_bloque, prueba)

        self.transacciones_pendientes = []
        return nuevo_bloque.index
    


## Comienza el flask ##


app = Flask(__name__)

pengucoin = Blockchain()


@app.route('/cerrar', methods=['GET', 'POST'])
def minar():
    if request.method == 'POST':
        pengucoin.cerrar_bloque()
    return render_template('minar.html')

@app.route('/transaccion/nueva', methods=['GET', 'POST'])
def nueva_transaccion():
    if request.method == 'POST':
        transaccion = request.form['nueva_transaccion']
        nueva_transaccion = pengucoin.agregar_transaccion(transaccion)
        return render_template('transaccion_nueva.html'), nueva_transaccion
    return render_template('transaccion_nueva.html')

@app.route('/cadena', methods=['GET'])
def cadena_completa():
    cadena = []
    for bloque in pengucoin.cadena:
        cadena.append(bloque.__dict__)
    
    return render_template('cadena.html', cadena=cadena)
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)