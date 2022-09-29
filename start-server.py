

from src.server import Server


if __name__ == "__main__":
    try:
        Server().start_server()
    except Exception as e:
        print("An exception occurred: ", e)
        input("Press enter to exit")
        exit(1)