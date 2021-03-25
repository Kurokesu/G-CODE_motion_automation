from pynput import keyboard
import yaml
import serial
import time


print("Manually adjust actuator")
print()
print("S - moves forward")
print("A - moves backwards")
print()
print("1-9 - set keypoint value")
print("SHIFT - makes motion slower")
print()
print("Q or ESC - exit tool")
print()


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


jog_steps = config["actuator"]["jog_length_rough"]

def on_press(key):
    global jog_steps

    try:
        #print('alphanumeric key {0} pressed'.format(key.char))

        # TODO: check buffer - do not send more commands if full, keep space for stop motion command
        if key.char == "s" or key.char == "S":            
            cmd = "$J=G91 "+config["actuator"]["axis"]+str(jog_steps)+" F"+str(config["actuator"]["jog_length_speed"])
            ser.write(bytes(cmd+'\n', 'utf8'))
            resp = ser.readline().decode("utf-8").strip()

        if key.char == "a" or key.char == "A":
            cmd = "$J=G91 "+config["actuator"]["axis"]+"-"+str(jog_steps)+" F"+str(config["actuator"]["jog_length_speed"])
            ser.write(bytes(cmd+'\n', 'utf8'))
            resp = ser.readline().decode("utf-8").strip()

        if key.char in ["1","2","3","4","5","6","7","8","9"]:
            cmd = "?"
            ser.write(bytes(cmd, 'utf8'))
            r1 = ser.readline().decode("utf-8").strip()
            text = r1[1:-1]
            feedback_split = text.split("|")
            positions = feedback_split[1].split(":")[1]
            positions = positions.split(",")
            axis = ["X", "Y", "Z", "A"].index(config["actuator"]["axis"])
            config["actuator"]["jog_position"] = float(positions[axis])

            kp_nr = int(key.char)-1
            config["actuator"]["keypoints"][kp_nr] = float(positions[axis])
            print("Keypoint", kp_nr, "=", config["actuator"]["keypoints"][kp_nr])

        if key.char == "q":
            return False


    except AttributeError:
        #print('special key {0} pressed'.format(key))

        if key == keyboard.Key.shift:
            jog_steps = config["actuator"]["jog_length_fine"]


def on_release(key):
    global jog_steps

    #print('{0} released'.format(key))

    cmd = b"\x85"
    ser.write(cmd)

    cmd = "?"
    ser.write(bytes(cmd, 'utf8'))
    r1 = ser.readline().decode("utf-8").strip()
    text = r1[1:-1]
    feedback_split = text.split("|")
    positions = feedback_split[1].split(":")[1]
    positions = positions.split(",")
    axis = ["X", "Y", "Z", "A"].index(config["actuator"]["axis"])
    config["actuator"]["jog_position"] = float(positions[axis])
    print(positions[axis], "mm")

    if key == keyboard.Key.shift:
        jog_steps = config["actuator"]["jog_length_rough"]

    if key == keyboard.Key.esc:
        # Stop listener
        return False

# Collect events until released
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

with open(config_file_name, 'w') as file:
    yaml.dump(config, file, sort_keys=False)
