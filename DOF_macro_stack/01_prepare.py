import yaml

def ask(question, value):
    temp = input("> "+ question + " [" + str(value) + "]: ")
    if temp == "" or temp == None:
        return value
    return temp


config_file_name = 'config.yaml'

with open(config_file_name) as file:
    config = yaml.load(file, Loader=yaml.FullLoader)


print("")
print("Enter hardware parameters.")
print("Press ENTER if value should not be changed.")
print("")

config["hadrware"]["comport"] =                     str(ask("Controller COM port", config["hadrware"]["comport"]))
config["actuator"]["axis"] =                        str(ask("Axis to be used", config["actuator"]["axis"]))

config["actuator"]["acceleration"] =                float(ask("Motion acceleration (mm/sec^2)", config["actuator"]["acceleration"]))
config["actuator"]["steps_per_mm"] =                float(ask("Motion (steps per mm)", config["actuator"]["steps_per_mm"]))
config["actuator"]["max_speed"] =                   float(ask("Max speed", config["actuator"]["max_speed"]))

config["power"]["motor_drive_power"] =              int(ask("Actuator drive current (1-32)", config["power"]["motor_drive_power"]))
config["power"]["motor_idle_power"] =               int(ask("Actuator idle current (1-32)", config["power"]["motor_idle_power"]))

config["motion"]["rapid_drive_speed"] =             float(ask("Rapid movement speed (mm/min)", config["motion"]["rapid_drive_speed"]))


with open(config_file_name, 'w') as file:
    yaml.dump(config, file, sort_keys=False)
