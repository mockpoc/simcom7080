from threading import Thread, Event
import time 
import logging as log
import re
import serial

class SerialThread(Thread) :
    """Parsing des infos recues par le module"""
    def __init__(self, COM="COM10", baudRate=115200) :
        Thread.__init__(self)
        self.shouldExit = False
        self.buffer = bytearray()
        try :
            self.ser = serial.Serial(COM, baudRate, timeout = 0.1, write_timeout = 0.1)
        except :
            log.error("Port open error")
            exit(-1)

        try : 
            self.fp = open("rx_dump.txt", "wb")
        except Exception as e : 
            print(e)
            exit(-1)

    def run(self) :
        while(False == self.shouldExit) :
            try :
                data = self.ser.read(1)
            except Exception as e :
                print("error : ", e)
                continue
            else :
                if len(data) > 0 :
                    self.fp.write(data)
                    self.buffer += data
        print("serialThread stopped")

    def stop(self) : 
        self.shouldExit = True
        self.ser.close()
        print("stopping serialThread ...")

    def send_command(self, command) :
        toSend = bytearray(command + "\r\n", encoding="utf-8")
        print("sending : {}".format(toSend))
        try : 
            self.ser.write(toSend)
        except TypeError :
            pass
