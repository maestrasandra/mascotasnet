import os
from pathlib import Path
import MySQLdb

# Load .env file
BASE_DIR = Path(__file__).resolve().parent
env_path = BASE_DIR / '.env'
if env_path.exists():
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, val = line.split('=', 1)
                os.environ[key.strip()] = val.strip().strip('"').strip("'")

# Get connection details
host = os.environ.get('MYSQLHOST', 'localhost')
port = int(os.environ.get('MYSQLPORT', '3306'))
user = os.environ.get('MYSQLUSER', 'root')
password = os.environ.get('MYSQLPASSWORD', 'user')
database = os.environ.get('MYSQLDATABASE', 'mascotasnet')

print(f"Connecting to database '{database}' on {host}:{port} to update images...")

try:
    conn = MySQLdb.connect(
        host=host,
        port=port,
        user=user,
        passwd=password,
        db=database,
        charset='utf8mb4'
    )
    cursor = conn.cursor()
except Exception as e:
    print(f"Failed to connect: {e}")
    exit(1)

# Update products
products_updates = [
    ("img/alimento.png", "Alimento Premium para Perros"),
    ("img/juguete.png", "Juguete Interactivo para Gatos"),
    ("img/shampoo.png", "Shampoo Hipoalergénico")
]

for img, name in products_updates:
    cursor.execute("UPDATE producto SET imagen = %s WHERE nombre = %s", (img, name))
    print(f"Updated product '{name}' with image '{img}'")

# Update pets
pets_updates = [
    ("img/max.png", "Max"),
    ("img/luna.png", "Luna"),
    ("img/bolita.png", "Bolita")
]

for img, name in pets_updates:
    cursor.execute("UPDATE mascota SET imagen = %s WHERE nombre = %s", (img, name))
    print(f"Updated pet '{name}' with image '{img}'")

conn.commit()
print("Images updated successfully in the database!")
conn.close()
