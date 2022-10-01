from src.server import Server


if __name__ == "__main__":

    try:
        server = Server()
        server.daemon = True
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

    except:
        print("An unknown error occurred")
        input("Press enter to exit")
        exit(1)
