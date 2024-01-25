"""EX 2.6 protocol implementation
   Author:
   Date:
"""

LENGTH_FIELD_SIZE = 2
PORT = 8820

def check_cmd(data):
    """Check if the command is defined in the protocol (e.g., RAND, NAME, TIME, EXIT)"""
    valid_commands = ["RAND", "WHORU", "TIME", "EXIT"]
    return data in valid_commands

def create_msg(data):
    """Create a valid protocol message, with length field"""
    length = str(len(data))
    if len(length) < LENGTH_FIELD_SIZE:
        length = length.zfill(LENGTH_FIELD_SIZE)
    return length + data

def get_msg(my_socket):
    """Extract a message from the protocol, without the length field
       If the length field does not include a number, return False, "Error" """
    try:
        # Receive the length field from the socket
        length_field = my_socket.recv(LENGTH_FIELD_SIZE).decode()

        # Check if the length field contains a valid number
        if not length_field.isdigit():
            return False, "Error"

        # Convert the length field to an integer to determine message length
        length = int(length_field)

        # Receive the actual message
        message = my_socket.recv(length).decode()

        # Return the received message
        return True, message
    except ValueError:
        return False, "Error"
    except Exception as e:
        return False, str(e)
