# Blockchain Educativo con Python

Implementación completa de una red blockchain distribuida desde cero usando Python, Flask y sockets. Proyecto educativo que demuestra los conceptos fundamentales de blockchain mediante un juego interactivo.

---

## Descripción del Proyecto

Este proyecto implementa un sistema blockchain funcional que cumple con todos los requisitos técnicos especificados:

- **Red blockchain distribuida** desde cero
- **Python y Flask** como tecnologías base
- **Hash SHA-256** para integridad criptográfica
- **Proof of Work (PoW)** como algoritmo de consenso
- **Sockets/HTTP** para comunicación entre nodos
- **JSON** para serialización de datos

### Componentes Implementados

1. **Estructura de Bloques**: Cada bloque contiene índice, timestamp, transacciones, prueba (PoW) y hash previo
2. **Encadenamiento Criptográfico**: Los bloques están enlazados mediante hash SHA-256
3. **Sistema de Transacciones**: Pool de transacciones pendientes que se confirman al minar
4. **Algoritmo Proof of Work**: Minado con dificultad configurable (4 ceros por defecto)
5. **Consenso Distribuido**: Regla de la cadena más larga para resolver conflictos
6. **Red de Nodos**: Múltiples nodos pueden comunicarse y sincronizarse

---

## Requisitos del Sistema

### Software Necesario

- Python 3.7 o superior
- pip (gestor de paquetes de Python)

### Dependencias Python

```
flask==3.0.0
requests==2.31.0
```

---

## Instalación

### 1. Clonar o Descargar el Proyecto

Descarga todos los archivos en una carpeta local.

### 2. Instalar Dependencias

```powershell
pip install flask requests
```

O usando el archivo de requisitos:

```powershell
pip install -r requirements.txt
```

---

## Estructura del Proyecto

```
Sistemas-operativos-/
│
├── blockchain.py           # Implementación principal del blockchain
├── juego_educativo.py      # Interfaz interactiva educativa
├── test_blockchain.py      # Suite de pruebas automáticas
├── requirements.txt        # Dependencias del proyecto
├── README.md              # Esta documentación
└── GUIA_TECNICA.md        # Guía técnica detallada
```

---

## Guía de Uso

### Modo 1: Sistema Básico

**Paso 1: Iniciar el servidor blockchain**

```powershell
python blockchain.py
```

El servidor iniciará en `http://localhost:5000`

**Paso 2: Interactuar mediante navegador o Postman**

- Ver blockchain: `http://localhost:5000/cadena`
- Minar bloque: `http://localhost:5000/minar`
- Info del nodo: `http://localhost:5000/`

---

### Modo 2: Juego Educativo Interactivo (RECOMENDADO)

**Terminal 1: Iniciar servidor**
```powershell
python blockchain.py
```

**Terminal 2: Iniciar juego**
```powershell
python juego_educativo.py
```

El juego guía al usuario a través de 5 niveles educativos:

1. **Nivel 1**: Fundamentos de blockchain
2. **Nivel 2**: Sistema de transacciones
3. **Nivel 3**: Proof of Work y minado
4. **Nivel 4**: Inmutabilidad y seguridad
5. **Nivel 5**: Consenso distribuido

Al completar, otorga un certificado y acceso a modo libre.

---

### Modo 3: Pruebas Automáticas

**Terminal 1: Iniciar servidor**
```powershell
python blockchain.py
```

**Terminal 2: Ejecutar pruebas**
```powershell
python test_blockchain.py
```

Ejecuta 7 pruebas automáticas que verifican todas las funcionalidades.

---

### Modo 4: Red Distribuida (Avanzado)

Para simular una red blockchain con múltiples nodos:

**Terminal 1: Nodo 1**
```powershell
python blockchain.py -p 5000
```

**Terminal 2: Nodo 2**
```powershell
python blockchain.py -p 5001
```

**Terminal 3: Nodo 3**
```powershell
python blockchain.py -p 5002
```

**Registrar nodos entre sí** (usar Postman o curl):

```bash
POST http://localhost:5000/nodos/registrar
Content-Type: application/json

{
  "nodos": ["http://localhost:5001", "http://localhost:5002"]
}
```

**Ejecutar consenso**:
```
GET http://localhost:5000/nodos/resolver
```

---

## API REST Endpoints

### GET /

Información básica del nodo

**Respuesta:**
```json
{
  "mensaje": "Blockchain Educativo - Nodo Activo",
  "nodo_id": "abc123...",
  "bloques": 1,
  "endpoints": {...}
}
```

---

### GET /cadena

Obtiene la blockchain completa

**Respuesta:**
```json
{
  "cadena": [
    {
      "indice": 1,
      "timestamp": 1638360000,
      "transacciones": [],
      "prueba": 100,
      "hash_previo": "1"
    }
  ],
  "longitud": 1
}
```

---

### GET /minar

Mina un nuevo bloque (ejecuta Proof of Work)

**Respuesta:**
```json
{
  "mensaje": "Nuevo bloque minado",
  "indice": 2,
  "transacciones": [...],
  "prueba": 35293,
  "hash_previo": "abc123..."
}
```

---

### POST /transacciones/nueva

Crea una nueva transacción

**Body:**
```json
{
  "emisor": "Alice",
  "receptor": "Bob",
  "cantidad": 50
}
```

**Respuesta:**
```json
{
  "mensaje": "Transacción será añadida al bloque 2"
}
```

---

### POST /nodos/registrar

Registra nuevos nodos en la red

**Body:**
```json
{
  "nodos": ["http://localhost:5001", "http://localhost:5002"]
}
```

**Respuesta:**
```json
{
  "mensaje": "Nuevos nodos registrados",
  "nodos_totales": ["localhost:5001", "localhost:5002"]
}
```

