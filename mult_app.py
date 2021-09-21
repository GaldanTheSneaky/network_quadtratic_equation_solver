from client import ClientApp
from client import ApplicationType


def client_mult(a, b):
    return a*b

def main():
    client = ClientApp(64, 5050, "192.168.1.4", ApplicationType.mult, client_function=client_mult)
    client.run()


if __name__ == '__main__':
    main()