import socket
import json
import control
import errno

def recieve_image(connection, chunks, overflow):
    file = open('test.jpg', 'wb')
    image_data = connection.recv(2048)
    for i in range(chunks + 2):
        try:
            file.write(image_data)
            connection.send("ACK chunk received".encode())
            image_data = connection.recv(2048)
        except socket.error as e:
            if e.errno == errno.EPIPE:
                break
            else:
                raise
    connection.recv(2048)
    print("Image received")
    connection.send("ACK image received, terminating".encode())



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 8080))
s.listen(5)

hello_message = {"message": "Hello, client!"}

while True:
    connection, address = s.accept()
    print('Connected with', address)

    try:
        request = connection.recv(1024).decode().split('\n')
        request_type = request[0]
        print(request_type)
        if request_type == "Hello":
            connection.send(json.dumps(hello_message).encode())
        
        elif request_type == "blur":
            chunks = int(request[1])
            overflow = int(request[2])
            # ask the client to send the picture
            connection.send("ACK send picture".encode()) 
            # receive the size of the image
            recieve_image(connection, chunks, overflow=overflow)
            control.service_blur("test.jpg")
            print("Applying Operation")

            connection.close()
        else:
            connection.send("Invalid request.".encode())
    except Exception as err:
        print(str(err))
    finally:
        connection.close()