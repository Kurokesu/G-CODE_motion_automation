import yaml

def ask(question, value):
    temp = input("> "+ question + " [" + str(value) + "]: ")
    if temp == "" or temp == None:
        return value
    return temp

def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")
        

config_file_name = 'config.yaml'

with open(config_file_name) as file:
    config = yaml.load(file, Loader=yaml.FullLoader)


print("")
print("Enter hardware parameters.")
print("Press ENTER if value should not be changed.")
print("")

config["hadrware"]["comport"] =                     str(ask("Controller COM port", config["hadrware"]["comport"]))
config["actuator"]["axis"] =                        str(ask("Axis to be used", config["actuator"]["axis"]))

print()
config["actuator"]["acceleration"] =                float(ask("Motion acceleration (mm/sec^2)", config["actuator"]["acceleration"]))
config["actuator"]["steps_per_mm"] =                float(ask("Motion (steps per mm)", config["actuator"]["steps_per_mm"]))
config["actuator"]["max_speed"] =                   float(ask("Max speed", config["actuator"]["max_speed"]))

print()
config["power"]["motor_drive_power"] =              int(ask("Actuator drive current (1-32)", config["power"]["motor_drive_power"]))
config["power"]["motor_idle_power"] =               int(ask("Actuator idle current (1-32)", config["power"]["motor_idle_power"]))

print()
config["shutter"]["pre_shutter_wait"] =               float(ask("Pre shutter wait time", config["shutter"]["pre_shutter_wait"]))
config["shutter"]["frames_to_capture_per_step"] =     int(ask("Frames to capture", config["shutter"]["frames_to_capture_per_step"]))
config["shutter"]["shutter_press_time"] =             float(ask("Shutter hold time", config["shutter"]["shutter_press_time"]))
config["shutter"]["post_shutter_wait_time"] =         float(ask("Post shutter hold time", config["shutter"]["post_shutter_wait_time"]))
#config["shutter"]["focus_wait_time"] =                float(ask("Focus wait time", config["shutter"]["focus_wait_time"]))
#config["shutter"]["use_focus"] =                      str2bool(ask("Use focus", str(config["shutter"]["use_focus"])))

print()
config["motion"]["rapid_drive_speed"] =               float(ask("Rapid movement speed while taking pictures", config["motion"]["rapid_drive_speed"]))
config["motion"]["drive_speed"] =                     float(ask("Normal movement speed while taking pictures", config["motion"]["drive_speed"]))


with open(config_file_name, 'w') as file:
    yaml.dump(config, file, sort_keys=False)
