from src.client import Client


if __name__ == "__main__":
    try:
        Client.upload()
    except Exception as e:
        raise(e)
        # print("An exception occurred: ", e)
        # input("Press enter to exit")
        # exit(1)