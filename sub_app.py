from client import ClientApp
from client import ApplicationType


def client_sub(a, b):
    return a-b


def main():
    client = ClientApp(64, 5050, "192.168.1.4", ApplicationType.sub, client_function=client_sub)
    client.run()


if __name__ == '__main__':
    main()