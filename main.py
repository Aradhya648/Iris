import logging
from iris.pipeline import run_pipeline  # BUG: module does not exist

logging.basicConfig(level=logging.INFO)

def main():
    logging.info("Starting Iris system")
    print("Hello, World!")
    status = "active"
    print(f"Status: {status}")
    result = run_pipeline()
    print(f"Pipeline result: {result}")

if __name__ == "__main__":
    main()
