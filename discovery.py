import signal
import socket
import sys
from urllib.parse import urlparse

# Author: Meg Zhang
# Date: 11/18/22

# discovery service socket
discovery_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# port that the discovery service will run on
PORT = 7777

# Dictionary containing room names and port numbers
rooms = dict()


# set up discovery service socket
def initialize_discovery():
    global discovery_socket

    # set up the port.
    discovery_socket.bind(('', PORT))

    print("The discovery service is now running on port " + str(PORT))


#  Signal handler - send a signal to all rooms to shut down
def signal_handler(sig, frame):
    message = 'disconnect'
    for key in rooms.keys():
        discovery_socket.sendto(message.encode(), ("", rooms.get(key)))

    print("Interrupt received, shutting down ...")
    sys.exit(0)


# Room debug printer
def print_rooms():
    print("Current rooms: ")
    print(rooms)
    print("")


# REGISTER function - returns OK if room is registered, else NOT OK
def register(roomname, port):
    # create URL
    URL = "room://" + roomname + ":" + str(port[1])
    # parse URL
    connection_address = urlparse(URL)

    # Check for duplicate room name
    if not rooms.get(connection_address.hostname):
        # check for duplicate room port
        check_empty = [key for key, value in rooms.items() if value == connection_address.port]

        if not check_empty:  # port is not a duplicate
            # Record name to address mapping.
            roomname = connection_address.hostname
            port = connection_address.port
            rooms.update({roomname: port})
            print(URL + " has been registered.")
            print_rooms()
            return "OK - Room has been registered"

        else:
            print(URL + " could not be registered as the port already has a room registered to it.")
            print_rooms()
            return "NOTOK The port already has a room registered to it."

    else:
        # Room name or port is a duplicate, return NOT OK.
        print(roomname + " is a duplicate and could not be registered.")
        print_rooms()
        return "NOTOK The room name has already been registered."


# DEREGISTER function - returns OK if room is deleted, else NOT OK
def deregister(roomname):
    try:
        deleted_room = rooms.pop(roomname)
        print(roomname + " has been deregistered")
        print_rooms()
        return "OK - Room has been deregistered"

    except KeyError:
        print(roomname + " could not be deregistered")
        print_rooms()
        return "NOTOK The room to be deleted does not exist."


# LOOKUP function - returns room address if room exists, otherwise returns NOT OK
def lookup(roomname):
    # Find the room, then return the address.
    if rooms.get(roomname):
        port = rooms.get(roomname)
        print("A successful lookup occurred for " + roomname)
        address = "room://" + roomname + ":" + str(port)
        return address

    else:
        print("A failed lookup occurred for " + roomname)
        return "NOTOK - Room does not exist"


#  process messages from room
def process_message(message, addr, disc_socket):
    # parse the message
    words = message.split()

    # REGISTER Function - Usage: REGISTER roomname, port
    if words[0] == "REGISTER":
        return register(words[1], addr)

    # DEREGISTER Function - usage: DEREGISTER roomname
    if words[0] == "DEREGISTER":
        return deregister(words[1])

    # LOOKUP function - usage: LOOKUP roomname
    if words[0] == "LOOKUP":
        return lookup(words[1])


# Our main function
def main():
    #  Register our signal handler for shutting down.
    signal.signal(signal.SIGINT, signal_handler)

    initialize_discovery()  # set up the socket

    # loop forever waiting for messages from rooms
    while True:
        # receive a packet from a room and process it.
        message, addr = discovery_socket.recvfrom(1024)

        # process the message and retrieve a response.
        response = process_message(message.decode(), addr, discovery_socket)

        if response is not None:
            # send the response message back to the room
            discovery_socket.sendto(response.encode(), addr)


if __name__ == '__main__':
    main()
