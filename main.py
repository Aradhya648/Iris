import logging
import pandas as pd

logging.basicConfig(level=logging.INFO)

def main():
    logging.info("Starting Iris system")
    df = pd.DataFrame({"score": [0.1, 0.5, 0.9]})
    print(df)
    status = "active"
    print(f"Status: {status}")

if __name__ == "__main__":
    main()
