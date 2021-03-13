import socket
import zmq
import base64
import cv2
import os

class PiZMQMessager:
    
    def __init__(self):
        self.context = zmq.Context()
        self.stream_socket = self.context.socket(zmq.REP)
        self.sound_socket = self.context.socket(zmq.REP)
        self.connection_socket = self.context.socket(zmq.PUB)
        self.stream_socket.bind("tcp://*:5555")
        self.sound_socket.bind("tcp://*:5556")
        self.connection_socket.bind("tcp://*:5557")
        self.video = cv2.VideoCapture("/home/pi/Desktop/sample.avi")
        while True:
            self.saveAudio()
            self.sendConnectionStatus()
            self.sendStream()

    def saveAudio(self):
        try:
            sound = self.sound_socket.recv(zmq.NOBLOCK)
            url = '/home/pi/Desktop/sounds/mod.wav'
            self.sound_socket.send_string("the pi got the sound")
            wav = base64.b64decode(sound)
            file = open(url,"wb")
            file.write(wav)
            file.close()
            os.system('vlc %s vlc://quit &' % url)
            
        except:
            pass

    def sendConnectionStatus(self):
        self.connection_socket.send_string("c")

    def sendStream(self):
        stream_message = self.stream_socket.recv_string()
        grabbed, frame = self.video.read()
        encoded, buffer = cv2.imencode(".jpg", frame)
        frame = base64.b64encode(buffer)
        self.stream_socket.send(frame)

        
messager = PiZMQMessager()
