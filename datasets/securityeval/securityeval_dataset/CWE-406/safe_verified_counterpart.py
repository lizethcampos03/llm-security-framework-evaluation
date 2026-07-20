import socket
import time
from collections import defaultdict
from threading import Lock

def parseUDPpacket(data):
    pass


def resolveName(nameToResolve):
    pass


def sendResponse(requestIP, record):
    pass


class RateLimiter:
    def __init__(self, max_requests_per_second=10, time_window=1.0):
        self.max_requests = max_requests_per_second
        self.time_window = time_window
        self.requests = defaultdict(list)
        self.lock = Lock()
    
    def is_allowed(self, client_ip):
        current_time = time.time()
        with self.lock:
            if client_ip not in self.requests:
                self.requests[client_ip] = [current_time]
                return True
            
            self.requests[client_ip] = [
                t for t in self.requests[client_ip] 
                if current_time - t < self.time_window
            ]
            
            if len(self.requests[client_ip]) < self.max_requests:
                self.requests[client_ip].append(current_time)
                return True
            
            return False


def UDPMessaging(udp_ip, udp_port):
    '''
    Create a UDP socket that listens on the IP and port provided for DNS requests.
    Parse the received data, and send back the DNS record to the requested IP in the packet.
    '''

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((udp_ip, udp_port))
    
    rate_limiter = RateLimiter(max_requests_per_second=10, time_window=1.0)
    
    while True:
        data, addr = sock.recvfrom(1024)
        if not data:
            break
        
        client_ip = addr[0]
        
        if not rate_limiter.is_allowed(client_ip):
            continue
        
        (requestIP, nameToResolve) = parseUDPpacket(data)
        record = resolveName(nameToResolve)
        sendResponse(requestIP, record)