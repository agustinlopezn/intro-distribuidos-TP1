from sys import argv
from src.lib.options import InvalidOptionsError, ServerOptions
from src.server import Server


def print_usage():
    print(
        "usage: start-server [-h] [-v | -q] [-H ADDR] [-p PORT] [-s DIRPATH]",
        end="\n\n",
    )
    print(
        "Starts the server for the clients to connect and upload/download files. The default port will grabbed from the enviroment variable",
        end="\n\n",
    )
    print("optional arguments:")
    print("-h, --help show this help message and exit")
    print("-v, --verbose increase output verbosity")
    print("-q, --quiet decrease output verbosity")
    print("-H, --host service IP address")
    print("-p, --port service port")
    print("-s, --storage storage dir path")


def start_server():
    try:
        options = ServerOptions(argv[1:])
        if options.show_help:
            print_usage()
            return
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
        print_usage()
        exit(1)

    except:
        print("An unknown error occurred")
        input("Press enter to exit")
        exit(1)


if __name__ == "__main__":
    start_server()
