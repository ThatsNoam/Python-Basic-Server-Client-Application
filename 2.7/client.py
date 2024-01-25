"""EX 2.7 client implementation
   Author: Noam Miller
   Date: = 25.1.24
"""
import socket
import protocol


SERVER_PORT = 8820
IP = '127.0.0.1'
SAVED_PHOTO_LOCATION = r'YOUR_OWN_PATH/screenshot.png'

def handle_server_response(my_socket, cmd):
    """
    Receive the response from the server and handle it, according to the request
    For example, DIR should result in printing the contents to the screen,
    Note - special attention should be given to SEND_PHOTO as it requires and extra receive
    """
    if cmd != 'SEND_PHOTO':
        response = my_socket.recv(1024).decode()
        print(response)
    else:
        file_size = int.from_bytes(my_socket.recv(4), 'big')
        # Receive and write the file
        with open(SAVED_PHOTO_LOCATION, 'wb') as file:
            bytes_received = 0
            while bytes_received < file_size:
                data = my_socket.recv(1024)
                if not data:
                    break
                file.write(data)
                bytes_received += len(data)


def main():
    # Establish a connection to the server
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        my_socket.connect((IP, SERVER_PORT))
    except ConnectionError:
        print("Failed to connect to the server.")
        return

    # Print instructions
    print('Welcome to remote computer application. Available commands are:')
    print('TAKE_SCREENSHOT\nSEND_PHOTO\nDIR\nDELETE\nCOPY\nEXECUTE\nEXIT')

    # Loop until user requests to exit
    while True:
        cmd = input("Please enter command:\n")
        if protocol.check_cmd(cmd):
            packet = protocol.create_msg(cmd)
            my_socket.send(packet)
            handle_server_response(my_socket, cmd)
            if cmd.startswith('EXIT'):
                break
        else:
            print("Not a valid command, or missing parameters\n")

    my_socket.close()

if __name__ == '__main__':
    main()