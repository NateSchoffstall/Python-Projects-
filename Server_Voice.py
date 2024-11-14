import socket
import threading
import pyaudio

# Constants for audio settings
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 40000

# Function to receive audio data from the socket and play it
def rAudio(sock, stream):
    global clientAddr
    while True:
        data, addr = sock.recvfrom(CHUNK)
        if clientAddr is None:
            clientAddr = addr
        stream.write(data)  
# Function to capture audio from microphone and send it to the client
def sAudio(sock, stream):
    global clientAddr
    while True:
        try:
            if clientAddr is not None:
                data = stream.read(CHUNK)
                sock.sendto(data, clientAddr)
        except socket.error as se:
            print(f"socket error at audio transmission se ")
       
        except OSError as oe:
            print(f"eo error ")
        except Exception as e:
            print(f"e error lol")






# Set up PyAudio
audio = pyaudio.PyAudio()
# Set up PyAudio with microphone as input device
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True, output=True,
                    frames_per_buffer=CHUNK, input_device_index=1, output_device_index=3)


# Set up socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(("10.103.46.198", 12345)) #LH = 127.0.0.1    192.168.0.14
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF,100000)
#"127.0.0.1", 12345
#text setup: '10.103.11.217', 42069

clientAddr = None

# Threading
rThread = threading.Thread(target=rAudio, args=(server_socket, stream))
rThread.start()

send_thread = threading.Thread(target=sAudio, args=(server_socket, stream))
send_thread.start()
