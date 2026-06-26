import socket
import os

PORT = 5005

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", PORT))

print("📡 Phone Monitor Running...")

while True:
    data, addr = sock.recvfrom(1024)
    message = data.decode()

    print("\n🚨 PATIENT ALERT 🚨")
    print(message)

    # alarm sound
    os.system("termux-vibrate -d 1000")