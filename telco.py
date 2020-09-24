import logging as log
from serialThread import RxThread, TxThread
import time
import serial

ser = 0
def config() :
    global ser
    log.basicConfig(filename='telco.log', format='%(asctime)s-%(levelname)s:%(message)s', filemode='w', level=log.DEBUG, datefmt='%m/%d/%Y %H:%M:%S')
    log.getLogger().addHandler(log.StreamHandler())

    try :
        ser = serial.Serial('COM10', 115200, timeout = 0.1, write_timeout = 10)  # open serial port
    except :
        log.error("Port open error")
        exit(-1)

def connexion(tx, rx) : 
    tx.send_command("AT")
    if -1 == rx.wait_ok(["OK"], 3) :
        log.warning("AT ERROR")
    else :
        log.warning("MODULE READY")

    tx.send_command("AT+CPIN?")
    if -1 == rx.wait_ok(["READY"], 3) :
        log.warning("SIM ERROR")
    else : 
        log.warning("SIM READY")

    tx.send_command("AT+CSQ")
    resp = rx.wait_ok(["CSQ: \d\d,\d\d"], 3)
    if -1 == resp:
        log.warning("CSQ cde Error")
    else :
        resp = resp.split(" ")
        resp = resp[1].split(",")
        if int(resp[0]) != 99 :
            log.debug("NETWORK READY")
        else :
            log.warning("network signal error")

    tx.send_command("AT+CGATT?")
    if -1 == rx.wait_ok(["CGATT: 1"], 3) :
        log.warning("network not attached")
    else :
        log.debug("NETWORK ATTACHED")

    tx.send_command("AT+COPS?")
    resp = rx.wait_ok(["COPS:.*\".*\""], 3)
    if -1 == resp :
        log.warning("network info error")
    else :
        log.debug("network info : {}".format(resp.split("\"")[1]))

    tx.send_command("AT+CGNAPN")
    resp = rx.wait_ok(["CGNAPN:.*\".*\""], 3)
    if -1 == resp :
        log.warning("network info error")
    else :
        log.debug("apn info : {}".format(resp.split("\"")[1]))

    tx.send_command("AT+CNACT", ["0", "1"])
    resp = rx.wait_ok(["ACTIVE", "ERROR"], 3)
    if -1 == resp :
        log.warning("network activation error")
    else :
        print(resp)

    tx.send_command("AT+CNACT?")
    resp = rx.wait_ok(["CNACT: 0,1,\".+\""], 3)
    if -1 == resp :
        log.warning("network activation error")
    else :
        print("IP : ", resp.split("\"")[1])
if __name__ == "__main__" :
    config()

    log.debug("starting ...")

    rx = RxThread(ser)
    tx = TxThread(ser)
    rx.start()
    tx.start()

    connexion(tx, rx)

    rx.stop()
    tx.stop()
    rx.join()
    tx.join()
    ser.close()