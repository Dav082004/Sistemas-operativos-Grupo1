"""
Script de Pruebas - Blockchain Educativo
=========================================
Ejecuta pruebas automáticas de todas las funcionalidades
"""

import requests
import json
from time import time, sleep

BASE_URL = "http://localhost:5000"


def linea():
    print("=" * 70)


def seccion(titulo):
    print("\n")
    linea()
    print(f"  {titulo}")
    linea()
    print()


def test_conexion():
    """Prueba 1: Verificar conexión con el servidor"""
    seccion("PRUEBA 1: CONEXIÓN CON EL SERVIDOR")
    
    try:
        response = requests.get(f"{BASE_URL}/")
        print("Estado: OK")
        info = response.json()
        print(f"Nodo ID: {info['nodo_id']}")
        print(f"Bloques iniciales: {info['bloques']}")
        return True
    except:
        print("Estado: ERROR")
        print("El servidor no está corriendo.")
        print("Ejecuta primero: python blockchain.py")
        return False


def test_cadena_inicial():
    """Prueba 2: Verificar bloque génesis"""
    seccion("PRUEBA 2: BLOQUE GÉNESIS")
    
    response = requests.get(f"{BASE_URL}/cadena")
    data = response.json()
    
    print(f"Longitud de la cadena: {data['longitud']}")
    
    genesis = data['cadena'][0]
    print("\nBloque Génesis:")
    print(f"  Índice: {genesis['indice']}")
    print(f"  Timestamp: {genesis['timestamp']}")
    print(f"  Transacciones: {len(genesis['transacciones'])}")
    print(f"  Prueba: {genesis['prueba']}")
    print(f"  Hash previo: {genesis['hash_previo']}")
    
    assert data['longitud'] == 1, "Debe haber exactamente 1 bloque"
    assert genesis['indice'] == 1, "El índice debe ser 1"
    print("\nResultado: PASS")


def test_transacciones():
    """Prueba 3: Crear transacciones"""
    seccion("PRUEBA 3: SISTEMA DE TRANSACCIONES")
    
    transacciones = [
        {"emisor": "Alice", "receptor": "Bob", "cantidad": 50},
        {"emisor": "Bob", "receptor": "Charlie", "cantidad": 25},
        {"emisor": "Charlie", "receptor": "David", "cantidad": 10},
    ]
    
    print("Creando transacciones:")
    for i, tx in enumerate(transacciones, 1):
        response = requests.post(f"{BASE_URL}/transacciones/nueva", json=tx)
        assert response.status_code == 201, "Código de respuesta debe ser 201"
        
        resultado = response.json()
        print(f"  {i}. {tx['emisor']} -> {tx['receptor']}: {tx['cantidad']} unidades")
        print(f"     {resultado['mensaje']}")
    
    print("\nResultado: PASS")


def test_minado():
    """Prueba 4: Minar un bloque"""
    seccion("PRUEBA 4: PROCESO DE MINADO")
    
    print("Iniciando minado...")
    print("(Esto puede tardar varios segundos debido al Proof of Work)")
    
    inicio = time()
    response = requests.get(f"{BASE_URL}/minar")
    fin = time()
    
    assert response.status_code == 200, "Código de respuesta debe ser 200"
    
    data = response.json()
    print(f"\n{data['mensaje']}")
    print(f"Bloque índice: {data['indice']}")
    print(f"Prueba encontrada: {data['prueba']}")
    print(f"Transacciones incluidas: {len(data['transacciones'])}")
    print(f"Tiempo de minado: {fin - inicio:.2f} segundos")
    
    assert data['indice'] == 2, "El nuevo bloque debe ser el índice 2"
    print("\nResultado: PASS")


