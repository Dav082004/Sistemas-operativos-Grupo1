# Guía Técnica Detallada - Blockchain Educativo

Esta guía proporciona un análisis técnico profundo de la implementación, explicando cada componente, decisión arquitectónica y mecanismo interno del sistema blockchain.

---

## Tabla de Contenidos

1. [Arquitectura General](#arquitectura-general)
2. [Componente: Bloque](#componente-bloque)
3. [Componente: Blockchain](#componente-blockchain)
4. [Algoritmo Proof of Work](#algoritmo-proof-of-work)
5. [Sistema de Transacciones](#sistema-de-transacciones)
6. [Red Distribuida](#red-distribuida)
7. [Algoritmo de Consenso](#algoritmo-de-consenso)
8. [API REST](#api-rest)
9. [Flujos de Operación](#flujos-de-operación)
10. [Decisiones de Diseño](#decisiones-de-diseño)

---

## Arquitectura General

### Diagrama de Componentes

```
┌─────────────────────────────────────────────┐
│           API REST (Flask)                  │
│  ┌────────┬────────┬────────┬────────────┐  │
│  │ GET /  │GET/minar│POST/tx│GET/resolver│  │
│  └───┬────┴────┬───┴───┬────┴──────┬─────┘  │
└──────┼─────────┼───────┼───────────┼────────┘
       │         │       │           │
       ▼         ▼       ▼           ▼
┌─────────────────────────────────────────────┐
│         Clase Blockchain                    │
│  ┌──────────────────────────────────────┐   │
│  │ - cadena: List[Bloque]               │   │
│  │ - transacciones_actuales: List[Dict] │   │
│  │ - nodos: Set[str]                    │   │
│  │                                      │   │
│  │ Métodos:                             │   │
│  │ + nuevo_bloque()                     │   │
│  │ + nueva_transaccion()                │   │
│  │ + proof_of_work()                    │   │
│  │ + validar_cadena()                   │   │
│  │ + resolver_conflictos()              │   │
│  └──────────────────────────────────────┘   │
└─────────────────┬───────────────────────────┘
                  │
                  │ contiene
                  ▼
┌─────────────────────────────────────────────┐
│            Clase Bloque                     │
│  ┌──────────────────────────────────────┐   │
│  │ - indice: int                        │   │
│  │ - timestamp: float                   │   │
│  │ - transacciones: List[Dict]          │   │
│  │ - prueba: int                        │   │
│  │ - hash_previo: str                   │   │
│  │                                      │   │
│  │ Métodos:                             │   │
│  │ + calcular_hash()                    │   │
│  │ + to_dict()                          │   │
│  └──────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

### Tecnologías Utilizadas

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| Python | 3.7+ | Lenguaje principal |
| Flask | 3.0.0 | Framework web para API REST |
| hashlib | stdlib | Implementación SHA-256 |
| requests | 2.31.0 | Cliente HTTP para comunicación entre nodos |
| json | stdlib | Serialización de datos |
| uuid | stdlib | Generación de identificadores únicos |
| urllib.parse | stdlib | Parseo de URLs |

---

## Componente: Bloque

### Estructura de Datos

```python
class Bloque:
    def __init__(self, indice, transacciones, prueba, hash_previo):
        self.indice = indice                      # Posición en la cadena
        self.timestamp = time()                   # Momento de creación
        self.transacciones = transacciones        # Lista de transacciones
        self.prueba = prueba                      # Nonce del PoW
        self.hash_previo = hash_previo           # Hash del bloque anterior
```

### Análisis Detallado de Propiedades

#### 1. Índice (indice)

- **Tipo**: `int`
- **Propósito**: Identificador secuencial del bloque en la cadena
- **Rango**: Comienza en 1 (bloque génesis)
- **Inmutabilidad**: No cambia una vez asignado

#### 2. Timestamp

- **Tipo**: `float`
- **Formato**: Unix timestamp (segundos desde 1970-01-01 00:00:00 UTC)
- **Propósito**: Marca temporal precisa del momento de creación
- **Uso**: 
  - Ordenamiento temporal
  - Auditoría
  - Detección de manipulación temporal

**Ejemplo:**
```python
>>> import time
>>> time.time()
1638360123.456789
```

#### 3. Transacciones

- **Tipo**: `List[Dict[str, Any]]`
- **Estructura de cada transacción**:
```python
{
    "emisor": str,      # Dirección del remitente
    "receptor": str,    # Dirección del destinatario
    "cantidad": float   # Monto transferido
}
```

- **Límite**: Sin límite técnico (en producción se limitaría por tamaño de bloque)
- **Estado**: Confirmadas cuando el bloque es minado

#### 4. Prueba (Nonce)

- **Tipo**: `int`
- **Propósito**: Número que satisface la condición del Proof of Work
- **Rango**: 0 a infinito (prácticamente hasta encontrar solución)
- **Complejidad**: Depende de la dificultad configurada

**Proceso de búsqueda:**
```python
prueba = 0
while not prueba_valida(hash_anterior, prueba):
    prueba += 1
# Al salir, prueba contiene el nonce válido
```

#### 5. Hash Previo

- **Tipo**: `str`
- **Formato**: 64 caracteres hexadecimales (SHA-256)
- **Propósito**: Enlazar criptográficamente con el bloque anterior
- **Especial**: El bloque génesis usa "1" como valor arbitrario

### Método: calcular_hash()

```python
def calcular_hash(self):
    bloque_string = json.dumps(self.to_dict(), sort_keys=True)
    return hashlib.sha256(bloque_string.encode()).hexdigest()
```

**Análisis paso a paso:**

1. **Serialización a JSON**:
   - `self.to_dict()` convierte el bloque a diccionario
   - `json.dumps()` serializa a string JSON
   - `sort_keys=True` asegura orden determinista

2. **Encoding**:
   - `.encode()` convierte string a bytes (UTF-8)
   - SHA-256 requiere entrada en bytes

3. **Hashing**:
   - `hashlib.sha256()` aplica función hash
   - `.hexdigest()` convierte resultado a hexadecimal

**Ejemplo de ejecución:**

```python
# Input
bloque = {
    "indice": 1,
    "timestamp": 1638360000,
    "transacciones": [],
    "prueba": 100,
    "hash_previo": "1"
}

# Serialización
json_string = '{"hash_previo":"1","indice":1,"prueba":100,"timestamp":1638360000,"transacciones":[]}'

# Encoding
bytes_data = b'{"hash_previo":"1","indice":1,"prueba":100,"timestamp":1638360000,"transacciones":[]}'

# Hash
hash_result = "abc123...def" # 64 caracteres hex
```

### Propiedades del Hash

- **Determinista**: Misma entrada → mismo hash
- **Avalanche Effect**: Cambio de 1 bit → ~50% del hash cambia
- **Unidireccional**: Hash → datos es imposible
- **Colisión resistente**: Prácticamente imposible encontrar dos entradas con mismo hash

---

## Componente: Blockchain

### Estructura de Datos

```python
class Blockchain:
    def __init__(self):
        self.transacciones_actuales = []  # Pool de transacciones pendientes
        self.cadena = []                  # Lista de bloques confirmados
        self.nodos = set()                # Red de nodos conectados
        
        # Crear bloque génesis
        self.nuevo_bloque(prueba_anterior=100, hash_previo='1')
```

### Bloque Génesis

**Definición**: Primer bloque de la cadena, creado manualmente sin referencia a bloque anterior.

**Propiedades especiales:**
- Índice: 1
- Hash previo: "1" (valor arbitrario)
- Prueba: 100 (valor arbitrario, no requiere PoW)
- Transacciones: Lista vacía
- No tiene bloque padre

**Importancia:**
- Punto de inicio común para todos los nodos
- Referencia inmutable para verificación
- En blockchains reales, contiene parámetros de configuración

### Método: nuevo_bloque()

```python
def nuevo_bloque(self, prueba, hash_previo=None):
    bloque = Bloque(
        indice=len(self.cadena) + 1,
        transacciones=self.transacciones_actuales,
        prueba=prueba,
        hash_previo=hash_previo or self.cadena[-1].calcular_hash()
    )
    
    # Reiniciar pool de transacciones
    self.transacciones_actuales = []
    
    # Agregar a la cadena
    self.cadena.append(bloque)
    
    return bloque
```

**Análisis del flujo:**

1. **Creación del bloque**:
   - Índice auto-incrementado
   - Transacciones actuales se incluyen (confirmación)
   - Prueba proviene del PoW
   - Hash previo se calcula del último bloque

2. **Limpieza del pool**:
   - `self.transacciones_actuales = []`
   - Las transacciones ya están confirmadas en el bloque
   - Pool queda listo para nuevas transacciones

3. **Adición a la cadena**:
   - `self.cadena.append(bloque)`
   - El bloque es ahora parte permanente

4. **Retorno**:
   - Devuelve el bloque creado para referencia

### Método: nueva_transaccion()

```python
def nueva_transaccion(self, emisor, receptor, cantidad):
    self.transacciones_actuales.append({
        'emisor': emisor,
        'receptor': receptor,
        'cantidad': cantidad,
    })
    
    return self.ultimo_bloque.indice + 1
```

**Estados de una transacción:**

1. **Pendiente**: En `transacciones_actuales`
   - No confirmada
   - Puede ser reordenada
   - No forma parte de la blockchain

2. **Confirmada**: En un bloque de `cadena`
   - Inmutable
   - Parte del consenso
   - Ordenada secuencialmente

**Valor de retorno:**

```python
return self.ultimo_bloque.indice + 1
```

- Indica el índice del próximo bloque que contendrá la transacción
- Útil para tracking y confirmación

---

## Algoritmo Proof of Work

### Concepto Teórico

**Proof of Work (PoW)** es un algoritmo de consenso que requiere trabajo computacional para crear un bloque válido.

### Propósito

1. **Prevenir spam**: Crear bloques tiene costo computacional
2. **Seguridad**: Atacar la red requiere >50% del poder computacional
3. **Consenso**: Regla objetiva para determinar cadena válida
4. **Incentivo**: Los mineros reciben recompensas

### Implementación

```python
def proof_of_work(self, ultimo_bloque):
    """
    Encuentra un número p' tal que hash(pp'h) contenga 4 ceros iniciales
    p = prueba anterior
    p' = nueva prueba
    h = hash del bloque anterior
    """
    ultima_prueba = ultimo_bloque.prueba
    ultimo_hash = ultimo_bloque.calcular_hash()
    
    prueba = 0
    while not self.prueba_valida(ultima_prueba, prueba, ultimo_hash):
        prueba += 1
    
    return prueba
```

### Análisis Matemático

**Función hash:**
```
H(prueba_anterior || prueba_actual || hash_previo)
```

**Condición de validez:**
```
H[:4] == "0000"
```

**Probabilidad de éxito en cada intento:**
```
P = 16^-4 = 1/65536 ≈ 0.00152%
```

**Intentos esperados:**
```
E = 1/P = 65536 intentos
```

**Tiempo estimado (Python):**
- Hashes por segundo: ~100,000
- Tiempo esperado: 65536/100000 ≈ 0.66 segundos

### Verificación

```python
def prueba_valida(self, ultima_prueba, prueba, ultimo_hash):
    intento = f'{ultima_prueba}{prueba}{ultimo_hash}'.encode()
    hash_intento = hashlib.sha256(intento).hexdigest()
    return hash_intento[:4] == "0000"
```

**Propiedades:**

1. **Difícil de encontrar**:
   - Requiere ~65,000 intentos
   - No hay atajo conocido

2. **Fácil de verificar**:
   - Una sola operación hash
   - O(1) complejidad

3. **Determinista**:
   - Mismos inputs → mismo resultado
   - Reproducible por cualquier nodo

### Ajuste de Dificultad

**Dificultad actual: 4 ceros (2^16)**

Modificar condición para ajustar:

```python
# Más fácil (2 ceros): 2^8 = 256 intentos
return hash_intento[:2] == "00"

# Más difícil (6 ceros): 2^24 = 16,777,216 intentos
return hash_intento[:6] == "000000"
```

**En Bitcoin:**
- Dificultad se ajusta cada 2016 bloques
- Objetivo: 1 bloque cada 10 minutos
- Fórmula: `nueva_dificultad = dificultad_actual * (20160 / tiempo_real)`

---

## Sistema de Transacciones

### Ciclo de Vida de una Transacción

```
┌─────────────┐
│   Creada    │ ← POST /transacciones/nueva
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Pendiente  │ ← En transacciones_actuales
└──────┬──────┘
       │
       ▼ Minado
┌─────────────┐
│ Confirmada  │ ← En bloque de la cadena
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Inmutable  │ ← Protegida por PoW subsiguientes
└─────────────┘
```

### Estructura de Transacción

```python
transaccion = {
    'emisor': str,         # Identificador del remitente
    'receptor': str,       # Identificador del destinatario
    'cantidad': float      # Monto a transferir
}
```

**Limitaciones actuales (simplificación educativa):**
- No hay verificación de balance
- No hay firmas digitales
- No hay verificación de autenticidad

**En blockchain real (ej. Bitcoin):**

```python
transaccion_bitcoin = {
    'inputs': [
        {
            'txid': str,          # ID transacción origen
            'vout': int,          # Índice salida
            'scriptSig': str      # Firma digital
        }
    ],
    'outputs': [
        {
            'value': int,         # Satoshis
            'scriptPubKey': str   # Script de bloqueo
        }
    ],
    'locktime': int,          # Tiempo de bloqueo
    'version': int            # Versión del protocolo
}
```

### Pool de Transacciones (Mempool)

```python
self.transacciones_actuales = []
```

**Propiedades:**
- Lista temporal en memoria
- Se vacía al minar un bloque
- No persiste entre reinicios
- No tiene límite de tamaño (en producción sí)

**Mejoras posibles:**
1. Ordenamiento por fee (tarifa)
2. Límite de tamaño
3. Expiración temporal
4. Priorización

---

## Red Distribuida

### Registro de Nodos

```python
def registrar_nodo(self, direccion):
    """
    Añadir un nuevo nodo a la red
    :param direccion: Dirección del nodo ej. 'http://192.168.0.5:5000'
    """
    parsed_url = urlparse(direccion)
    self.nodos.add(parsed_url.netloc)
```

**Análisis:**

1. **Parsing de URL**:
```python
urlparse('http://192.168.0.5:5000/path')
# Resultado:
# ParseResult(
#     scheme='http',
#     netloc='192.168.0.5:5000',  ← Esto se guarda
#     path='/path',
#     params='',
#     query='',
#     fragment=''
# )
```

2. **Almacenamiento en Set**:
   - `set()` evita duplicados automáticamente
   - No importa registrar el mismo nodo múltiples veces

3. **Formato netloc**:
   - Incluye host y puerto
   - Sin protocolo, sin path
   - Ejemplo: `"localhost:5001"`

### Comunicación Entre Nodos

```python
# Obtener cadena de otro nodo
response = requests.get(f'http://{nodo}/cadena')
```

**Protocolo HTTP simple:**
- GET para consultar
- POST para enviar datos
- JSON como formato de intercambio

**En producción:**
- P2P puro (sin servidor central)
- Protocolo binario (más eficiente)
- Encryption (TLS)
- Discovery automático de nodos

---

## Algoritmo de Consenso

### Regla de la Cadena Más Larga

**Principio fundamental**: En caso de conflicto, la cadena válida más larga es la autoritativa.

### Implementación

```python
def resolver_conflictos(self):
    """
    Algoritmo de consenso: reemplaza la cadena con la más larga de la red
    :return: True si la cadena fue reemplazada, False si no
    """
    vecinos = self.nodos
    nueva_cadena = None
    
    # Buscar cadenas más largas que la nuestra
    longitud_maxima = len(self.cadena)
    
    # Consultar todos los nodos de la red
    for nodo in vecinos:
        response = requests.get(f'http://{nodo}/cadena')
        
        if response.status_code == 200:
            longitud = response.json()['longitud']
            cadena = response.json()['cadena']
            
            # Verificar si es más larga y válida
            if longitud > longitud_maxima and self.validar_cadena(cadena):
                longitud_maxima = longitud
                nueva_cadena = cadena
    
    # Reemplazar si encontramos una mejor
    if nueva_cadena:
        self.cadena = [Bloque(**bloque) for bloque in nueva_cadena]
        return True
    
    return False
```

### Análisis del Flujo

**Paso 1: Inicialización**
```python
vecinos = self.nodos
nueva_cadena = None
longitud_maxima = len(self.cadena)
```

**Paso 2: Consulta a vecinos**
```python
for nodo in vecinos:
    response = requests.get(f'http://{nodo}/cadena')
```

**Paso 3: Comparación**
```python
if longitud > longitud_maxima and self.validar_cadena(cadena):
    longitud_maxima = longitud
    nueva_cadena = cadena
```

**Criterios de selección:**
1. Más larga que la actual
2. Pasa validación completa
3. Si hay empate, se queda con la primera encontrada

**Paso 4: Reemplazo**
```python
if nueva_cadena:
    self.cadena = [Bloque(**bloque) for bloque in nueva_cadena]
    return True
```

### Validación de Cadena

```python
def validar_cadena(self, cadena):
    """
    Determina si una blockchain es válida
    """
    bloque_previo = cadena[0]
    indice_actual = 1
    
    while indice_actual < len(cadena):
        bloque = cadena[indice_actual]
        
        # Verificar hash del bloque previo
        if bloque['hash_previo'] != self.hash(bloque_previo):
            return False
        
        # Verificar Proof of Work
        if not self.prueba_valida(
            bloque_previo['prueba'],
            bloque['prueba'],
            bloque['hash_previo']
        ):
            return False
        
        bloque_previo = bloque
        indice_actual += 1
    
    return True
```

**Verificaciones realizadas:**

1. **Integridad de enlaces**:
   - Cada bloque referencia correctamente al anterior
   - Hash previo coincide con hash calculado

2. **Proof of Work válido**:
   - Cada bloque tiene prueba válida
   - Satisface condición de dificultad

3. **Secuencia ordenada**:
   - Bloques en orden correcto
   - No hay saltos ni duplicados

### Casos de Conflicto

#### Caso 1: Fork Simple

```
Nodo A: [G] → [1] → [2] → [3]
Nodo B: [G] → [1] → [2'] → [3']

Resolución: Ambas tienen longitud 4, no hay reemplazo automático
```

#### Caso 2: Fork con Resolución

```
Nodo A: [G] → [1] → [2] → [3]
Nodo B: [G] → [1] → [2'] → [3'] → [4']

Resolución: B tiene longitud 5 > A, todos adoptan cadena de B
```

#### Caso 3: Cadena Inválida

```
Nodo A: [G] → [1] → [2] → [3]
Nodo B: [G] → [1] → [2x] → [3'] → [4'] (2x tiene PoW inválido)

Resolución: B rechazada por validación, A permanece autoritativa
```

### Ataque del 51%

**Escenario**: Un atacante controla >50% del poder computacional.

**Consecuencias:**
- Puede crear cadena alternativa más rápido
- Puede revertir transacciones (double-spend)
- No puede modificar bloques antiguos (requiere recalcular todos)

**Protección:**
- Esperar múltiples confirmaciones
- Red distribuida con muchos nodos honestos
- Alto costo de obtener >50% poder

---

## API REST

### Endpoint: GET /

```python
@app.route('/', methods=['GET'])
def informacion():
    response = {
        'mensaje': 'Blockchain Educativo - Nodo Activo',
        'nodo_id': identificador_nodo,
        'bloques': len(blockchain.cadena),
        'endpoints': {
            'cadena': '/cadena',
            'minar': '/minar',
            'transacciones': '/transacciones/nueva',
            'nodos': '/nodos/registrar',
            'resolver': '/nodos/resolver'
        }
    }
    return jsonify(response), 200
```

**Uso**: Verificar estado del nodo, descubrir endpoints disponibles.

### Endpoint: GET /cadena

```python
@app.route('/cadena', methods=['GET'])
def cadena_completa():
    response = {
        'cadena': [bloque.to_dict() for bloque in blockchain.cadena],
        'longitud': len(blockchain.cadena),
    }
    return jsonify(response), 200
```

**Análisis:**
- Serialización de objetos Bloque a diccionarios
- Uso de list comprehension para eficiencia
- Retorna cadena completa (en producción se paginaría)

### Endpoint: GET /minar

```python
@app.route('/minar', methods=['GET'])
def minar():
    # 1. Ejecutar PoW
    ultimo_bloque = blockchain.ultimo_bloque
    prueba = blockchain.proof_of_work(ultimo_bloque)
    
    # 2. Recompensar al minero
    blockchain.nueva_transaccion(
        emisor="0",
        receptor=identificador_nodo,
        cantidad=1,
    )
    
    # 3. Crear nuevo bloque
    hash_previo = ultimo_bloque.calcular_hash()
    bloque = blockchain.nuevo_bloque(prueba, hash_previo)
    
    # 4. Respuesta
    response = {
        'mensaje': "Nuevo bloque minado",
        'indice': bloque.indice,
        'transacciones': bloque.transacciones,
        'prueba': bloque.prueba,
        'hash_previo': bloque.hash_previo,
    }
    return jsonify(response), 200
```

**Flujo de minado:**

1. **Cálculo de PoW**: ~0.5-1 segundos
2. **Recompensa de minado**: 1 unidad al nodo minero
3. **Creación de bloque**: Confirma todas las transacciones pendientes
4. **Respuesta**: Devuelve información del bloque minado

### Endpoint: POST /transacciones/nueva

```python
@app.route('/transacciones/nueva', methods=['POST'])
def nueva_transaccion():
    valores = request.get_json()
    
    # Verificar campos requeridos
    requeridos = ['emisor', 'receptor', 'cantidad']
    if not all(k in valores for k in requeridos):
        return 'Faltan valores', 400
    
    # Crear transacción
    indice = blockchain.nueva_transaccion(
        valores['emisor'],
        valores['receptor'],
        valores['cantidad']
    )
    
    response = {'mensaje': f'Transacción será añadida al bloque {indice}'}
    return jsonify(response), 201
```

**Validaciones realizadas:**
- Verificación de campos requeridos
- Estructura JSON correcta
- Retorna código 201 (Created)

### Endpoint: POST /nodos/registrar

```python
@app.route('/nodos/registrar', methods=['POST'])
def registrar_nodos():
    valores = request.get_json()
    
    nodos = valores.get('nodos')
    if nodos is None:
        return "Error: Lista de nodos no válida", 400
    
    for nodo in nodos:
        blockchain.registrar_nodo(nodo)
    
    response = {
        'mensaje': 'Nuevos nodos registrados',
        'nodos_totales': list(blockchain.nodos),
    }
    return jsonify(response), 201
```

**Registro bilateral:**

Para red completa, cada nodo debe registrar a los demás:

```
Nodo A registra a B y C
Nodo B registra a A y C
Nodo C registra a A y B
```

### Endpoint: GET /nodos/resolver

```python
@app.route('/nodos/resolver', methods=['GET'])
def consenso():
    reemplazada = blockchain.resolver_conflictos()
    
    if reemplazada:
        response = {
            'mensaje': 'Cadena reemplazada',
            'nueva_cadena': [bloque.to_dict() for bloque in blockchain.cadena]
        }
    else:
        response = {
            'mensaje': 'Cadena autoritativa',
            'cadena': [bloque.to_dict() for bloque in blockchain.cadena]
        }
    
    return jsonify(response), 200
```

**Cuándo ejecutar:**
- Después de desconexión temporal
- Periódicamente (en producción)
- Al detectar discrepancia
- Al unirse a la red

---

## Flujos de Operación

### Flujo 1: Crear y Minar Transacción

```
┌──────┐          ┌────────────┐          ┌────────────┐
│Client│          │   Flask    │          │ Blockchain │
└──┬───┘          └─────┬──────┘          └─────┬──────┘
   │                    │                       │
   │  POST /transacciones/nueva                 │
   │───────────────────>│                       │
   │                    │  nueva_transaccion()  │
   │                    │──────────────────────>│
   │                    │                       │
   │                    │  [Añade a pool]       │
   │                    │<──────────────────────│
   │  201 Created       │                       │
   │<───────────────────│                       │
   │                    │                       │
   │  GET /minar        │                       │
   │───────────────────>│                       │
   │                    │  proof_of_work()      │
   │                    │──────────────────────>│
   │                    │  [Calcula PoW]        │
   │                    │  (0.5-1 seg)          │
   │                    │<──────────────────────│
   │                    │                       │
   │                    │  nuevo_bloque()       │
   │                    │──────────────────────>│
   │                    │  [Crea bloque]        │
   │                    │<──────────────────────│
   │  200 OK            │                       │
   │<───────────────────│                       │
   │  {bloque minado}   │                       │
```

### Flujo 2: Consenso Distribuido

```
┌──────┐     ┌──────┐    ┌──────┐    ┌──────┐
│Nodo A│     │Nodo B│    │Nodo C│    │Nodo D│
└──┬───┘     └──┬───┘    └──┬───┘    └──┬───┘
   │            │           │           │
   │  [Mina bloque 4]       │           │
   │<─          │           │           │
   │            │           │           │
   │            │  [Mina bloque 4']     │
   │            │           │<─         │
   │            │           │           │
   │  GET /nodos/resolver   │           │
   │───────────────────────>│           │
   │            │           │           │
   │            │  GET /cadena          │
   │            │<──────────────────────│
   │            │  [longitud: 4]        │
   │            │           │           │
   │  GET /cadena           │           │
   │<───────────────────────│           │
   │  [longitud: 5]         │           │
   │            │           │           │
   │  [Adopta cadena de C]  │           │
   │────────────────────────>           │
   │  200 OK {reemplazada}  │           │
```

### Flujo 3: Validación de Cadena

```
validar_cadena(cadena)
│
├─> Para cada bloque en cadena:
│   │
│   ├─> Verificar hash_previo
│   │   ├─> Calcular hash de bloque anterior
│   │   ├─> Comparar con hash_previo del bloque actual
│   │   └─> Si no coincide → return False
│   │
│   ├─> Verificar Proof of Work
│   │   ├─> Calcular hash(prueba_anterior + prueba_actual + hash_previo)
│   │   ├─> Verificar que comience con "0000"
│   │   └─> Si no válido → return False
│   │
│   └─> Avanzar al siguiente bloque
│
└─> Si todos los bloques son válidos → return True
```

---

## Decisiones de Diseño

### 1. ¿Por qué Flask en lugar de FastAPI?

**Decisión**: Flask 3.0.0

**Razones:**
- Simplicidad para proyecto educativo
- Documentación extensa y madura
- Sintaxis directa y comprensible
- Menor curva de aprendizaje

**Alternativa considerada**: FastAPI
- Ventajas: Async, tipo checking, documentación automática
- Desventajas: Más complejo, overkill para este caso

### 2. ¿Por qué PoW y no PoS?

**Decisión**: Proof of Work

**Razones:**
- Más fácil de entender conceptualmente
- No requiere gestión de stakes
- Demostración directa de trabajo computacional
- Históricamente el primer algoritmo (Bitcoin)

**Alternativa considerada**: Proof of Stake
- Ventajas: Más eficiente energéticamente
- Desventajas: Más complejo, requiere sistema de staking

### 3. ¿Por qué dificultad fija (4 ceros)?

**Decisión**: Dificultad estática de 4 ceros

**Razones:**
- Tiempo de minado predecible (~0.5-1 segundo)
- Facilita demostraciones y pruebas
- Suficiente para mostrar concepto de PoW
- No requiere ajuste dinámico

**En producción**: Dificultad ajustable cada N bloques

### 4. ¿Por qué no hay persistencia?

**Decisión**: Todo en memoria RAM

**Razones:**
- Simplifica código educativo
- Reinicio rápido para experimentos
- No requiere gestión de archivos o DB
- Enfoque en lógica blockchain, no en I/O

**Para producción**: LevelDB, RocksDB, o PostgreSQL

### 5. ¿Por qué transacciones sin firma digital?

**Decisión**: Transacciones simples sin criptografía de clave pública

**Razones:**
- Simplifica demostración del mecanismo
- Evita complejidad de gestión de claves
- Enfoque en estructura blockchain, no en seguridad completa

**Para producción**: ECDSA (Bitcoin), EdDSA (Ethereum)

### 6. ¿Por qué HTTP en lugar de P2P puro?

**Decisión**: API REST sobre HTTP

**Razones:**
- Fácil de probar con herramientas estándar (Postman, curl)
- No requiere protocolo P2P personalizado
- Infraestructura conocida (HTTP)
- Suficiente para demostrar red distribuida

**Para producción**: Protocolo P2P (libp2p, devp2p)

### 7. ¿Por qué Set para nodos?

**Decisión**: `self.nodos = set()`

**Razones:**
- Evita duplicados automáticamente
- Operaciones O(1) para agregar/verificar
- No importa orden de nodos

**Alternativa considerada**: Lista
- Desventaja: Permite duplicados, requiere verificación manual

---

## Comparación con Blockchains Reales

### Bitcoin vs Este Proyecto

| Aspecto | Este Proyecto | Bitcoin |
|---------|--------------|---------|
| **Lenguaje** | Python | C++ |
| **Consenso** | PoW (4 ceros fijos) | PoW (dificultad ajustable) |
| **Transacciones** | Cuenta simple | UTXO model |
| **Red** | HTTP REST | P2P sobre TCP |
| **Persistencia** | Memoria | LevelDB |
| **Criptografía** | SHA-256 | SHA-256 + RIPEMD-160 + ECDSA |
| **Scripting** | No | Bitcoin Script |
| **Tamaño bloque** | Sin límite | 1 MB (4 MB con SegWit) |
| **Tiempo bloque** | ~1 segundo | ~10 minutos |
| **Ajuste dificultad** | No | Cada 2016 bloques |

### Ethereum vs Este Proyecto

| Aspecto | Este Proyecto | Ethereum |
|---------|--------------|---------|
| **Smart Contracts** | No | Sí (Solidity) |
| **Máquina virtual** | No | EVM |
| **Consenso** | PoW | PoS (post-Merge) |
| **Estado** | Solo transacciones | Estado global |
| **Gas** | No | Sí |
| **Cuentas** | Simple | EOA + Contract |

---

## Ejercicios Prácticos

### Ejercicio 1: Modificar Dificultad

**Objetivo**: Experimentar con diferentes niveles de dificultad.

**Tarea**:
1. Modificar `prueba_valida()` para requerir 6 ceros
2. Medir tiempo de minado
3. Comparar con 2 ceros

**Código:**
```python
# En blockchain.py, línea ~150
def prueba_valida(self, ultima_prueba, prueba, ultimo_hash):
    intento = f'{ultima_prueba}{prueba}{ultimo_hash}'.encode()
    hash_intento = hashlib.sha256(intento).hexdigest()
    return hash_intento[:6] == "000000"  # Cambiar aquí
```

### Ejercicio 2: Implementar Recompensa Variable

**Objetivo**: Reducir recompensa cada N bloques (halving).

**Tarea**:
1. Calcular recompensa basada en altura del bloque
2. Implementar halving cada 10 bloques

**Código sugerido:**
```python
def calcular_recompensa(self):
    altura = len(self.cadena)
    halvings = altura // 10
    recompensa = 50 / (2 ** halvings)
    return max(recompensa, 1)  # Mínimo 1
```

### Ejercicio 3: Persistencia en JSON

**Objetivo**: Guardar blockchain en archivo.

**Tarea**:
1. Serializar cadena a JSON al cerrar
2. Cargar cadena al iniciar

**Código sugerido:**
```python
def guardar(self, archivo='blockchain.json'):
    with open(archivo, 'w') as f:
        json.dump([b.to_dict() for b in self.cadena], f)

def cargar(self, archivo='blockchain.json'):
    try:
        with open(archivo, 'r') as f:
            datos = json.load(f)
            self.cadena = [Bloque(**b) for b in datos]
    except FileNotFoundError:
        pass  # Crear bloque génesis
```

### Ejercicio 4: Transacciones con Balance

**Objetivo**: Implementar verificación de saldo.

**Tarea**:
1. Calcular balance de cada dirección
2. Rechazar transacciones sin fondos

**Código sugerido:**
```python
def calcular_balance(self, direccion):
    balance = 0
    for bloque in self.cadena:
        for tx in bloque.transacciones:
            if tx['receptor'] == direccion:
                balance += tx['cantidad']
            if tx['emisor'] == direccion:
                balance -= tx['cantidad']
    return balance

def nueva_transaccion(self, emisor, receptor, cantidad):
    if emisor != "0":  # No validar recompensas de minado
        if self.calcular_balance(emisor) < cantidad:
            raise ValueError("Saldo insuficiente")
    # ... resto del código
```

---

## Glosario Técnico

**- Blockchain**: Estructura de datos encadenada criptográficamente donde cada bloque contiene el hash del anterior.

**- Hash**: Función criptográfica unidireccional que convierte datos de cualquier tamaño en una cadena de longitud fija.

**- once**: Number used once. En PoW, el número que se busca para satisfacer la condición de dificultad.

**- Proof of Work**: Algoritmo de consenso que requiere trabajo computacional demostrable para crear bloques válidos.

**- Consenso**: Mecanismo por el cual los nodos de una red distribuida acuerdan el estado del sistema.

**- Fork**: Bifurcación en la blockchain cuando dos bloques diferentes se minan simultáneamente.

**- Mempool**: Pool de transacciones pendientes que esperan ser confirmadas en un bloque.

**- Bloque Génesis**: Primer bloque de una blockchain, creado manualmente.

**- Inmutabilidad**: Propiedad por la cual los datos en la blockchain no pueden ser modificados sin recalcular todos los bloques subsiguientes.

**- Distributed Ledger**: Libro contable distribuido entre múltiples nodos sin autoridad central.

**- Double Spend**: Intento de gastar los mismos fondos dos veces. Prevenido por la blockchain.

**- 51% Attack**: Ataque donde una entidad controla más del 50% del poder computacional de la red.

---

## Referencias Técnicas

1. **Bitcoin Whitepaper** - Satoshi Nakamoto (2008)
   - https://bitcoin.org/bitcoin.pdf

2. **Mastering Bitcoin** - Andreas Antonopoulos
   - https://github.com/bitcoinbook/bitcoinbook

3. **Blockchain Demo Interactivo**
   - https://andersbrownworth.com/blockchain/

4. **SHA-256 Standard**
   - FIPS PUB 180-4

5. **Flask Documentation**
   - https://flask.palletsprojects.com/

6. **Python hashlib**
   - https://docs.python.org/3/library/hashlib.html

---

**Fin de la Guía Técnica**

Esta guía proporciona una comprensión profunda de cada componente del sistema blockchain educativo. Para más información o dudas específicas, consulta el código fuente comentado en `blockchain.py`.
