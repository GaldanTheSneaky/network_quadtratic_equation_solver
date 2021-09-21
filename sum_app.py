from client import ClientApp
from client import ApplicationType


def client_sum(a, b):
    return a + b


def main():
    client = ClientApp(64, 5050, "192.168.1.4", ApplicationType.sum, client_function=client_sum)
    client.run()


if __name__ == '__main__':
    main()