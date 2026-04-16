import csv
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker('es_MX')

NUM_REGISTROS = 100000
OUTPUT_FILE = "datos_delictivos_no_normalizados.csv"

# ==================== CATÁLOGOS ====================
tipos_delito = [
    ("Robo", "Media"), ("Asalto", "Alta"), ("Homicidio", "Muy Alta"),
    ("Fraude", "Media"), ("Secuestro", "Muy Alta"), ("Extorsión", "Alta"),
    ("Violencia familiar", "Media"), ("Tráfico de drogas", "Muy Alta")
]

delitos = {
    "Robo": ["Robo de vehículo", "Robo a casa habitación", "Robo a negocio", "Robo a transeúnte"],
    "Asalto": ["Asalto a mano armada", "Asalto en transporte público", "Asalto en vía pública"],
    "Homicidio": ["Homicidio doloso", "Homicidio culposo"],
    "Fraude": ["Fraude bancario", "Fraude cibernético", "Fraude inmobiliario"],
    "Secuestro": ["Secuestro exprés", "Secuestro virtual"],
    "Extorsión": ["Extorsión telefónica", "Extorsión por cobro de piso"],
    "Violencia familiar": ["Violencia intrafamiliar", "Violencia de género"],
    "Tráfico de drogas": ["Narcomenudeo", "Tráfico de estupefacientes"]
}

estatuses = ["Detenido", "En proceso", "Liberado", "Investigación"]

def generar_curp():
    """Genera CURP de 18 caracteres más realista"""
    return (''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=4)) +
            ''.join(random.choices("0123456789", k=6)) +
            random.choice("HM") +
            ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=2)) +
            ''.join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=5)))

def random_fecha():
    start = datetime(2020, 1, 1)
    end = datetime(2025, 12, 31)
    return (start + timedelta(days=random.randint(0, (end - start).days))).date()

def random_hora():
    return f"{random.randint(0,23):02d}:{random.randint(0,59):02d}:{random.randint(0,59):02d}"

# ==================== GENERACIÓN DEL CSV ====================
with open(OUTPUT_FILE, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow([
        "nombre","apellido","curp","edad","genero","domicilio",
        "delito","tipo_delito","gravedad",
        "fecha","hora","estado","ciudad","colonia","zona_postal",
        "estatus","reincidente","numero_delitos","peso_delito","indice_delictivo",
        "fuero","arma_fuego","recuperado","tiempo_respuesta_minutos"
    ])

    for _ in range(NUM_REGISTROS):
        nombre = fake.first_name()
        apellido = fake.last_name()
        curp = generar_curp()
        edad = random.randint(18, 75)
        genero = random.choice(['M', 'F'])
        domicilio = fake.street_address()

        tipo, gravedad = random.choice(tipos_delito)
        delito = random.choice(delitos[tipo])          # ← Aquí estaba el error

        estado = fake.state()
        ciudad = fake.city()
        colonia = fake.neighborhood() if hasattr(fake, 'neighborhood') else fake.street_name()
        zona_postal = fake.postcode()

        fecha = random_fecha()
        hora = random_hora()

        estatus = random.choice(estatuses)
        reincidente = random.choice([0, 1])
        numero_delitos = random.randint(1, 12)
        peso_delito = round(random.uniform(0.5, 10.0), 2)
        indice_delictivo = round(numero_delitos * peso_delito, 2)

        fuero = random.choice(['Común', 'Federal'])
        arma_fuego = random.choice([True, False]) if tipo in ["Asalto", "Robo"] else False
        recuperado = random.choice([True, False]) if "vehículo" in delito.lower() else False
        tiempo_respuesta_minutos = random.randint(5, 180)

        writer.writerow([
            nombre, apellido, curp, edad, genero, domicilio,
            delito, tipo, gravedad,
            fecha, hora, estado, ciudad, colonia, zona_postal,
            estatus, reincidente, numero_delitos, peso_delito, indice_delictivo,
            fuero, arma_fuego, recuperado, tiempo_respuesta_minutos
        ])

print(f"CSV generado correctamente: {OUTPUT_FILE} con {NUM_REGISTROS:,} registros")