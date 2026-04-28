import logging

def greet(name="World"):
    return f"Hello, {name}!"

def main():
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting Iris system")
    msg = greet()
    print(msg)

if __name__ == "__main__":
    main()
