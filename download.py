from src.client import Client


if __name__ == "__main__":
    try:
        Client.download()
    except Exception as e:
        print("An exception occurred: ", e)
        input("Press enter to exit")
        exit(1)