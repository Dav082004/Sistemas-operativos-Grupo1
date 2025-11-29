"""
Blockchain Educativo - Implementación Base
==========================================
Sistema de blockchain distribuido con Python y Flask

Componentes:
- Bloques con hash SHA-256
- Proof of Work (PoW)
- Consenso por cadena más larga
- Red distribuida con múltiples nodos
"""

import hashlib
import json
from time import time
from urllib.parse import urlparse
from uuid import uuid4
import requests
from flask import Flask, jsonify, request


class Bloque:
    """
    Representa un bloque individual en la blockchain.
    
    Atributos:
        indice: Posición del bloque en la cadena
        timestamp: Momento de creación del bloque
        transacciones: Lista de transacciones incluidas
        prueba: Proof of Work (número que satisface la condición)
        hash_previo: Hash SHA-256 del bloque anterior
    """
    
    def __init__(self, indice, timestamp, transacciones, prueba, hash_previo):
        self.indice = indice
        self.timestamp = timestamp
        self.transacciones = transacciones
        self.prueba = prueba
        self.hash_previo = hash_previo

    def to_dict(self):
        """Convierte el bloque a diccionario para serialización"""
        return {
            'indice': self.indice,
            'timestamp': self.timestamp,
            'transacciones': self.transacciones,
            'prueba': self.prueba,
            'hash_previo': self.hash_previo,
        }


