from src.client import Client


if __name__ == "__main__":
    try:
        Client().download()

    except KeyboardInterrupt:
        print("\n-- Exiting --")
        exit(0)

    except:
        print("An unknown error occurred")
        input("Press enter to exit")
        exit(1)
