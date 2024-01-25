"""EX 2.7 server implementation
   Author: Noam Miller
   Date: 25.1.24
"""

import socket
import protocol
import os
import glob
import shutil
import subprocess
import pyautogui


IP = '127.0.0.1' # localhost
PHOTO_PATH =  r'YOUR_OWN_PATH\screenshot.png'


def check_client_request(cmd):
    """
    Break cmd to command and parameters
    Check if the command and params are good.

    For example, the filename to be copied actually exists

    Returns:
        valid: True/False
        command: The requested cmd (ex. "DIR")
        params: List of the cmd params (ex. ["c:\\cyber"])
    """
    if not protocol.check_cmd(cmd):
        return False, "", []

    parts = cmd.split(' ', 1)
    command = parts[0]
    params = parts[1].split(' ') if len(parts) > 1 else []

    return True, command, params


def handle_client_request(command, params):
    try:
        if command == 'DIR':
            path = params[0]
            files_list = glob.glob(os.path.join(path, '*'))
            return '\n'.join(files_list)

        elif command == 'DELETE':
            path = params[0]
            print(f"Attempting to delete: {path}")  # Debugging line
            if not os.path.exists(path):
                return f'Error: File not found at {path}'
            os.remove(path)
            return 'File deleted successfully'

        elif command == 'COPY':
            src, dst = params
            shutil.copy(src, dst)
            return 'File copied successfully'

        elif command == 'EXECUTE':
            program = params[0]
            subprocess.call(program, shell=True)
            return f'Program {program} executed successfully'

        elif command == 'TAKE_SCREENSHOT':
            screenshot = pyautogui.screenshot()
            screenshot.save(PHOTO_PATH)
            return 'Screenshot taken and saved'

        elif command == 'SEND_PHOTO':
            return str(os.path.getsize(PHOTO_PATH))

        elif command == 'EXIT':
            return True

        else:
            return 'Error: Unknown command'

    except Exception as e:
        return f'Error: {e}'

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, protocol.PORT))
    server_socket.listen(1)
    client_socket, client_address = server_socket.accept()

    while True:
        valid_protocol, cmd = protocol.get_msg(client_socket)
        if valid_protocol:
            valid_cmd, command, params = check_client_request(cmd)
            if valid_cmd:
                if command == 'SEND_PHOTO':
                    # Handle SEND_PHOTO differently as it involves sending a file
                    try:
                        file_size = os.path.getsize(PHOTO_PATH)
                        # Send file size as 4-byte big-endian integer
                        client_socket.send(file_size.to_bytes(4, 'big'))

                        with open(PHOTO_PATH, 'rb') as file:
                            # Read and send file in chunks
                            bytes_sent = 0
                            while bytes_sent < file_size:
                                file_data = file.read(1024)  # Chunk size
                                if not file_data:
                                    break
                                client_socket.send(file_data)
                                bytes_sent += len(file_data)
                    except FileNotFoundError:
                        response = "File not found"
                        packet = protocol.create_msg(response)
                        client_socket.send(packet)
                    except Exception as e:
                        response = f"Error: {e}"
                        packet = protocol.create_msg(response)
                        client_socket.send(packet)

                else:
                    # Handle other commands
                    response = handle_client_request(command, params)
                    packet = protocol.create_msg(response)
                    client_socket.send(packet)

                if command == 'EXIT':
                    break
            else:
                response = 'Bad command or parameters'
                client_socket.send(protocol.create_msg(response))
        else:
            response = 'Packet not according to protocol'
            client_socket.send(protocol.create_msg(response))
            client_socket.recv(1024)

    client_socket.close()
    server_socket.close()
    print("Closing connection")

if __name__ == '__main__':
    main()