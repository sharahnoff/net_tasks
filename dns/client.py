import socket

DESTINATION = "192.168.1.2" 
DNS_PORT = 53

requests = [
            b"\x75\xa3\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x02\x70\x75\x02"
                b"\x76\x6b\x03\x63\x6f\x6d\x00\x00\x01\x00\x01",
            b"\x96\xd9\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x06\x67\x6f"
                b"\x6c\x61\x6e\x67\x03\x6f\x72\x67\x00\x00\x01\x00\x01"]

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(2)
for req in requests:
    sock.sendto(req, (DESTINATION, DNS_PORT))