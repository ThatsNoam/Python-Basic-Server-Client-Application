"""EX 2.6 client implementation
   Author: Noam Miller
   Date: 18.1.24
"""

import socket
import protocol

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", protocol.PORT))

    while True:
        user_input = input("Enter command (TIME, WHORU, RAND, EXIT):\n")

        if user_input == "EXIT":
            client_socket.send(protocol.create_msg(user_input).encode())
            break

        if not protocol.check_cmd(user_input):
            print("Invalid command. It should be TIME, WHORU, RAND, or EXIT.")
            continue

        client_socket.send(protocol.create_msg(user_input).encode())
        response = client_socket.recv(1024).decode()[2:]
        print(f"Server response: {response}")

    client_socket.close()

if __name__ == "__main__":
    main()