class Blockchain:
    """
    Implementación de la estructura Blockchain completa.
    
    Funcionalidades:
    - Creación de bloques enlazados
    - Algoritmo Proof of Work
    - Consenso distribuido
    - Validación de cadena
    """
    
    def __init__(self):
        self.cadena = []
        self.transacciones_pendientes = []
        self.nodos = set()
        
        # Crear bloque génesis (primer bloque)
        print("Inicializando blockchain...")
        self.nuevo_bloque(hash_previo='1', prueba=100)
        print(f"Bloque génesis creado. Cadena iniciada con {len(self.cadena)} bloque(s).")

    def registrar_nodo(self, direccion):
        """
        Añade un nuevo nodo a la red distribuida.
        
        Args:
            direccion: URL del nodo (ej: 'http://192.168.0.5:5000')
        """
        url_parseada = urlparse(direccion)
        if url_parseada.netloc:
            self.nodos.add(url_parseada.netloc)
        elif url_parseada.path:
            self.nodos.add(url_parseada.path)
        else:
            raise ValueError('URL de nodo inválida')
        
        print(f"Nodo registrado: {direccion}")

    def validar_cadena(self, cadena):
        """
        Verifica la validez de una cadena blockchain.
        
        Validaciones:
        1. Hash del bloque anterior coincide
        2. Proof of Work es válido
        
        Args:
            cadena: Lista de bloques a validar
            
        Returns:
            bool: True si la cadena es válida, False en caso contrario
        """
        bloque_anterior = cadena[0]
        indice_actual = 1

        while indice_actual < len(cadena):
            bloque = cadena[indice_actual]
            print(f"Validando bloque {indice_actual}...")
            
            # Verificar hash del bloque anterior
            hash_anterior = self.hash(bloque_anterior)
            if bloque['hash_previo'] != hash_anterior:
                print(f"Error: Hash previo no coincide en bloque {indice_actual}")
                return False

            # Verificar Proof of Work
            if not self.prueba_valida(bloque_anterior['prueba'], 
                                      bloque['prueba'], 
                                      hash_anterior):
                print(f"Error: Proof of Work inválido en bloque {indice_actual}")
                return False

            bloque_anterior = bloque
            indice_actual += 1

        return True

    def resolver_conflictos(self):
        """
        Algoritmo de consenso: Regla de la cadena más larga.
        
        Reemplaza la cadena actual si existe una más larga y válida
        en la red distribuida.
        
        Returns:
            bool: True si la cadena fue reemplazada, False en caso contrario
        """
        vecinos = self.nodos
        nueva_cadena = None
        longitud_maxima = len(self.cadena)

        print(f"Verificando consenso con {len(vecinos)} nodos...")

        # Consultar todos los nodos de la red
        for nodo in vecinos:
            try:
                respuesta = requests.get(f'http://{nodo}/cadena', timeout=5)

                if respuesta.status_code == 200:
                    longitud = respuesta.json()['longitud']
                    cadena = respuesta.json()['cadena']

                    # Verificar si es más larga y válida
                    if longitud > longitud_maxima and self.validar_cadena(cadena):
                        longitud_maxima = longitud
                        nueva_cadena = cadena
                        print(f"Cadena más larga encontrada en nodo {nodo}: {longitud} bloques")
            except requests.exceptions.RequestException as e:
                print(f"Error conectando con nodo {nodo}: {e}")
                continue

        # Actualizar cadena si se encontró una mejor
        if nueva_cadena:
            self.cadena = nueva_cadena
            print("Cadena actualizada por consenso")
            return True

        print("Cadena actual es autoritativa")
        return False

    def nuevo_bloque(self, prueba, hash_previo=None):
        """
        Crea un nuevo bloque y lo añade a la cadena.
        
        Args:
            prueba: Número que satisface el Proof of Work
            hash_previo: Hash del bloque anterior (opcional)
            
        Returns:
            Bloque: El nuevo bloque creado
        """
        bloque = Bloque(
            indice=len(self.cadena) + 1,
            timestamp=time(),
            transacciones=self.transacciones_pendientes,
            prueba=prueba,
            hash_previo=hash_previo or self.hash(self.cadena[-1].to_dict()),
        )

        # Resetear transacciones pendientes
        self.transacciones_pendientes = []
        self.cadena.append(bloque)
        
        print(f"Bloque {bloque.indice} añadido a la cadena")
        return bloque

    def nueva_transaccion(self, emisor, receptor, cantidad):
        """
        Añade una nueva transacción al pool de transacciones pendientes.
        
        Args:
            emisor: Dirección del emisor
            receptor: Dirección del receptor
            cantidad: Cantidad a transferir
            
        Returns:
            int: Índice del bloque que contendrá esta transacción
        """
        self.transacciones_pendientes.append({
            'emisor': emisor,
            'receptor': receptor,
            'cantidad': cantidad,
        })

        return self.ultimo_bloque.indice + 1

    @property
    def ultimo_bloque(self):
        """Retorna el último bloque de la cadena"""
        return self.cadena[-1]

    @staticmethod
    def hash(bloque):
        """
        Genera hash SHA-256 de un bloque.
        
        Args:
            bloque: Diccionario representando el bloque
            
        Returns:
            str: Hash hexadecimal del bloque
        """
        bloque_string = json.dumps(bloque, sort_keys=True).encode()
        return hashlib.sha256(bloque_string).hexdigest()

    def proof_of_work(self, ultimo_bloque):
        """
        Algoritmo Proof of Work (PoW).
        
        Encuentra un número p' tal que hash(pp'h) contenga 4 ceros iniciales,
        donde p es la prueba anterior, p' es la nueva prueba, y h es el hash anterior.
        
        Args:
            ultimo_bloque: Último bloque de la cadena
            
        Returns:
            int: Prueba válida encontrada
        """
        ultima_prueba = ultimo_bloque.prueba
        ultimo_hash = self.hash(ultimo_bloque.to_dict())

        prueba = 0
        print("Ejecutando Proof of Work...", end="")
        
        while self.prueba_valida(ultima_prueba, prueba, ultimo_hash) is False:
            prueba += 1
            if prueba % 100000 == 0:
                print(".", end="", flush=True)

        print(f"\nProof of Work completado. Prueba encontrada: {prueba}")
        return prueba

    @staticmethod
    def prueba_valida(ultima_prueba, prueba, ultimo_hash):
        """
        Valida la Proof of Work.
        
        Args:
            ultima_prueba: Prueba del bloque anterior
            prueba: Prueba actual a validar
            ultimo_hash: Hash del bloque anterior
            
        Returns:
            bool: True si la prueba es válida
        """
        intento = f'{ultima_prueba}{prueba}{ultimo_hash}'.encode()
        hash_intento = hashlib.sha256(intento).hexdigest()
        return hash_intento[:4] == "0000"


# Inicializar aplicación Flask
app = Flask(__name__)

# Generar identificador único para este nodo
identificador_nodo = str(uuid4()).replace('-', '')

# Instanciar blockchain
blockchain = Blockchain()


@app.route('/minar', methods=['GET'])
def minar():
    """
    Endpoint para minar un nuevo bloque.
    
    Proceso:
    1. Ejecutar Proof of Work
    2. Recompensar al minero
    3. Crear nuevo bloque
    
    Returns:
        JSON con información del bloque minado
    """
    print("\n--- INICIANDO MINADO ---")
    
    # Ejecutar PoW
    ultimo_bloque = blockchain.ultimo_bloque
    prueba = blockchain.proof_of_work(ultimo_bloque)

    # Recompensa por minar
    blockchain.nueva_transaccion(
        emisor="0",
        receptor=identificador_nodo,
        cantidad=1,
    )

    # Crear nuevo bloque
    hash_previo = blockchain.hash(ultimo_bloque.to_dict())
    bloque = blockchain.nuevo_bloque(prueba, hash_previo)

    respuesta = {
        'mensaje': "Nuevo bloque minado",
        'indice': bloque.indice,
        'transacciones': bloque.transacciones,
        'prueba': bloque.prueba,
        'hash_previo': bloque.hash_previo,
    }
    
    print("--- MINADO COMPLETADO ---\n")
    return jsonify(respuesta), 200


