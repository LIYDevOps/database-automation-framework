import psycopg2
import yaml
import logging
import os

# Base paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, "config", "db_config.yaml")
LOG_DIR = os.path.join(BASE_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "automation.log")

os.makedirs(LOG_DIR, exist_ok=True)

# ✅ Explicit logger configuration (IMPORTANT)
logger = logging.getLogger("db_health_check")
logger.setLevel(logging.INFO)

# Prevent duplicate handlers
if not logger.handlers:
    file_handler = logging.FileHandler(LOG_FILE)
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

def load_config():
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)

def db_health_check():
    db = load_config()["database"]
    password = os.getenv(db["password_env"])

    try:
        conn = psycopg2.connect(
            host=db["host"],
            port=db["port"],
            dbname=db["name"],
            user=db["user"],
            password=password
        )

        cur = conn.cursor()
        logger.info("DB Health Check: Connection successful")

        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_schema='public'
                AND table_name='orders'
            );
        """)
        table_exists = cur.fetchone()[0]

        if not table_exists:
            logger.error("DB Health Check: orders table NOT found")
            return

        logger.info("DB Health Check: orders table exists")

        cur.execute("SELECT COUNT(*) FROM orders;")
        row_count = cur.fetchone()[0]

        logger.info(f"DB Health Check: orders row count = {row_count}")

        cur.close()
        conn.close()

        logger.info("DB Health Check: COMPLETED SUCCESSFULLY")

    except Exception as e:
        logger.error(f"DB Health Check: FAILED | {e}")

if __name__ == "__main__":
    db_health_check()

