import socket
import ipaddress


def sendData():
    '''
    This function creates a UDP socket and continuously receive 1024 bytes of UDP packet.
    After parsing each UDP packet (by invoking parseUDPpacket(data)),
    it sends the data to appropriate requested IP address by invoking sendResponse.
    '''

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    while True:
        data, addr = sock.recvfrom(1024)
        if not data:
            break
        (requestIP, record) = parseUDPpacket(data)
        
        # Validate destination IP address
        if not isValidDestination(requestIP, addr):
            continue
            
        sendResponse(requestIP, record)


def isValidDestination(requestIP, sourceAddr):
    '''
    Validates the destination IP address to prevent spoofing and SSRF attacks.
    Checks that the destination is not a private, loopback, or reserved address
    and matches the actual source of the packet.
    '''
    try:
        ip = ipaddress.ip_address(requestIP)
        sourceIP = ipaddress.ip_address(sourceAddr[0])
        
        # Block private, loopback, multicast, and reserved addresses
        if ip.is_private or ip.is_loopback or ip.is_multicast or ip.is_reserved:
            return False
        
        # Verify the requested IP matches the actual source address
        if ip != sourceIP:
            return False
            
        return True
    except (ValueError, TypeError):
        return False