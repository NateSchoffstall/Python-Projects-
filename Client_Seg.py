import socket
import threading
import pyaudio

# Constants for audio settings
CHUNK = 2048
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 40000

# Receives audio data from the socket to play it
def rAudio(sock, stream):
    while True:
        try:
            data, addr = sock.recvfrom(CHUNK)
            stream.write(data)
        except Exception as e:
            print(f"Error receiving audio: {e}")

# Captures audio from the microphone and sends it to the server side
def sAudio(sock, stream):
    while True:
        try:
            data = stream.read(CHUNK)
            send_segments(sock, data, serverAddr)
        except Exception as e:
            print(f"Error sending audio: {e}")

# Makes and sends segments of data to server
def send_segments(sock, data, addr):
    segment_size = 1000  # segment size
    num_segments = (len(data) + segment_size - 1) // segment_size  # Calculating number of segments
    for i in range(num_segments):
        start = i * segment_size
        end = min((i + 1) * segment_size, len(data))
        segment = data[start:end]
        sock.sendto(segment, addr)

# Receives segments and reassembles them
def receive_segments(sock, stream):
    buffer = b''
    while True:
        try:
            segment, addr = sock.recvfrom(CHUNK)
            buffer += segment
            if len(buffer) >= CHUNK:
                stream.write(buffer[:CHUNK])
                buffer = buffer[CHUNK:]
        except Exception as e:
            print(f"Error receiving audio segment: {e}")

# Sets up PyAudio
audio = pyaudio.PyAudio()

# Setting up the specific format, channels, and I/O devices for pyaudio
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True, output=True,
                    frames_per_buffer=CHUNK, input_device_index=1, output_device_index=4)

# Sets up socket for client
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientSocket.bind(("10.103.11.217", 12346)) 

# Set the buffer size for the socket
clientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 80000)

# Sets target address for server
serverAddr = ("10.103.46.198", 12345)  # Server information

# Threading
rThread = threading.Thread(target=receive_segments, args=(clientSocket, stream))
rThread.start()

sThread = threading.Thread(target=sAudio, args=(clientSocket, stream))
sThread.start()
