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
    log.warning("====CONNECT===")
    send_command("AT", ["OK"], tx, rx, 3)
    send_command("AT", ["OK"], tx, rx, 3)
    send_command("AT", ["OK"], tx, rx, 3)
    send_command("AT+CPIN?", ["READY"], tx, rx, 3)
    send_command("AT+CSQ", ["CSQ: \d\d,\d\d"], tx, rx, 3)
    send_command("AT+COPS?", ["COPS:.*\".*\"", "OK"], tx, rx, 10)
    send_command("AT+CGNAPN", ["CGNAPN:.*\".*\""], tx, rx, 3)
    send_command("AT+CNACT", ["COPS:.*\".*\"", "ERROR"], tx, rx, 10, args=["0", "1"])
    send_command("AT+CNACT?", ["CNACT: 0,1,\".+\""], tx, rx, 10)

def send_command(command, expected, tx, rx, tmo_s, args=[], doFlush=True) :
    tx.send_command(command, args=args)
    response = rx.wait_ok(expected, tmo_s)
    if -1 ==  response :
        # log.warning("CDE {} args : {} ERROR : {}".format(command, args, response))
        buffer, resp = rx.get_rx_buffer()
        print("!!! DUMP BUFFER : {}".format(buffer))
        print("!!! DUMP RESPONSE: {}".format(resp))
    else :
        # log.warning("CDE {} args : {} OK : {}".format(command, args, response))
        log.warning("OK")
    if doFlush :
        rx.flush_rx()

def send_msg(tx, rx) :
    log.warning("====SENDING MSG===")
    send_command("AT+SHCONF", ["OK"], tx, rx, 3, args=["\"URL\"", "\"http://api.mockpoc.fr\""])
    send_command("AT+SHCONF", ["OK"], tx, rx, 3, args=["\"BODYLEN\"", "1024"])
    send_command("AT+SHCONF", ["OK"], tx, rx, 3, args=["\"HEADERLEN\"", "350"])
    send_command("AT+SHCONN", ["OK"], tx, rx, 3)
    send_command("AT+SHSTATE?", ["SHSTATE: \d", "OK"], tx, rx, 3)
    send_command("AT+SHCHEAD", ["OK"], tx, rx, 3)
    send_command("AT+SHAHEAD", ["OK"], tx, rx, 3, args=["\"Host\"","\"api.mockpoc.fr\""])
    send_command("AT+SHAHEAD", ["OK"], tx, rx, 3, args=["\"auth-token\"","\"...\""])
    send_command("AT+SHREQ", ["ERROR", "\+SHREQ: \"GET\",\d+,\d+"], tx, rx, 10, args=["\"/light/list\"","1"])
    send_command("AT+SHREAD", ["\+SHREAD: \d+", "ERROR"], tx, rx, 3, args=["0","13"], doFlush=False)
    time.sleep(3)
    buffer, resp = rx.get_rx_buffer()
    if "OK" in resp[1] :
        if "+SHREAD" in resp[3] :
            print("received : {}".format(resp[4]))
    send_command("AT+SHDISC", ["OK"], tx, rx, 3)
    
if __name__ == "__main__" :
    config()

    log.debug("starting ...")

    rx = RxThread(ser)
    tx = TxThread(ser)
    rx.start()
    tx.start()

    connexion(tx, rx)
    send_msg(tx, rx)
    rx.stop()
    tx.stop()
    rx.join()
    tx.join()
    ser.close()