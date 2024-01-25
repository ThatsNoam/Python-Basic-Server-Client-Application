"""EX 2.7 protocol implementation
   Author: Noam Miller
   Date: 25.1.24
"""

LENGTH_FIELD_SIZE = 4
PORT = 8820


def check_cmd(data):
    """
    Check if the command is defined in the protocol, including all parameters
    For example, DELETE c:\work\file.txt is good, but DELETE alone is not
    """

    parts = data.split(' ', 2)  # Split into command and parameters
    command = parts[0]

    if command not in ["EXIT", "DIR", "TAKE_SCREENSHOT", "SEND_PHOTO", "COPY", "DELETE", "EXECUTE"]:
        return False

    # Commands that require at least one parameter
    if command in ["DIR", "DELETE", "EXECUTE"]:
        return len(parts) >= 2

    # COPY command requires at least two parameters
    elif command == "COPY":
        return len(parts) >= 3

    # Commands that do not require additional parameters
    return True
def create_msg(data):
    """
    Create a valid protocol message, with length field
    """

    length = str(len(data)).zfill(LENGTH_FIELD_SIZE)
    return (length + data).encode()


def get_msg(my_socket):
    """
    Extract message from protocol, without the length field
    If length field does not include a number, returns False, "Error"
    """

    length_field = my_socket.recv(LENGTH_FIELD_SIZE).decode()
    if not length_field.isdigit():
        return False, "Error"

    length = int(length_field)
    message = my_socket.recv(length).decode()
    return True, message

