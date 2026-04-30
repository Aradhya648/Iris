import logging

def greet(name):
    return f"Hello, {name}!"

def main():
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting Iris system")
    msg = greet("World")
    print(msg)
    print(f"Status: {status}")

if __name__ == "__main__":
    main()