---

### GET /nodos/resolver

Ejecuta algoritmo de consenso (regla de cadena más larga)

**Respuesta (si se reemplazó):**
```json
{
  "mensaje": "Cadena reemplazada",
  "nueva_cadena": [...]
}
```

**Respuesta (si no se reemplazó):**
```json
{
  "mensaje": "Cadena autoritativa",
  "cadena": [...]
}
```

---

## Conceptos Técnicos Implementados

### 1. Estructura de Bloques

Cada bloque contiene:

- **Índice**: Posición en la cadena
- **Timestamp**: Momento de creación
- **Transacciones**: Lista de transacciones incluidas
- **Prueba**: Número que satisface el Proof of Work
- **Hash Previo**: Hash SHA-256 del bloque anterior

### 2. Hash SHA-256

Función criptográfica que:
- Genera un hash de 64 caracteres hexadecimales
- Es unidireccional (no se puede revertir)
- Cualquier cambio en los datos produce un hash completamente diferente
- Asegura la integridad de la cadena

### 3. Proof of Work

Algoritmo de consenso que:
- Requiere encontrar un número (prueba) que al combinarse con datos anteriores produzca un hash con N ceros iniciales
- Es difícil de computar (requiere muchos intentos)
- Es fácil de verificar (solo un hash)
- Previene spam y ataques a la red

**Condición de validez:**
```python
SHA256(prueba_anterior + prueba + hash_anterior)[:4] == "0000"
```

### 4. Consenso Distribuido

**Regla de la Cadena Más Larga:**
- Cada nodo mantiene su propia copia de la blockchain
- En caso de conflicto, se adopta la cadena válida más larga
- Esto resuelve automáticamente las bifurcaciones (forks)
- Protege contra ataques del 51%

### 5. Inmutabilidad

La blockchain es inmutable porque:
- Cada bloque contiene el hash del anterior
- Cambiar un bloque antiguo invalida todos los siguientes
- Requeriría recalcular todos los PoW subsiguientes
- En una red grande, es computacionalmente imposible

---

## Configuración Avanzada

### Ajustar Dificultad del Proof of Work

Editar en `blockchain.py`, método `prueba_valida`:

```python
# Fácil (2 ceros): rápido para demostraciones
return hash_intento[:2] == "00"

# Medio (4 ceros): equilibrado [POR DEFECTO]
return hash_intento[:4] == "0000"

# Difícil (6 ceros): muy lento
return hash_intento[:6] == "000000"
```

### Cambiar Puerto del Servidor

```powershell
python blockchain.py -p 8080
```

---

## Solución de Problemas

### Error: "No module named 'flask'"

```powershell
pip install flask requests
```

### Error: "Address already in use"

El puerto está ocupado. Usa otro puerto:
```powershell
python blockchain.py -p 5001
```

### El juego no se conecta

Asegúrate de ejecutar primero `blockchain.py` antes de `juego_educativo.py`

---

## Casos de Uso Educativo

### 1. Demostración en Clase

Usar el **juego educativo** para explicar conceptos paso a paso.

### 2. Laboratorio Práctico

Los estudiantes ejecutan nodos y experimentan con transacciones y minado.

### 3. Proyecto de Investigación

Modificar el código para experimentar con:
- Diferentes algoritmos de consenso
- Variaciones de dificultad
- Tipos de transacciones personalizadas

### 4. Red Distribuida

Simular una red blockchain con múltiples computadoras en la misma red local.

---

## Limitaciones

Este es un proyecto **educativo**. No debe usarse en producción porque:

1. No tiene persistencia (los datos se pierden al cerrar)
2. No implementa criptografía de clave pública/privada
3. No tiene protección contra ataques avanzados
4. La dificultad de PoW es baja (para demostración)
5. No implementa todas las optimizaciones de blockchains reales

---

## Comparación con Bitcoin

| Característica | Este Proyecto | Bitcoin |
|---------------|---------------|---------|
| Lenguaje | Python | C++ |
| Consenso | PoW (4 ceros) | PoW (dificultad variable) |
| Red | HTTP/Flask | P2P sobre TCP |
| Transacciones | Simple | UTXO model |
| Persistencia | No | Sí (LevelDB) |
| Criptografía | SHA-256 | SHA-256 + ECDSA |
| Dificultad | Fija | Ajustable cada 2016 bloques |

---

## Extensiones Posibles

1. **Persistencia**: Guardar blockchain en archivo o base de datos
2. **Firmas Digitales**: Implementar criptografía de clave pública
3. **Merkle Trees**: Optimizar verificación de transacciones
4. **Smart Contracts**: Añadir lógica programable
5. **Wallet**: Crear interfaz de billetera
6. **Explorer**: Crear explorador web de bloques

---

## Referencias

- **Bitcoin Whitepaper**: https://bitcoin.org/bitcoin.pdf
- **Blockchain Demo Visual**: https://andersbrownworth.com/blockchain/
- **Documentación Flask**: https://flask.palletsprojects.com/
- **SHA-256**: https://en.wikipedia.org/wiki/SHA-2

---

## Autor y Licencia

**Proyecto**: Blockchain Educativo con Python  
**Propósito**: Sistemas Operativos - Proyecto Final  
**Licencia**: Código abierto para fines educativos

---

## Conclusión

Este proyecto demuestra de manera práctica y funcional cómo se implementa una blockchain desde cero, cubriendo todos los componentes esenciales:

- Estructura de bloques con hash SHA-256
- Algoritmo Proof of Work
- Consenso por cadena más larga
- Red distribuida con múltiples nodos
- API REST para interacción

Es ideal para aprender los fundamentos de blockchain de manera práctica, con un enfoque educativo mediante el juego interactivo incluido.

---

Última actualización: Noviembre 2025
