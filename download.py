from src.lib.options import InvalidOptionsError
from src.client import Client, print_download_usage as print_usage


if __name__ == "__main__":
    try:
        Client().download()

    except KeyboardInterrupt:
        print("\n-- Exiting --")
        exit(0)

    except ConnectionRefusedError:
        print("\n-- Connection aborted --")
        input("Press enter to exit...")
        exit(1)

    except InvalidOptionsError as e:
        print("Error parsing options: ", e)
        print_usage()
        exit(1)

    except:
        print("An unknown error occurred")
        input("Press enter to exit")
        exit(1)
