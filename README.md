# README: Chat Application Using Python and Tkinter

## Description

This project is a simple chat application built using Python's socket, threading, and tkinter libraries. It consists of a server and client application that facilitates communication between multiple users over a local network. Each client can either broadcast messages to all connected users or send private messages to specific users.

---

## Features

1. *Graphical User Interface (GUI):*
   - Built using tkinter.
   - User-friendly interface for both server and client.

2. *Messaging Options:*
   - Broadcast messages to all users.
   - Send private messages to specific users.

3. *Dynamic User List:*
   - Automatically updates the list of connected users on the client.

4. *Multi-threaded Communication:*
   - Handles multiple clients concurrently using threading.

5. *Error Handling:*
   - Alerts for connection errors, invalid inputs, or server conflicts.

---

## Requirements

1. Python 3.x
2. Required libraries:
   - tkinter
   - socket
   - threading
   - queue

---

## File Structure

- *server.py*: Contains the server-side logic and GUI.
- *client.py*: Contains the client-side logic and GUI.

---

## Installation

1. Clone the repository or download the files.
2. Ensure Python 3.x is installed on your machine.
3. Install any missing dependencies:
   bash
   pip install tk
   
4. Run the server first:
   bash
   python server.py
   
5. Launch the client:
   bash
   python client.py
   

---

## Usage

### Server:

1. Start the server using the "Start Server" button.
2. Add clients by entering their name, host (e.g., 127.0.0.1), and port (5678) and clicking "Add Client."
3. Broadcast messages to all connected clients using the text box and "Send" button.

### Client:

1. Enter the name for the client upon launch.
2. Select "All" to broadcast messages or choose a specific user from the dropdown menu to send private messages.
3. Type the message in the input box and click "Send" to deliver the message.

---

## Limitations

1. This chat application is designed for local networks and uses a fixed IP (127.0.0.1) and port (5678).
2. It does not use encryption, so it is not secure for sensitive information.
3. Error handling for certain edge cases may need improvements.

---

## Future Enhancements

1. Add authentication and user registration.
2. Implement encryption for secure messaging.
3. Extend support for internet-based communication.
4. Add file-sharing capabilities.
5. Implement a persistent chat log.

---

## Credits

Developed by MD.Mushfiqur Rahman Sakib, ID:213-134-021 and MD.Absaruzzaman Omi,ID:222-134-026. This project demonstrates the use of Python for creating basic chat systems with a graphical interface.
