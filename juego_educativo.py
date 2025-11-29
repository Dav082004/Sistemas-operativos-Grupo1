"""
Juego Educativo - Blockchain Interactivo
=========================================
Simulación interactiva para aprender conceptos de blockchain
mediante un juego paso a paso.
"""

import requests
import json
from time import sleep

BASE_URL = "http://localhost:5000"


def linea_separadora(caracter="=", longitud=70):
    """Imprime una línea separadora"""
    print(caracter * longitud)


def titulo(texto):
    """Imprime un título destacado"""
    print("\n")
    linea_separadora()
    print(f"  {texto}")
    linea_separadora()
    print()


def pausa(segundos=2):
    """Pausa la ejecución con indicador visual"""
    for _ in range(segundos):
        print(".", end="", flush=True)
        sleep(1)
    print()


def verificar_conexion():
    """Verifica que el servidor blockchain esté activo"""
    try:
        response = requests.get(f"{BASE_URL}/", timeout=2)
        return True
    except:
        return False


def limpiar():
    """Simula limpieza de pantalla con saltos de línea"""
    print("\n" * 2)


def nivel_1_blockchain_basico():
    """
    Nivel 1: Introducción a Blockchain
    Conceptos: Cadena de bloques, bloque génesis
    """
    titulo("NIVEL 1: FUNDAMENTOS DE BLOCKCHAIN")
    
    print("Concepto: BLOCKCHAIN (Cadena de Bloques)")
    print("-" * 70)
    print("Blockchain es una cadena de bloques enlazados.")
    print("Cada bloque contiene:")
    print("  1. Índice (posición en la cadena)")
    print("  2. Timestamp (momento de creación)")
    print("  3. Transacciones (datos almacenados)")
    print("  4. Prueba (Proof of Work)")
    print("  5. Hash previo (enlace al bloque anterior)")
    print()
    
    input("Presiona ENTER para ver el bloque génesis...")
    
    response = requests.get(f"{BASE_URL}/cadena")
    data = response.json()
    
    print("\nBLOQUE GÉNESIS (Primer bloque):")
    print("-" * 70)
    bloque_genesis = data['cadena'][0]
    print(f"Índice: {bloque_genesis['indice']}")
    print(f"Timestamp: {bloque_genesis['timestamp']}")
    print(f"Transacciones: {len(bloque_genesis['transacciones'])}")
    print(f"Prueba: {bloque_genesis['prueba']}")
    print(f"Hash previo: {bloque_genesis['hash_previo']}")
    
    print("\n" + "=" * 70)
    print("NIVEL 1 COMPLETADO")
    print("Has aprendido: Estructura básica de blockchain")
    print("=" * 70)
    
    input("\nPresiona ENTER para continuar al siguiente nivel...")


def nivel_2_transacciones():
    """
    Nivel 2: Sistema de Transacciones
    Conceptos: Transacciones pendientes, pool de transacciones
    """
    titulo("NIVEL 2: SISTEMA DE TRANSACCIONES")
    
    print("Concepto: TRANSACCIONES")
    print("-" * 70)
    print("Las transacciones son transferencias de valor entre participantes.")
    print("Antes de ser confirmadas, van a un 'pool' de transacciones pendientes.")
    print("Se confirman cuando se minan en un nuevo bloque.")
    print()
    
    input("Presiona ENTER para crear transacciones...")
    
    transacciones = [
        {"emisor": "Alice", "receptor": "Bob", "cantidad": 50},
        {"emisor": "Bob", "receptor": "Charlie", "cantidad": 25},
        {"emisor": "Charlie", "receptor": "Alice", "cantidad": 10},
    ]
    
    print("\nCreando transacciones:")
    for i, tx in enumerate(transacciones, 1):
        print(f"\n{i}. {tx['emisor']} -> {tx['receptor']}: {tx['cantidad']} unidades")
        response = requests.post(
            f"{BASE_URL}/transacciones/nueva",
            json=tx
        )
        resultado = response.json()
        print(f"   Estado: {resultado['mensaje']}")
        pausa(1)
    
    print("\nIMPORTANTE:")
    print("Las transacciones están PENDIENTES.")
    print("Se incluirán en el próximo bloque que se mine.")
    
    print("\n" + "=" * 70)
    print("NIVEL 2 COMPLETADO")
    print("Has aprendido: Sistema de transacciones")
    print("=" * 70)
    
    input("\nPresiona ENTER para continuar al siguiente nivel...")


