import socket

ip_address_list = ['31.13.74.36', '172.217.14.174', '40.97.142.194']
for ip in ip_address_list:
    print("Begin IP Scan on: " + ip + ".")
    try:
        for port in range(1,1000):
            #Create the Socket
            aSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #Set the timeout to 2 seconds
            aSocket.settimeout(1)
            #Attempt to connect
            res = aSocket.connect_ex((ip, port))
            if res == 0: #If res is 0, then the port is open.
                print("IP: " + str(ip) + " | Port Number " + str(port) + " is open.")
            else: #Otherwise, the port is considered closed
                print("IP: " + str(ip) + " | Port Number " + str(port) + " is closed.")
            #Close the socket
            aSocket.close()
    #Timeout exception
    except socket.timeout:
        print("Timeout has happened.")
    #Failure to connect to server exception
    except socket.error:
        print("Could not connect to the server.")
print("I have finished scanning the ports.")


