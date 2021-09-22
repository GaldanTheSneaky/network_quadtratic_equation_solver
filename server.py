import socket
import threading
import enum


class ApplicationType(enum.Enum):
    sum  = 0
    sub  = 1
    mult = 2
    div  = 3
    sqrt = 4


class Server:
    def __init__(self, header, port, connection_slots=1, format='utf-8', disconnect_message="!DISCONNECT"):
        """Creates a server for solving quadratic equations with multiple remote clients performing mathematical
        operations

        Args:
            header: header of message
            port: port
            connection_slots: number of allowed connections to server
            format: encoding format
            disconnect_message: message to send clients before disconnect
        """
        self._header = header
        self._port = port
        self._host = socket.gethostbyname(socket.gethostname())
        self._addr = (self._host, self._port)
        self._format = format
        self._disconnect_message = disconnect_message
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.bind(self._addr)
        self._connections = [(None, None)] * 5
        self._connection_slots = connection_slots
        self.a = 0
        self.b = 0
        self.c = 0

    def set_coefficients(self, a, b, c) -> None:
        """Set coefficients of quadratic equation ax^2+bx+c
        """
        self.a = a
        self.b = b
        self.c = c

    def register_client(self, conn, addr) -> None:
        """"Saves all clients and their type

            Args:
                conn: socket object
                addr: address
        """
        print(f"[NEW CONNECTION] {addr} connected.")

        msg_length = conn.recv(self._header).decode(self._format)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(self._format)
            self._connections[int(msg)] = ((conn, addr))

            print(f"[{addr}] {msg}")
            conn.send(f"Msg received '{msg}'".encode(self._format))

    def handle_clients(self) -> None:
        """Accepts <connection_counter> connections and register them
        """
        self._server.listen()
        print(f"[LISTENING] Server is listening on {self._host}")
        connection_counter = 0
        while connection_counter < self._connection_slots:
            conn, addr = self._server.accept()
            self.register_client(conn, addr)
            connection_counter += 1
            print(f"[ACTIVE CONNECTIONS] {connection_counter}")

    def encode_msg(self, msg: str) -> tuple:
        """Encodes message and its length to byte format
        """
        message = msg.encode(self._format)
        msg_length = len(message)
        send_length = str(msg_length).encode(self._format)
        send_length += b' ' * (self._header - len(send_length))
        return send_length, message

    def binary_operation(self, a, b, type) -> float:
        """Sends a request to binary operation
            first sent character is the number of operands

        Args:
            a: first operand
            b: second operand
            type: type of the operation, enum
        """
        msg = f"{2} {a} {b}"
        conn = self._connections[type.value][0]
        send_length, msg = self.encode_msg(msg)
        conn.send(send_length)
        conn.send(msg)

        result = conn.recv(2048).decode(self._format)
        return float(result)

    def unary_operation(self, a, type) -> float:
        """Sends a request to unary operation
            first sent character is the number of operands

                Args:
                    a: first operand
                    type: type of the operation, enum
                """
        msg = f"{1} {a}"
        conn = self._connections[type.value][0]
        send_length, msg = self.encode_msg(msg)
        conn.send(send_length)
        conn.send(msg)

        result = conn.recv(2048).decode(self._format)
        return float(result)

    def disconnect_all(self) -> None:
        """Sends clients disconnect message and breaks the connections
        """
        send_length, msg = self.encode_msg(self._disconnect_message)
        for conn in self._connections:
            conn[0].send(send_length)
            conn[0].send(msg)
            conn[0].close()

    def solve_equation(self) -> tuple:
        """Solves quadratic equation
        """
        a = self.a
        b = self.b
        c = self.c
        # d = b*b - 4*a*c
        b_sq = self.binary_operation(b, b, ApplicationType.mult)
        a_c = self.binary_operation(4, a, ApplicationType.mult)
        a_c = self.binary_operation(a_c, c, ApplicationType.mult)
        d = self.binary_operation(b_sq, a_c, ApplicationType.sub)

        if d > 0:
            d_sqrt = self.unary_operation(d, ApplicationType.sqrt)
            neg_b = self.binary_operation(0, b, ApplicationType.sub)
            a_2 = self.binary_operation(a, 2, ApplicationType.mult)

            x1 = self.binary_operation(neg_b, d_sqrt, ApplicationType.sum)
            x1 = self.binary_operation(x1, a_2, ApplicationType.div)

            x2 = self.binary_operation(neg_b, d_sqrt, ApplicationType.sub)
            x2 = self.binary_operation(x2, a_2, ApplicationType.div)

        elif d == 0:
            neg_b = self.binary_operation(0, b, ApplicationType.sub)
            a_2 = self.binary_operation(a, 2, ApplicationType.mult)

            x1 = self.binary_operation(neg_b, a_2, ApplicationType.div)
            x2 = x1
        else:
            raise Exception("Equation has no roots!")

        return x1, x2

    def run(self) -> None:
        """Runs the server
        """
        self.handle_clients()
        print(self.solve_equation())
        self.disconnect_all()





def main():
    server = Server(64, 5050, connection_slots=5)
    server.set_coefficients(1, 0, -2)
    server.run()


if __name__ == '__main__':
    main()