# main.py
import time
import logging

logging.basicConfig(level=logging.INFO)


def greet(name: str) -> str:
    return f"Hello, {name}"


def main():
    logging.info("Starting Iris system")
    msg = greet()
    print(msg_typo_xyz)


if __name__ == "__main__":
    main()
