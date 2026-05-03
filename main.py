import logging

logging.basicConfig(level=logging.INFO)

def main():
    logging.info("Starting Iris system")
    print("Hello, World!")
    status = "active"
    print(f"Status: {status}")

if __name__ == "__main__":
    main()
