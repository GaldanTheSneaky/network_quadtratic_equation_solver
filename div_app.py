from client import ClientApp
from client import ApplicationType


def client_div(a, b):
    return a/b

def main():
    client = ClientApp(64, 5050, "192.168.1.4", ApplicationType.div, client_function=client_div)
    client.run()


if __name__ == '__main__':
    main()