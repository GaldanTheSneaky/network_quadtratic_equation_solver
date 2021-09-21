from client import ClientApp
from client import ApplicationType
import math


def client_sqrt(a):
    return math.sqrt(a)

def main():
    client = ClientApp(64, 5050, "192.168.1.4", ApplicationType.sqrt, client_function=client_sqrt)
    client.run()


if __name__ == '__main__':
    main()