import socket

sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
# Get the old state of the SO_REUSEADDR option
old_state = sock.getsockopt(socket.SOL_SOCKET,
socket.SO_REUSEADDR )
print ("Old sock state: %s" %old_state)
sock.bind(('127.0.0.1', 100))
sock.listen(1)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
old_state = sock.getsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR)
print ("Old sock state: %s" %old_state)
