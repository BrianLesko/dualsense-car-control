# Brian Lesko
# Ethernet communication class

import socket
import pandas as pd

class ethernet:

    def __init__(self, name, IP, PORT, SUBNETMASK = "MASK"):
        self.name = name
        self.IP = IP
        self.PORT = PORT
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Set the send buffer size
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 112)
        # Set the receive buffer size
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 112)
        self.s.settimeout(5)  # Set a timeout of 5 seconds

    def connect(self):
        messages = []
        try: 
            self.s.connect((self.IP, self.PORT))
            messages.append(f'The connection with *{self.name}* established.')
            self.connected = True
        except socket.error as e:
            messages.append(f'Sorry, the connection with *{self.name}* was not established.')
            messages.append(e)
        return messages
    
    def is_connected(self):
        if self.s.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR) == 0:
            self.connected = True
        else:
            self.connected = False
        return self.connected

    
    def disconnect(self): 
        self.s.close()
        return f"The connection with *{self.name}* was closed."
    
    def receive(self):
        response = self.s.recv(1024) # Max amount of bytes to receive
        if response:
            return response.decode()
        else:
            return None

    def send(self, command):
        if isinstance(command, str):
            bytes = command.encode()
        else:
            bytes = str(command).encode("utf-8")
        self.s.sendall(bytes)

    def send_and_receive(self, command):
        if isinstance(command, str):
            bytes = command.encode()
        else:
            bytes = str(command).encode("utf-8")
        self.s.sendall(bytes)
        response = self.s.recv(1024) # Max amount of bytes to receive
        if response:
            return response.decode()
        else:
            return None 
    
    def to_df(self):
        df = pd.DataFrame({'name': [self.name], 'ipv4': [self.IP], 'port': [self.PORT]})
        return df
    
    @classmethod
    def from_excel(cls, excel_file_name):
        # To create a list of ethernet objects from an excel file
        ethernets = []
        data_types = {
            'ipv4': str,
            'port': int,
            'subnetmask': str
        }
        external_connections = pd.read_excel(excel_file_name, index_col=None)
        external_connections = external_connections.astype(data_types)
        for i in range(len(external_connections)):
            name = external_connections['name'][i]
            IP = external_connections['ipv4'][i]
            PORT = external_connections['port'][i]
            ethernet = cls(name, IP, PORT)
            ethernets.append(ethernet)
        return ethernets
    
    # WIP - need to test this
    def get_local_ip():
        # This will only work on Linux
        import subprocess
        IP= subprocess.run(["hostname", "-I"],stdout=subprocess.PIPE,text=True).stdout
        return IP

    def get_subnet_mask():
        netmask = "255.255.255.0"
        return netmask
    
    def check_connection_compatibility(self):
        if self.get_local_ip().split('.')[0:3] == self.IP.split('.')[0:3]:
            response = 'Your computer and *{self.name}* are ready to connect.'
            errors = False
        else: 
            response = 'Your host computer and *{self.name}* cannot communicate.' + "\n" + """
                - Are the IP addresses in the same range? 
                - Is the printer connected on the same ethernet as the computer?
                - Do the port and IP specified above match the printer settings?
                """
            errors = True
        return response, errors
