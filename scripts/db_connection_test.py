import psycopg2
import yaml
import logging
import os

# Get absolute path of project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONFIG_PATH = os.path.join(BASE_DIR, "config", "db_config.yaml")
LOG_DIR = os.path.join(BASE_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "automation.log")

# Ensure log directory exists
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def load_config():
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)

def test_db_connection():
    db = load_config()["database"]

    try:
        conn = psycopg2.connect(
            host=db["host"],
            port=db["port"],
            dbname=db["name"],
            user=db["user"],
            password=os.getenv(db["password_env"])
        )
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        cur.fetchone()

        logging.info("PostgreSQL connection test: SUCCESS")

        cur.close()
        conn.close()

    except Exception as e:
        logging.error(f"PostgreSQL connection test: FAILED | {e}")

if __name__ == "__main__":
    test_db_connection()