@app.route('/transacciones/nueva', methods=['POST'])
def nueva_transaccion():
    """
    Endpoint para crear una nueva transacción.
    
    Body esperado:
        {
            "emisor": "direccion_emisor",
            "receptor": "direccion_receptor",
            "cantidad": 100
        }
    
    Returns:
        JSON confirmando la transacción
    """
    valores = request.get_json()

    # Validar campos requeridos
    campos_requeridos = ['emisor', 'receptor', 'cantidad']
    if not all(campo in valores for campo in campos_requeridos):
        return 'Faltan valores requeridos', 400

    # Crear transacción
    indice = blockchain.nueva_transaccion(
        valores['emisor'],
        valores['receptor'],
        valores['cantidad']
    )

    respuesta = {
        'mensaje': f'Transacción será añadida al bloque {indice}'
    }
    return jsonify(respuesta), 201


@app.route('/cadena', methods=['GET'])
def cadena_completa():
    """
    Endpoint que retorna la blockchain completa.
    
    Returns:
        JSON con la cadena completa y su longitud
    """
    respuesta = {
        'cadena': [bloque.to_dict() for bloque in blockchain.cadena],
        'longitud': len(blockchain.cadena),
    }
    return jsonify(respuesta), 200


@app.route('/nodos/registrar', methods=['POST'])
def registrar_nodos():
    """
    Endpoint para registrar nuevos nodos en la red.
    
    Body esperado:
        {
            "nodos": ["http://localhost:5001", "http://localhost:5002"]
        }
    
    Returns:
        JSON con lista de nodos registrados
    """
    valores = request.get_json()
    nodos = valores.get('nodos')
    
    if nodos is None:
        return "Error: Lista de nodos inválida", 400

    for nodo in nodos:
        blockchain.registrar_nodo(nodo)

    respuesta = {
        'mensaje': 'Nuevos nodos registrados',
        'nodos_totales': list(blockchain.nodos),
    }
    return jsonify(respuesta), 201


@app.route('/nodos/resolver', methods=['GET'])
def consenso():
    """
    Endpoint para ejecutar algoritmo de consenso.
    
    Aplica la regla de la cadena más larga para resolver
    conflictos entre nodos.
    
    Returns:
        JSON indicando si la cadena fue reemplazada
    """
    print("\n--- EJECUTANDO CONSENSO ---")
    reemplazada = blockchain.resolver_conflictos()

    if reemplazada:
        respuesta = {
            'mensaje': 'Cadena reemplazada',
            'nueva_cadena': [bloque.to_dict() for bloque in blockchain.cadena]
        }
    else:
        respuesta = {
            'mensaje': 'Cadena autoritativa',
            'cadena': [bloque.to_dict() for bloque in blockchain.cadena]
        }

    print("--- CONSENSO COMPLETADO ---\n")
    return jsonify(respuesta), 200


@app.route('/', methods=['GET'])
def info():
    """
    Endpoint de información del nodo.
    
    Returns:
        JSON con información básica del nodo
    """
    respuesta = {
        'mensaje': 'Blockchain Educativo - Nodo Activo',
        'nodo_id': identificador_nodo,
        'bloques': len(blockchain.cadena),
        'endpoints': {
            'minar': '/minar',
            'nueva_transaccion': '/transacciones/nueva',
            'cadena': '/cadena',
            'registrar_nodos': '/nodos/registrar',
            'consenso': '/nodos/resolver'
        }
    }
    return jsonify(respuesta), 200


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--puerto', default=5000, type=int, 
                       help='Puerto para el servidor')
    args = parser.parse_args()
    puerto = args.puerto

    print("\n" + "="*60)
    print("BLOCKCHAIN EDUCATIVO - SISTEMA DISTRIBUIDO")
    print("="*60)
    print(f"\nNodo ID: {identificador_nodo}")
    print(f"Puerto: {puerto}")
    print(f"\nServidor iniciado en: http://localhost:{puerto}")
    print("\nEndpoints disponibles:")
    print("  GET  /           - Información del nodo")
    print("  GET  /cadena     - Ver blockchain completa")
    print("  GET  /minar      - Minar nuevo bloque")
    print("  POST /transacciones/nueva - Crear transacción")
    print("  POST /nodos/registrar     - Registrar nodos")
    print("  GET  /nodos/resolver      - Ejecutar consenso")
    print("\n" + "="*60 + "\n")

    app.run(host='0.0.0.0', port=puerto, debug=True, use_reloader=False)
