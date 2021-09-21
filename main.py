from server import Server


def main():
    server = Server(64, 5050, connection_slots=5)
    server.set_coefficients(1, 0, -2)
    server.run()



if __name__ == '__main__':
    main()