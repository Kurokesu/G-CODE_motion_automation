import yaml
import time
from tqdm import tqdm
import serial

config_file_name = 'config.yaml'

def wait_idle(ser):
    while(True):
        ser.timeout = 0.2
        cmd = "?"

        ser.write(bytes(cmd, 'utf8'))
        r1 = ser.readline().decode("utf-8").strip()

        #self.__ser_send(ser, cmd, monitor=False)
        #r1 = self.__ser_read(ser, monitor=False)

        try:
            if r1[0] == "<":
                    # <Idle|MPos:0.000,0.000,0.000,0.000|Bf:35,254|FS:0,0|Pn:X>
                    text = r1[1:-1]
                    feedback_split = text.split("|")
                    positions = feedback_split[2].split(":")
                    positions = positions[1]
                    positions = positions.split(",")
                    buffers = int(positions[0])
                    status = feedback_split[0]

                    # GRBL command buffer = 0
                    if buffers >= 35:
                        if status == "Idle":
                            break
        except:
            pass


with open(config_file_name) as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

ser = serial.Serial()
ser.port = config["hadrware"]["comport"]
ser.baudrate = int(config["hadrware"]["baudrate"])
ser.timeout = int(config["hadrware"]["timeout"])

res = ser.open()
ser.flushInput()
ser.flushOutput()

#print("Sleeping 1s...")
#time.sleep(1)

for line in tqdm(config["generated_gcode"]):
    l = bytes(line.strip()+ '\n', 'utf8')
    ser.write(l)
    grbl_out = ser.readline()
