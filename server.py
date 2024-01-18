"""EX 2.6 server implementation
   Author: Noam Miller
   Date: 18.1.24
"""

import socket
import protocol

def create_server_rsp(cmd):
    """Based on the command, create a proper response"""
    if cmd == "TIME":
        import datetime
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        return current_time
    elif cmd == "WHORU":
        return "2.6 SERVER"
    elif cmd == "RAND":
        import random
        return str(random.randint(1, 10))
    elif cmd == "EXIT":
        return None
    else:
        return "Unknown command"

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", protocol.PORT))
    server_socket.listen()
    print("Server is up and running")
    (client_socket, client_address) = server_socket.accept()
    print("Client connected")

    while True:
        valid_msg, cmd = protocol.get_msg(client_socket)
        if valid_msg:
            print(f"Received command: {cmd}")

            if cmd == "EXIT":
                break

            if protocol.check_cmd(cmd):
                response = create_server_rsp(cmd)
            else:
                response = "Unknown command"
        else:
            response = "Wrong protocol"
            client_socket.recv(1024)

        try:
            if response is not None:
                client_socket.sendall(protocol.create_msg(response).encode())
        except Exception as e:
            print(f"Error sending response: {str(e)}")

    print("Closing\n")
    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    main()
