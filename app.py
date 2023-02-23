from flask import Flask, jsonify, request
from datetime import datetime

tiempo = datetime.today()

class Bloque:
    def __init__(self, index, transacciones, timestamp):
        self.index = index
        self.transacciones = transacciones
        self.timestamp = timestamp


class Blockchain:
    def __init__(self):
        self.transacciones_pendientes = []
        self.cadena = []
        # creamos el bloque genesis
        self.crear_bloque_genesis()

    #Lo siguiente seria crear una funcion que nos permita crear el bloque genesis. 
    #Para llamarlo al iniciar la blockchain.

    def crear_bloque_genesis(self):
        bloque_genesis = Bloque(0, ["Genesis"], tiempo)
        self.cadena.append(bloque_genesis)


    # Agregamos una propiedad a la cadena. 
    # Esta propiedad nos permite acceder al ultimo bloque

    @property
    def ultimo_bloque(self):
        return self.cadena[-1]
    
    # Luego creamos una funcion que nos permita agregar bloques a la cadena
    def agregar_bloque(self, bloque):
        self.cadena.append(bloque)
        return True
    
    # Una funcion que agregue las transacciones al bloque que queremos agregar
    def agregar_transaccion(self, transaccion):
        self.transacciones_pendientes.append(transaccion)

    # Por ultimo lo que debemos hacer es cerrar un bloque, para ello creamos una funcion
    # que cree un bloque con las transacciones pendientes y luego los agregue a la cadena de bloques.
    def cerrar_bloque(self):
        if not self.transacciones_pendientes:
            return False
        ultimo_bloque = self.ultimo_bloque
        nuevo_bloque = Bloque(ultimo_bloque.index + 1, self.transacciones_pendientes, tiempo)
        self.agregar_bloque(nuevo_bloque)
        self.transacciones_pendientes = []
        return nuevo_bloque
    


app = Flask(__name__)

pengucoin = Blockchain()


@app.route('/cerrar', methods=['GET'])
def mine():
    bloque = pengucoin.cerrar_bloque()
    response = {
        'mensaje': "Nuevo Bloque Cerrado",
        'index': bloque.index,
        'transacciones': bloque.transacciones,
        'timestamp': bloque.timestamp
    }
    return jsonify(response), 200

@app.route('/transaccion/nueva', methods=['POST'])
def nueva_transaccion():
    values = request.get_json()

    index = pengucoin.agregar_transaccion(values['transaccion'])

    response = {'mensaje': f'La transaccion se ha agregado correctamente.'}
    return jsonify(response), 201

@app.route('/cadena', methods=['GET'])
def cadena_completa():
    cadena = []
    for bloque in pengucoin.cadena:
        cadena.append(bloque.__dict__)
    response = {
        'cadena': cadena,
        'longitud': len(cadena)
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)