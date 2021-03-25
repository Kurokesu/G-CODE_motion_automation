import yaml

def ask(question, value):
    temp = input("> "+ question + " [" + str(value) + "]: ")
    if temp == "" or temp == None:
        return value
    return temp

def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")

generator_version = "0.1.0" 
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
print("** Start:", config["motion"]["keypoints"][0], "mm")
print("** End:", config["motion"]["keypoints"][1], "mm")
print("** Distance to go:", (config["motion"]["keypoints"][1] - config["motion"]["keypoints"][0]), "mm")
config["motion"]["steps"] =                           float(ask("Steps", config["motion"]["steps"]))
step_distance = (config["motion"]["keypoints"][1] - config["motion"]["keypoints"][0]) / config["motion"]["steps"]
print("** Step size:", step_distance, "mm")




gcode = []


gcode.append("; Generator version " + str(generator_version))
gcode.append("; Set absolute movement mode")
gcode.append("G90")
gcode.append("")

gcode.append("; Move to start position") 
gcode.append("G1 "+config["actuator"]["axis"]+str(config["motion"]["keypoints"][0])+" F"+str(config["motion"]["rapid_drive_speed"])) 

gcode.append("")
gcode.append("; Set relative movement mode")
gcode.append("G91")
gcode.append("")


for step in range(int(config["motion"]["steps"])):

    gcode.append("")
    gcode.append("; ----------- NEW STEP ---------------")
    if step > 0:
        gcode.append("; Moving by " + str(step_distance)+"mm")
        gcode.append("G1 " + config["actuator"]["axis"] + str(step_distance) + " F"+str(config["motion"]["drive_speed"])) 

    for i in range(int(config["shutter"]["frames_to_capture_per_step"])):
        gcode.append("; Wait till platform is stable")
        gcode.append("G4 P" + str(config["shutter"]["pre_shutter_wait"]))
        gcode.append("; Trigger shutter")
        gcode.append("M8")
        gcode.append("; Capturing...")
        gcode.append("G4 P" + str(config["shutter"]["shutter_press_time"]))
        gcode.append("; Retract shutter")
        gcode.append("M9")
        gcode.append("; Wait post trigger")
        gcode.append("G4 P" + str(config["shutter"]["post_shutter_wait_time"]))


gcode.append("") 
if config["motion"]["return_home_after_complete"]:
    gcode.append("; Set absolute movement mode")
    gcode.append("G90")
    gcode.append("; Move to start position") 
    gcode.append("G1 "+config["actuator"]["axis"]+str(config["motion"]["keypoints"][0])+" F"+str(config["motion"]["rapid_drive_speed"])) 

config["generated_gcode"] = gcode

with open(config_file_name, 'w') as file:
    yaml.dump(config, file, sort_keys=False)