def nivel_3_proof_of_work():
    """
    Nivel 3: Proof of Work
    Conceptos: Minado, PoW, dificultad computacional
    """
    titulo("NIVEL 3: PROOF OF WORK (PRUEBA DE TRABAJO)")
    
    print("Concepto: PROOF OF WORK")
    print("-" * 70)
    print("El Proof of Work es un algoritmo de consenso.")
    print("Requiere encontrar un número (prueba) que satisfaga una condición:")
    print("  - El hash de (prueba_anterior + prueba + hash_anterior)")
    print("    debe empezar con '0000' (4 ceros)")
    print()
    print("Características:")
    print("  1. Difícil de encontrar (requiere muchos intentos)")
    print("  2. Fácil de verificar (solo un hash)")
    print("  3. Asegura la integridad de la blockchain")
    print()
    
    input("Presiona ENTER para minar un bloque...")
    
    print("\nIniciando proceso de minado...")
    print("(Esto puede tardar varios segundos)")
    print()
    
    from time import time
    inicio = time()
    response = requests.get(f"{BASE_URL}/minar")
    fin = time()
    
    data = response.json()
    
    print(f"\n{data['mensaje']}")
    print("-" * 70)
    print(f"Bloque índice: {data['indice']}")
    print(f"Prueba encontrada: {data['prueba']}")
    print(f"Hash previo: {data['hash_previo'][:32]}...")
    print(f"Transacciones incluidas: {len(data['transacciones'])}")
    print(f"Tiempo de minado: {fin - inicio:.2f} segundos")
    
    print("\nAnálisis:")
    print(f"Se probaron aproximadamente {data['prueba']} números")
    print("hasta encontrar uno válido.")
    print("Esto demuestra el 'trabajo' computacional requerido.")
    
    print("\n" + "=" * 70)
    print("NIVEL 3 COMPLETADO")
    print("Has aprendido: Proof of Work y minado")
    print("=" * 70)
    
    input("\nPresiona ENTER para continuar al siguiente nivel...")


def nivel_4_inmutabilidad():
    """
    Nivel 4: Inmutabilidad de Blockchain
    Conceptos: Enlace criptográfico, inmutabilidad
    """
    titulo("NIVEL 4: INMUTABILIDAD Y SEGURIDAD")
    
    print("Concepto: INMUTABILIDAD")
    print("-" * 70)
    print("Blockchain es inmutable: no se puede alterar sin detectarlo.")
    print()
    print("¿Por qué?")
    print("Cada bloque contiene el hash del bloque anterior.")
    print("Si cambias un bloque antiguo:")
    print("  1. Su hash cambia")
    print("  2. El siguiente bloque apunta a un hash incorrecto")
    print("  3. Toda la cadena posterior se invalida")
    print("  4. Todos los nodos detectan la manipulación")
    print()
    
    input("Presiona ENTER para ver la cadena completa...")
    
    response = requests.get(f"{BASE_URL}/cadena")
    data = response.json()
    
    print(f"\nBlockchain actual: {data['longitud']} bloques")
    print("-" * 70)
    
    for bloque in data['cadena']:
        print(f"\nBloque {bloque['indice']}:")
        print(f"  Transacciones: {len(bloque['transacciones'])}")
        print(f"  Prueba: {bloque['prueba']}")
        print(f"  Hash previo: {bloque['hash_previo'][:32]}...")
        if bloque['indice'] < data['longitud']:
            print("  |")
            print("  v  (enlazado por hash)")
    
    print("\nCada bloque está criptográficamente enlazado al anterior.")
    print("Esta estructura hace que la blockchain sea segura e inmutable.")
    
    print("\n" + "=" * 70)
    print("NIVEL 4 COMPLETADO")
    print("Has aprendido: Inmutabilidad y seguridad")
    print("=" * 70)
    
    input("\nPresiona ENTER para continuar al nivel final...")


def nivel_5_consenso_distribuido():
    """
    Nivel 5: Consenso Distribuido
    Conceptos: Red distribuida, consenso, cadena más larga
    """
    titulo("NIVEL 5: CONSENSO DISTRIBUIDO")
    
    print("Concepto: RED DISTRIBUIDA Y CONSENSO")
    print("-" * 70)
    print("En una blockchain real, hay múltiples nodos (computadoras).")
    print("Cada nodo tiene su propia copia de la blockchain.")
    print()
    print("¿Qué pasa si hay diferencias?")
    print("Se usa un algoritmo de CONSENSO:")
    print("  - Regla: La cadena MÁS LARGA es la válida")
    print("  - Todos los nodos adoptan la cadena más larga")
    print("  - Esto resuelve conflictos automáticamente")
    print()
    print("Simulación:")
    print("  Nodo 1 (tú): 2 bloques")
    print("  Nodo 2 (simulado): 5 bloques")
    print("  Nodo 3 (simulado): 3 bloques")
    print()
    print("Resultado: Todos adoptan la cadena del Nodo 2 (5 bloques)")
    print()
    
    print("VENTAJAS de la descentralización:")
    print("  1. No hay autoridad central")
    print("  2. Resistente a censura")
    print("  3. Tolerante a fallos (si un nodo cae, otros continúan)")
    print("  4. Transparente (todos pueden verificar)")
    print()
    
    print("Para hacer trampa, necesitarías:")
    print("  - Controlar más del 51% de la red")
    print("  - Minar más rápido que todos los demás combinados")
    print("  - En redes grandes (como Bitcoin), esto es prácticamente imposible")
    
    print("\n" + "=" * 70)
    print("NIVEL 5 COMPLETADO")
    print("Has aprendido: Consenso y red distribuida")
    print("=" * 70)
    
    input("\nPresiona ENTER para ver tu certificación...")


