# Author: Isabella Samuelsson
# Date: 10/7/22
import sys
from socket import *

"""
Auction client class. If you are the first to connect to the server you will be connected as a seller client, if not you 
will be connected as a buyer client. Bids must be an integer greater than zero.

Seller Client: Once connected you will be prompted to enter auction information. This includes Auction Type: 1 
for a first price auction and 2 for a second price auction, Minimum Bid price: non-negative integer, Number of Bidders: 
non-negative integer less than 10 and Item Name: string. If you enter invalid auction information you will be prompted for valid information before continuing.

Buyer Client: Once connected you will be prompted to enter a bid. A bid should be a non-negative integer, if an invalid 
bid is given you will be prompted again.

Run example: python3 auc_client.py server_ip_address server_port_number
"""
class auc_client:
    # default server name and port
    serverName = "192.168.0.15"
    serverPort = 12345

    """ Initializes server name and port from run command arguments and starts the main() function."""
    def __init__(self):
        self.serverName = sys.argv[1]
        self.serverPort = int(sys.argv[2])
        self.main()

    """ 
    Creates a connection to the auction server. 
    - If you are the first to connect to the server you will be connected as a seller client, if not you will be 
    connected as a buyer client. 
    - If the client connects when the sever is busy setting up a seller connection or the server is busy handling 
    bidding the client will receive a "connect again later" message and the client will close the socket and exit. 
    """
    def main(self):
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((self.serverName, self.serverPort))        # client connection

        client_status_msg = clientSocket.recv(1024).decode()
        if "connect again later" in client_status_msg:                  # if server sends a busy msg disconnect and exit
            print(client_status_msg)
            clientSocket.close()
            exit()
        if "Seller" in client_status_msg:                               # if client is a buyer prompt for auction info
            auc_info_msg = input(client_status_msg)
            clientSocket.send(auc_info_msg.encode())
            received_auc_info = clientSocket.recv(1024).decode()

            while "Invalid" in received_auc_info:                       # if invalid auction info given prompt again
                new_auc_info = input(received_auc_info)
                clientSocket.send(new_auc_info.encode())
                received_auc_info = clientSocket.recv(1024).decode()

            print(received_auc_info)

            auction_finished = clientSocket.recv(1024).decode()
            print(auction_finished)

        else:                                                           # if client is a seller wait for bid start
            print(client_status_msg)
            did_bid_start = clientSocket.recv(1024).decode()
            if "waiting" in did_bid_start:
                print(did_bid_start)
                did_bid_start = clientSocket.recv(1024).decode()

            bid = input(did_bid_start)                                  # at bid start prompt for bid
            clientSocket.send(bid.encode())
            received_bid = clientSocket.recv(1024).decode()

            while "Invalid" in received_bid:                            # if bid is invalid prompt again
                new_bid = input(received_bid)
                clientSocket.send(new_bid.encode())
                received_bid = clientSocket.recv(1024).decode()

            print(received_bid)

            auction_finished = clientSocket.recv(1024).decode()         # print auction result and disconnect
            print(auction_finished)

        clientSocket.close()

""" Creates a client object. """
if __name__ == "__main__":
    client = auc_client()