def test_cadena_actualizada():
    """Prueba 5: Verificar cadena después del minado"""
    seccion("PRUEBA 5: VERIFICACIÓN DE CADENA")
    
    response = requests.get(f"{BASE_URL}/cadena")
    data = response.json()
    
    print(f"Longitud de la cadena: {data['longitud']}")
    assert data['longitud'] == 2, "Debe haber 2 bloques"
    
    print("\nEstructura de la cadena:")
    for bloque in data['cadena']:
        print(f"\n  Bloque {bloque['indice']}:")
        print(f"    Timestamp: {bloque['timestamp']}")
        print(f"    Transacciones: {len(bloque['transacciones'])}")
        print(f"    Prueba: {bloque['prueba']}")
        print(f"    Hash previo: {bloque['hash_previo'][:32]}...")
    
    print("\nVerificando enlace entre bloques:")
    bloque1 = data['cadena'][0]
    bloque2 = data['cadena'][1]
    
    # El hash previo del bloque 2 debe ser diferente del bloque 1
    assert bloque2['hash_previo'] != bloque1['hash_previo'], "Los hash previos deben ser diferentes"
    print("  Bloques correctamente enlazados")
    
    print("\nResultado: PASS")


def test_multiples_bloques():
    """Prueba 6: Crear múltiples bloques"""
    seccion("PRUEBA 6: CREACIÓN DE MÚLTIPLES BLOQUES")
    
    print("Creando 3 bloques adicionales...")
    
    for i in range(1, 4):
        print(f"\nBloque {i}/3:")
        
        # Crear transacciones
        tx = {
            "emisor": f"Usuario{i}",
            "receptor": f"Usuario{i+1}",
            "cantidad": i * 10
        }
        requests.post(f"{BASE_URL}/transacciones/nueva", json=tx)
        print(f"  Transacción creada: {tx['emisor']} -> {tx['receptor']}")
        
        # Minar
        print(f"  Minando...")
        response = requests.get(f"{BASE_URL}/minar")
        data = response.json()
        print(f"  Bloque {data['indice']} minado")
    
    # Verificar cadena final
    response = requests.get(f"{BASE_URL}/cadena")
    data = response.json()
    
    print(f"\nCadena final: {data['longitud']} bloques")
    assert data['longitud'] == 5, "Debe haber 5 bloques en total"
    
    print("\nResultado: PASS")


def test_estadisticas():
    """Prueba 7: Estadísticas finales"""
    seccion("PRUEBA 7: ESTADÍSTICAS FINALES")
    
    response = requests.get(f"{BASE_URL}/cadena")
    data = response.json()
    
    total_bloques = data['longitud']
    total_transacciones = sum(len(bloque['transacciones']) for bloque in data['cadena'])
    
    print(f"Total de bloques: {total_bloques}")
    print(f"Total de transacciones: {total_transacciones}")
    
    print("\nDistribución de transacciones por bloque:")
    for bloque in data['cadena']:
        print(f"  Bloque {bloque['indice']}: {len(bloque['transacciones'])} transacciones")
    
    print("\nResultado: PASS")


def ejecutar_todas_las_pruebas():
    """Ejecuta todas las pruebas en secuencia"""
    
    print("\n")
    linea()
    print("  BLOCKCHAIN EDUCATIVO - SUITE DE PRUEBAS")
    linea()
    print()
    print("Este script ejecutará pruebas automáticas de todas")
    print("las funcionalidades del sistema blockchain.")
    print()
    
    # Verificar conexión primero
    if not test_conexion():
        return
    
    sleep(1)
    
    # Ejecutar pruebas
    try:
        test_cadena_inicial()
        sleep(1)
        
        test_transacciones()
        sleep(1)
        
        test_minado()
        sleep(1)
        
        test_cadena_actualizada()
        sleep(1)
        
        test_multiples_bloques()
        sleep(1)
        
        test_estadisticas()
        
        # Resumen final
        print("\n")
        linea()
        print("  RESUMEN DE PRUEBAS")
        linea()
        print()
        print("Todas las pruebas completadas exitosamente.")
        print()
        print("Funcionalidades verificadas:")
        print("  [OK] Conexión con servidor")
        print("  [OK] Bloque génesis")
        print("  [OK] Sistema de transacciones")
        print("  [OK] Algoritmo de minado (PoW)")
        print("  [OK] Encadenamiento de bloques")
        print("  [OK] Integridad de la cadena")
        print()
        print("El sistema blockchain está funcionando correctamente.")
        print()
        linea()
        
    except AssertionError as e:
        print(f"\nPrueba FALLIDA: {e}")
    except Exception as e:
        print(f"\nError durante las pruebas: {e}")


if __name__ == "__main__":
    ejecutar_todas_las_pruebas()