def mostrar_certificacion():
    """Muestra certificación de finalización"""
    limpiar()
    linea_separadora("=")
    print()
    print("           CERTIFICADO DE COMPLETACIÓN")
    print()
    linea_separadora("=")
    print()
    print("  Has completado exitosamente el curso:")
    print("  'BLOCKCHAIN EDUCATIVO CON PYTHON'")
    print()
    print("  Conocimientos adquiridos:")
    print()
    print("  [X] Estructura de blockchain")
    print("  [X] Sistema de transacciones")
    print("  [X] Algoritmo Proof of Work")
    print("  [X] Hash SHA-256 y encadenamiento")
    print("  [X] Inmutabilidad y seguridad")
    print("  [X] Consenso distribuido")
    print("  [X] Red de nodos")
    print()
    linea_separadora("=")
    print("\n")


def menu_libre():
    """Menú para interactuar libremente con la blockchain"""
    titulo("MODO LIBRE - EXPERIMENTACIÓN")
    
    print("Ahora puedes experimentar libremente con la blockchain.")
    print()
    
    while True:
        print("\nOpciones:")
        print("  1. Ver blockchain completa")
        print("  2. Crear transacción")
        print("  3. Minar bloque")
        print("  4. Ver estadísticas")
        print("  5. Salir")
        
        opcion = input("\nSelecciona una opción (1-5): ").strip()
        
        if opcion == "1":
            response = requests.get(f"{BASE_URL}/cadena")
            data = response.json()
            print(f"\nBlockchain: {data['longitud']} bloques")
            for bloque in data['cadena']:
                print(f"  Bloque {bloque['indice']}: {len(bloque['transacciones'])} transacciones")
        
        elif opcion == "2":
            print("\nCrear nueva transacción:")
            emisor = input("  Emisor: ")
            receptor = input("  Receptor: ")
            cantidad = input("  Cantidad: ")
            
            try:
                tx = {
                    "emisor": emisor,
                    "receptor": receptor,
                    "cantidad": int(cantidad)
                }
                response = requests.post(f"{BASE_URL}/transacciones/nueva", json=tx)
                print(f"  {response.json()['mensaje']}")
            except:
                print("  Error al crear transacción")
        
        elif opcion == "3":
            print("\nMinando bloque...")
            response = requests.get(f"{BASE_URL}/minar")
            data = response.json()
            print(f"  {data['mensaje']}")
            print(f"  Bloque {data['indice']} creado")
        
        elif opcion == "4":
            response = requests.get(f"{BASE_URL}/cadena")
            data = response.json()
            total_tx = sum(len(b['transacciones']) for b in data['cadena'])
            print(f"\nEstadísticas:")
            print(f"  Bloques: {data['longitud']}")
            print(f"  Transacciones totales: {total_tx}")
        
        elif opcion == "5":
            print("\nGracias por usar Blockchain Educativo")
            break
        
        else:
            print("\nOpción inválida")


def main():
    """Función principal del juego educativo"""
    
    # Verificar conexión
    if not verificar_conexion():
        titulo("ERROR DE CONEXIÓN")
        print("No se puede conectar con el servidor blockchain.")
        print()
        print("Solución:")
        print("  1. Abre otra terminal")
        print("  2. Ejecuta: python blockchain.py")
        print("  3. Luego vuelve a ejecutar este juego")
        print()
        input("Presiona ENTER para salir...")
        return
    
    # Pantalla de bienvenida
    limpiar()
    linea_separadora("=")
    print()
    print("      BLOCKCHAIN EDUCATIVO - JUEGO INTERACTIVO")
    print()
    linea_separadora("=")
    print()
    print("Aprende los conceptos fundamentales de blockchain")
    print("mediante una experiencia interactiva paso a paso.")
    print()
    print("Temas que aprenderás:")
    print("  - Estructura de bloques")
    print("  - Transacciones")
    print("  - Proof of Work")
    print("  - Inmutabilidad")
    print("  - Consenso distribuido")
    print()
    linea_separadora("=")
    print()
    
    input("Presiona ENTER para comenzar...")
    
    # Ejecutar niveles
    nivel_1_blockchain_basico()
    nivel_2_transacciones()
    nivel_3_proof_of_work()
    nivel_4_inmutabilidad()
    nivel_5_consenso_distribuido()
    
    # Certificación
    mostrar_certificacion()
    
    input("Presiona ENTER para el modo libre...")
    
    # Modo libre
    menu_libre()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nJuego interrumpido por el usuario.")
    except Exception as e:
        print(f"\nError: {e}")
        input("\nPresiona ENTER para salir...")
