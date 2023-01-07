Author: Meg Zhang
12/8/22

Usage:
**** Please start "discovery.py" before launching the "room.py" instances so that these rooms can be registered and
    looked up. "player.py" will time out automatically if it is unable to connect to discovery.py, and will return an
    error if the room it is trying to find has not been started.



*** USING "discovery.py" - the room discovery service ***

1. Navigate to the directory where "discovery.py" is located.

2. In a terminal open in this directory, enter the following command:
    python3 discovery.py

NOTE: discovery.py is hardcoded to run on port 7777, and room clients and player clients are all also hardcoded to
    look for the discovery service on port 7777. Please make sure that no other service is using port 7777 so that
    discovery.py can be run.

    To stop the discovery service, CTRL+C can be pressed. This will stop the discovery signal, and will shut
    down all rooms and player clients that were connected to it.



*** USING "room.py" - the room servers ***

1. Navigate to the directory where "room.py" is located.

2. In the terminal, enter the following command to create a room with no connections:
   python3 room.py [room name] [room description] [items (can list multiple arguments)]
   example:
   python3 room.py Foyer "The entry way to an old house. Weathered, but still tidy and clean. A doorway leads away from the room to the north." Vase Rug

    A room can have none, or multiple connections. To add a connection, specify the direction, and the name of the room.
    Directions possible:
    -n north
    -s south
    -e east
    -w west
    -u up
    -d down

    Usage:
    ex. to create a connection to the north: -n Study
    ex. to create a connection to the south: -s Foyer

    The full commands for the above two examples would look like this:
    python3 room.py -n Study Foyer "The entry way to an old house. Weathered, but still tidy and clean. A doorway leads away from the room to the north." Vase Rug
    python3 room.py -s Foyer Study "An old study. Some manner of business apparently was run from here. A doorway leads away from the room to the south." desk lamp books paper

    To stop the server, press ctrl+C in the terminal where "room.py" is running. This will also disconnect any
    game clients that are connected, and will DEREGISTER the room server from the discovery service.



*** USING "player.py" - the game client ***
USING "player.py" - the game client

1. Navigate to the directory where "player.py" is located.

2. In the terminal, enter the following command:
    python3 player.py [player name] [name of starting room]
    example:
    python3 player.py Meg Foyer

3. Upon connecting to the server, the room's name, description, and items will be displayed in the client.
    From here, you can do the following commands:

    look: Displays the name, description and contents of the room.
    take [item]: Take an item from the room and add it to player's inventory (e.g. take vase)
    drop [item]: Take an item from player's inventory and add it to the room.
    inventory: list the player's inventory.
    say [user inputted sentence]: this sends a message to everyone else in the room.
    exit: Leaves the game and terminates the game client.

    Additionally, there are the following directional commands to enter other rooms.
    north: head north, if path exists
    south: head south, if path exists
    east: head east, if path exists
    west: head west, if path exists
    up: head up, if path exists
    down: head down, if path exists

    Pressing ctrl + C will disconnect you from the room server.
