import socket
import zmq
import base64
import cv2

class PiZMQMessager:
    
    def __init__(self):
        self.context = zmq.Context()
        self.stream_socket = self.context.socket(zmq.REP)
        self.sound_socket = self.context.socket(zmq.REP)
        self.connection_socket = self.context.socket(zmq.PUB)
        self.stream_socket.bind("tcp://*:5555")
        self.sound_socket.bind("tcp://*:5556")
        self.connection_socket.bind("tcp://*:5557")
        self.video = cv2.VideoCapture("rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov")
        while True:
            try:
                sound_message = self.sound_socket.recv(zmq.NOBLOCK)
                self.sound_socket.send_string("the pi got the file!")
                self.audio(sound_message)
            except:
                pass
            self.connection_socket.send_string("c")    
            stream_message = self.stream_socket.recv_string()
            grabbed, frame = self.video.read()
            encoded, buffer = cv2.imencode(".jpg", frame)
            frame = base64.b64encode(buffer)
            self.stream_socket.send(frame)

    def audio(self, sound):
        wav = base64.b64decode(sound)
        file = open("/home/pi/Desktop/test.wav","wb")
        file.write(wav)
        file.close()
        

test = PiZMQMessager()
