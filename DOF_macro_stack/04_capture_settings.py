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


print()
print("Enter motion parameters.")
print("Press ENTER if value should not be changed.")
print("Preset points: 1 - start motion, 2 - end motion")
print()


print()
print("** Keyponts from manual jogging")
print("** Start:", config["actuator"]["keypoints"][0], "mm")
print("** End:", config["actuator"]["keypoints"][1], "mm")
print("** Distance to go:", (config["actuator"]["keypoints"][0] - config["actuator"]["keypoints"][1]), "mm")
config["motion"]["steps"] =                           float(ask("Steps", config["motion"]["steps"]))
print("** Step size:", (config["actuator"]["keypoints"][1] - config["actuator"]["keypoints"][0]) / config["motion"]["steps"], "mm")

print()
config["motion"]["rapid_drive_speed"] =               float(ask("Rapid movement speed", config["motion"]["rapid_drive_speed"]))
config["motion"]["drive_speed"] =                     float(ask("Normal movement speed", config["motion"]["drive_speed"]))

print()
config["shutter"]["pre_shutter_wait"] =               float(ask("Pre shutter wait time", config["shutter"]["pre_shutter_wait"]))
config["shutter"]["focus_wait_time"] =                float(ask("Focus wait time", config["shutter"]["focus_wait_time"]))
config["shutter"]["frames_to_capture_per_step"] =     float(ask("Frames to capture", config["shutter"]["frames_to_capture_per_step"]))
config["shutter"]["shutter_press_time"] =             float(ask("Shutter hold time", config["shutter"]["shutter_press_time"]))
config["shutter"]["post_shutter_wait_time"] =         float(ask("Post shutter hold time", config["shutter"]["post_shutter_wait_time"]))
config["shutter"]["use_focus"] =                      str2bool(ask("Use focus", str(config["shutter"]["use_focus"])))



g_code = []





config["generated_gcode"] = g_code

with open(config_file_name, 'w') as file:
    yaml.dump(config, file, sort_keys=False)



