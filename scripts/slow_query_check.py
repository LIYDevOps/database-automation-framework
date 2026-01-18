import psycopg2
import yaml
import logging
import os
import time

# Base paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(BASE_DIR, "config", "db_config.yaml")
LOG_DIR = os.path.join(BASE_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "automation.log")

os.makedirs(LOG_DIR, exist_ok=True)

# Logger setup
logger = logging.getLogger("slow_query_check")
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.FileHandler(LOG_FILE)
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def load_config():
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)

def slow_query_check():
    config = load_config()
    db = config["database"]
    threshold = config.get("thresholds", {}).get("slow_query_seconds", 2)

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

        query = """
            SELECT COUNT(*)
            FROM orders
            WHERE amount > 1000;
        """

        start_time = time.time()
        cur.execute(query)
        cur.fetchone()
        execution_time = time.time() - start_time

        if execution_time > threshold:
            logger.warning(
                f"Slow Query Detected | Time: {execution_time:.2f}s | Threshold: {threshold}s"
            )
        else:
            logger.info(
                f"Query executed within limit | Time: {execution_time:.2f}s"
            )

        cur.close()
        conn.close()

    except Exception as e:
        logger.error(f"Slow Query Check FAILED | {e}")

if __name__ == "__main__":
    slow_query_check()
