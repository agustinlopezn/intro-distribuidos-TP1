from sys import argv
from src.lib.options import InvalidOptionsError, ServerOptions
from src.server import Server


def start_server():
    try:
        options = ServerOptions(argv[1:])
        if options.show_help:
            raise InvalidOptionsError()
        server = Server(options)
        server.daemon = True
        print("Server running on port ", options.port)
        server.start()

        while True:
            quit = input("Press q to exit gracefully, then CTRL+C\n")
            if quit == "q":
                break
        server.stop()
        server.join()

    except KeyboardInterrupt:
        print("\n-- Exiting --")
        exit(0)

    except InvalidOptionsError as e:
        print("Error parsing options: ", e)
        print("Usage: start-server [-h] [-v | -q] [-H ADDR] [-p PORT] [-s DIRPATH]")
        exit(1)

    except:
        print("An unknown error occurred")
        input("Press enter to exit")
        exit(1)


if __name__ == "__main__":
    start_server()
