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

# Get connection details from environment (from .env)
host = os.environ.get('MYSQLHOST', 'localhost')
port = int(os.environ.get('MYSQLPORT', '3306'))
user = os.environ.get('MYSQLUSER', 'root')
password = os.environ.get('MYSQLPASSWORD', 'user')
database = os.environ.get('MYSQLDATABASE', 'mascotasnet')

print(f"Connecting to database '{database}' on {host}:{port}...")

try:
    # Connect to database
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
    print(f"Failed to connect to database: {e}")
    exit(1)

# Read SQL file
sql_file_path = BASE_DIR / 'templates' / 'MASCOTAS_NET_CORREGIDO.sql'
with open(sql_file_path, 'r', encoding='utf-8') as f:
    sql_content = f.read()

# Parse and execute statements
statements = []
current_statement = []

for line in sql_content.split('\n'):
    stripped_line = line.strip()
    if not stripped_line or stripped_line.startswith('--'):
        continue
    # Skip creating new schema and USE statements so it imports into the existing Railway DB
    if (stripped_line.upper().startswith('CREATE SCHEMA') or 
        stripped_line.upper().startswith('USE ') or
        stripped_line.upper().startswith('DROP SCHEMA')):
        print(f"Skipping statement: {stripped_line}")
        continue
    current_statement.append(line)
    if stripped_line.endswith(';'):
        statements.append('\n'.join(current_statement))
        current_statement = []

print(f"Found {len(statements)} SQL statements to execute.")

for i, stmt in enumerate(statements):
    try:
        cursor.execute(stmt)
    except Exception as e:
        print(f"Error executing statement {i+1}: {e}")
        print("Statement was:")
        print(stmt)
        conn.rollback()
        conn.close()
        exit(1)

conn.commit()
print("Database tables and test data imported successfully!")
conn.close()
