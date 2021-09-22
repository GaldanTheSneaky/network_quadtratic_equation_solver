import socket
import enum


class ApplicationType(enum.Enum):
    sum  = 0
    sub  = 1
    mult = 2
    div  = 3
    sqrt = 4


class ClientApp:
    def __init__(self, header, port, host, app_type, format='utf-8', disconnect_message="!DISCONNECT",
                 client_function=None):
        """Creates a client that can perform 1 mathematical operation

               Args:
                   header: header of message
                   port: port
                   format: encoding format
                   disconnect_message: message to send clients before disconnect
                   client_function: function to perform
               """
        self._header = header
        self._port = port
        self._host = host
        self._addr = (self._host, self._port)
        self._format = format
        self._app_type = app_type
        self._disconnect_message = disconnect_message
        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._client.connect(self._addr)
        self._client_function = client_function

    def send(self, msg: str) -> None:
        """Encodes message and send it to server
        """
        message = msg.encode(self._format)
        msg_length = len(message)
        send_length = str(msg_length).encode(self._format)
        send_length += b' ' * (self._header - len(send_length))
        self._client.send(send_length)
        self._client.send(message)
        print(self._client.recv(2048).decode(self._format))

    def run(self) -> None:
        """Runs an application. Performs given operation on numbers received from server until disconnect_message
        """
        self.send(str(self._app_type.value))

        while True:
            msg_length = self._client.recv(self._header).decode(self._format)
            if msg_length:
                msg_length = int(msg_length)
                msg = self._client.recv(msg_length).decode(self._format)
                if msg == self._disconnect_message:
                    break

                print(f"[{self._host}] {msg}")

                expression = msg.split()
                print(expression[0])
                if expression[0] == '2':
                    a, b = map(float, expression[1:])
                    msg = self._client_function(a, b)
                else:
                    a = float(expression[1])
                    msg = self._client_function(a)

                self._client.send(f"{msg}".encode(self._format))

            print("server disconnected")





