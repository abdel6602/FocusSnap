import socket
import os

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('', 8080))

image_size = os.path.getsize('test.jpg')
image_chunks = image_size // 2048
remaining_data = image_size % 2048

s.send(f'blur\n{image_chunks}\n{remaining_data}'.encode())
server_response = s.recv(1024).decode()
print('recieved:', server_response)

print('Image size:', image_size, 'bytes')
print('Number of 2048 chunks:', image_chunks)

if server_response == "ACK send picture":
    file = open('test.jpg', 'rb')
    image_chunk = file.read(2048)

    for i in range(image_chunks + 2):
        s.send(image_chunk)
        image_chunk = file.read(2048)
        print("recieved:", s.recv(1024).decode())

    s.send(image_chunk)
print('recieved:',s.recv(1024).decode())
s.close()



