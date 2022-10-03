from src.client import Client


if __name__ == "__main__":
    try:
        Client().upload()

    except KeyboardInterrupt:
        print("\n-- Exiting --")
        exit(0)
    except ConnectionRefusedError:
        print("\n-- Connection aborted --")
        input("Press enter to exit...")
        exit(1)
    except:
        print("An unknown error occurred")
        input("Press enter to exit")
        exit(1)
