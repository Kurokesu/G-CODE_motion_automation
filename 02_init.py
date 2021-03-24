import yaml
import serial
import time


def ask(question, value):
    temp = input("> "+ question + " [" + str(value) + "]: ")
    if temp == "" or temp == None:
        return value
    return temp

def send_cfg(ser, address, value):
    cmd = "$"+address+"="+str(value)    
    ser.write(bytes(cmd+'\n', 'utf8'))
    resp = ser.readline().decode("utf-8").strip()
    print(" >", cmd, resp)
    if resp != "ok":
        raise ValueError('Send config returned: '+ str(resp))


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



config_file_name = 'config.yaml'

with open(config_file_name) as file:
    config = yaml.load(file, Loader=yaml.FullLoader)


ser = serial.Serial()
ser.port = config["hadrware"]["comport"]
ser.baudrate = int(config["hadrware"]["baudrate"])
ser.timeout = int(config["hadrware"]["timeout"])

res = ser.open()
ser.flushInput()
ser.flushOutput()



# unlock
cmd = "$X"
ser.write(bytes(cmd+'\n', 'utf8'))
resp = ser.readline().decode("utf-8").strip()
print(" >", cmd, resp)
ser.flushInput()
ser.flushOutput()


# read version
cmd = "$I"
ser.write(bytes(cmd+'\n', 'utf8'))
r1 = ser.readline().decode("utf-8").strip()
r2 = ser.readline().decode("utf-8").strip()
r3 = ser.readline().decode("utf-8").strip()
print("Controller version:", r1)


# send parameters
send_cfg(ser, '24', config["actuator"]["homing_feed"])
send_cfg(ser, '25', config["actuator"]["homing_seek"])
send_cfg(ser, '27', config["actuator"]["homing_pulloff"])

axis = ["X", "Y", "Z", "A"].index(config["actuator"]["axis"])

send_cfg(ser, str(100+axis), config["actuator"]["steps_per_mm"])
send_cfg(ser, str(120+axis), config["actuator"]["acceleration"])
send_cfg(ser, str(110+axis), config["actuator"]["max_speed"])


# send power
cmd = "G100 P"+str(axis)+" L144 N0 S0 F"+str(config["power"]["motor_drive_power"])+" R"+str(config["power"]["motor_idle_power"])
ser.write(bytes(cmd+'\n', 'utf8'))
resp = ser.readline().decode("utf-8").strip()
print(" >", cmd, resp)



# move fwd (in case it is stuck beyond home pos)
print("")
print("Moving fwd...")

cmd = "G91"
ser.write(bytes(cmd+'\n', 'utf8'))
resp = ser.readline().decode("utf-8").strip()
print(" >", cmd, resp)


# wait till stop
print("")
print("Waiting to stop...")
wait_idle(ser)


# home
print("")
print("Homing...")
ser.flushInput()
ser.flushOutput()
ser.timeout = 60
cmd = "$H"+config["actuator"]["axis"]
ser.write(bytes(cmd+'\n', 'utf8'))
resp = ser.readline().decode("utf-8").strip()
ser.timeout = int(config["hadrware"]["timeout"])
print(" >", cmd, resp)


# pull back
print("")
print("Moving back...")

# pull back
cmd = "G0 "+config["actuator"]["axis"]+str(config["actuator"]["pull_back"])
ser.write(bytes(cmd+'\n', 'utf8'))
resp = ser.readline().decode("utf-8").strip()
print(" >", cmd, resp)

# wait till stop
print("")
print("Waiting to stop...")
wait_idle(ser)

ser.timeout = int(config["hadrware"]["timeout"])
