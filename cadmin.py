import os
import sys
from datetime import datetime
import subprocess
import yaml
import re
import argparse
from dataclasses import dataclass, fields
import threading
import json
from fabric import Connection
import time
from invoke import UnexpectedExit
import invoke.exceptions


@dataclass
class Cluster:
    
    TVOCCONC : str = "../commands/Total_Volatile_Organic_Compounds_Concentration_Measurement.txt"
    NDOCONC : str = "../commands/Nitrogen_Dioxide_Concentration_Measurement.txt"
    CC : str = "../commands/Color_Control.txt"
    LUNIT : str = "../commands/Unit_localization.txt"
    FLDCONC : str = "../commands/Formaldehyde_Concentration_Measurement.txt"
    SWTCH : str = "../commands/Switch.txt"
    BRBINFO : str = "../commands/Bridged_Device_Basic_Information.txt"
    BIND : str = "../commands/Binding.txt"
    ULABEL : str = "../commands/User_Lable.txt"
    PMICONC : str = "../commands/PM2.5_Concentration_Measurement.txt"
    SMOKECO : str = "../commands/Smoke_and_CO_Alarm.txt"
    DISHM : str = "../commands/Dishwasher_Mode_Cluster.txt"
    FLABEL : str = "../commands/Fixed_Lable.txt"
    DRLK : str = "../commands/Door_lock.txt"
    ACFREMON : str = "../commands/Activated_Carbon_Filter_Monitoring.txt"
    TSTAT : str = "../commands/Thermostat.txt"
    DESC : str = "../commands/Descriptor_Cluster.txt"
    MC : str = "../commands/Media.txt"
    CDOCONC : str = "../commands/Carbon_Dioxide_Concentration_Measurement.txt"
    PSCFG : str = "../commands/Power_Source_Configuration.txt"
    DGETH : str = "../commands/Ethernet_Diag.txt"
    DGSW : str = "../commands/Software_Diag.txt"
    HEPAFREMON : str = "../commands/HEPA_Filter_Monitoring.txt"
    RVCCLEANM : str = "../commands/RVC_Clean_Mode.txt"
    PRS : str = "../commands/Pressure_measurement.txt"
    I : str = "../commands/Identify.txt"
    DGTHREAD : str = "../commands/Thread_diag.txt"
    BOOL : str = "../commands/Boolean.txt"
    TSUIC : str = "../commands/Thermostat_User.txt"
    LCFG : str = "../commands/Localization_Configuration_cluster.txt"
    WNCV : str = "../commands/Window_Covering.txt"
    BINFO : str = "../commands/Basic_Information.txt"
    OCC : str = "../commands/OccupancySensing.txt"
    DGWIFI : str = "../commands/Wifi_Diag.txt"
    GRPKEY : str = "../commands/Group_Communication.txt"
    RH : str = "../commands/Relative_Humidity_Measurement_Cluster.txt"
    PS : str = "../commands/Power_Source_Cluster.txt"
    LTIME : str = "../commands/Time_Format_localization.txt"
    G : str = "../commands/Groups.txt"
    LWM : str = "../commands/Laundry_Washer_Mode.txt"
    PMHCONC : str = "../commands/PM1_Concentration_Measurement.txt"
    PCC : str = "../commands/pump_configuration.txt"
    ACL : str = "../commands/Access_Control.txt"
    RVCRUNM : str = "../commands/RVC_Run_Mode.txt"
    RNCONC : str = "../commands/Radon_Concentration_Measurement.txt"
    FLW : str = "../commands/Flow_Measurement_Cluster.txt"
    MOD : str = "../commands/Mode_Select.txt"
    LVL : str = "../commands/Level_Control.txt"
    AIRQUAL : str = "../commands/Air_Quality.txt"
    PMKCONC : str = "../commands/PM10_Concentration_Measurement.txt"
    TMP : str = "../commands/Temperature_Measurement_Cluster.txt"
    OZCONC : str = "../commands/Ozone_Concentration_Measurement.txt"
    FAN : str = "../commands/Fan_Control.txt"
    OO : str = "../commands/OnOff.txt"
    CMOCONC : str = "../commands/Carbon_Monoxide_Concentration_Measurement.txt"
    TCCM : str = "../commands/Refrigerator_And_Temperature_Controlled_Cabinet_Mode.txt"
    DGGEN: str = "../commands/Gendiag.txt"
    ILL : str = "../commands/Illuminance_Measurement_Cluster.txt"
    CADMIN : str = "../commands/cadmin.txt"

clusters = fields(Cluster)


cluster_name = [field.name for field in clusters]

parser = argparse.ArgumentParser(description='cluster name')

parser.add_argument('-c','--cluster', nargs='+',help='name of the cluster',choices= cluster_name)
parser.add_argument('-p','--pairing',help='Auto-pairing function', default= False)

args = parser.parse_args()



pattern1 = re.compile(r'(CHIP:DMG|CHIP:TOO)(.*)')
pattern2 = re.compile(r'^\./chip-tool')
pattern3 = re.compile(r'avahi-browse')
t = ""
# chip-tool path
homedir = os.path.join(os.path.expanduser('~'), "chip_command_run", "config.yaml")
with open(homedir, 'r') as file:
    yaml_info = yaml.safe_load(file)
    build = yaml_info["chip_tool_directory"]

# Folder Path
path = os.path.join(os.getcwd(),"../commands")

# Change the directory
os.chdir(path)

def factory_reset( data ):

        ssh = Connection(host= data["host"], user=data["username"], connect_kwargs={"password": data["password"]})


        # Executing the  'ps aux | grep process_name' command to find the PID value to kill
        command = f"ps aux | grep {data['command']}"
        pid_val = ssh.run(command, hide=True)

        pid_output = pid_val.stdout
        pid_lines = pid_output.split('\n')
        for line in pid_lines:
            if data["command"] in line:
                pid = line.split()[1]
                conformance = line.split()[7]
                if conformance == 'Ssl':
                    kill_command = f"kill -9 {pid}"
                    ssh.run(kill_command)


        ssh.close()


def advertise():
        
        cd = os.getcwd()
        rpi_path = os.path.join(cd,"../scripts/rpi.json") 

        with open( rpi_path, "r") as f:
            data = json.load(f)


        ssh = Connection(host= data["host"], user=data["username"], connect_kwargs={"password": data["password"]})

        path = data["path"]
        ssh.run('rm -rf /tmp/chip_*')

        try:
            log = ssh.run('cd ' + path + ' && ' + data["command"], warn=True, hide=True, pty=False)
        except UnexpectedExit as e:
            if e.result.exited == -1:
                None
            else:
                raise

        #self.start_logging(log)
        ssh.close()
        logpath = os.path.join(cd,"../Logs/BackendLogs") 
        date = datetime.now().strftime("%m_%Y_%d-%I:%M:%S_%p")
        with open(f"{logpath}/{t}dut-{date}.txt", 'a') as c:
            c.write(log.stdout)
        return True

def tc(tc):
    global t
    t = tc
    return None


# Fn to process log files and save them
def process_log_files(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for filename in os.listdir(input_dir):
        if filename.endswith('.txt'):
            input_file_path = os.path.join(input_dir, filename)
            output_file_path = os.path.join(output_dir, filename)
            avahi = False

            with open(input_file_path, 'r') as input_file, open(output_file_path, 'w') as output_file:
                for line in input_file:
                    line = line.strip()
                    match1 = pattern1.search(line)
                    match2 = pattern2.search(line)
                    match3 = pattern3.search(line)
                    if match1:
                        chip_text = match1.group(1).strip()
                        trailing_text = match1.group(2).strip()
                        output_line = f"{chip_text} {trailing_text}"
                        output_file.write(output_line + '\n')
                    elif match2:
                        output_file.write('\n' 'CHIP:CMD : ' + line + '\n\n')
                        avahi = False
                    elif match3:
                        output_file.write('\n' 'CHIP:CMD : ' + line + '\n')
                        avahi = True
                    elif avahi:
                        output_file.write( line + '\n')


def code():
    with open ("temp.txt", 'r') as f:
        for l in f:
            l = l.strip()
            match = re.search(r'Manual pairing code: \[(\d+)\]', l)
            if match:
                manualcode = match.group(1)
                return(str(manualcode))
            
    return False

    

# Fn to run chip commands in terminal
def run_command(commands, testcase):
    file_path = os.path.join(os.path.expanduser('~'), build)
    save_path = os.path.join(os.path.expanduser('~'), "chip_command_run", "Logs", "BackendLogs")
    tc(testcase)
    cd = os.getcwd()
    rpi_path = os.path.join(cd,"../scripts/rpi.json") 
    p = args.pairing
    date = datetime.now().strftime("%m_%Y_%d-%I:%M:%S_%p")
    manualcode = "34970112332"
    if p :
        with open( rpi_path, "r") as f:
            data = json.load(f)
        factory_reset(data)
        thread = threading.Thread(target= advertise)
        thread.daemon = True
        thread.start()
        time.sleep(5)
        os.chdir(file_path)
        rebootcmd = "rm -rf /tmp/chip_*"
        subprocess.run(rebootcmd, shell=True, text=True, stdout= subprocess.PIPE, stderr=subprocess.PIPE)
        pairing_cmd = "./chip-tool pairing onnetwork 1 20202021"
        subprocess.run(pairing_cmd, shell=True, text=True, stdout= subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        os.chdir(file_path)

    while "" in commands:
        commands.remove("")
    for i in commands:
        with open(f"{save_path}/{testcase}-{date}.txt", 'a') as cluster_textfile:
            print(testcase, i)
        # subprocess module is used to open, append logs and run command in the terminal
            if "open-commissioning-window" in i:
                cluster_textfile.write('\n' + '\n' + i + '\n' + '\n')

            if "open-basic-commissioning-window" in i:
                manualcode = "34970112332"

            elif "{code}" in i:
                i = i.replace("{code}", manualcode)
                cluster_textfile.write('\n' + '\n' + i + '\n' + '\n')

            else:
                cluster_textfile.write('\n' + '\n' + i + '\n' + '\n')

        run = subprocess.run(i, shell=True, text=True, stdout= subprocess.PIPE, stderr=subprocess.PIPE)

        log = run.stdout
                
        with open("temp.txt", 'w') as f:
                    f.write(log)
        if "open-commissioning-window" in i:
            cod = code()
            if cod == False:
                None
            else:
                manualcode = cod

        with open(f"{save_path}/{testcase}-{date}.txt", 'a') as cluster_textfile:
            cluster_textfile.write(log)

    if p :
        factory_reset(data)
        time.sleep(5)
    
    # Process the log file immediately after running the commands
    input_directory = os.path.join(os.path.expanduser('~'), "chip_command_run", "Logs", "BackendLogs")
    output_directory = os.path.join(os.path.expanduser('~'), "chip_command_run", "Logs", "ExecutionLogs")
    process_log_files(input_directory, output_directory)
    os.chdir(cd)
    print(f"---------------------{testcase} - Executed----------------------")


# Read text File
def read_text_file(file_path):
    testsite_array = []
    filterCommand = []
    with open(file_path, 'r') as f:
        for line in f:
            testsite_array.append(line)
        filter_command = filter_commands(testsite_array)
        for command in filter_command:
            for com in command:
                # Separate testcase name from the array of commands
                if "#" in com:
                    testcase = com.split()[1]
                else:
                    filterCommand.append(com)
            run_command(filterCommand, testcase)
            filterCommand = []



# Fn to filter only commands from txt file
def filter_commands(commands):
    newcommand = []
    for command in commands:
        if "\n" in command:
            command = command.replace("\n", "")
        if "$" not in command:
            newcommand.append(command)
    size = len(newcommand)
    # Remove all the "end" in the array
    idx_list = [idx + 1 for idx, val in
                enumerate(newcommand) if val.lower() == "end"]
    res = [newcommand[i: j] for i, j in
           zip([0] + idx_list, idx_list +
               ([size] if idx_list[-1] != size else []))]
    newRes = []
    for i in res:
        i.pop()
        newRes.append(i)
    return newRes

def all():
# iterate through all files
    for file in os.listdir():
    # Check whether the file is in text format or not
        if file.endswith(".txt"):
            file_path = os.path.join(os.path.expanduser('~'), "chip_command_run", "commands", file)  # Chip tool commands txt directory
            # call read text file function
            read_text_file(file_path)

if __name__ == "__main__":
    
    test = args.cluster
    
    if test:
        for c in test:
             file = vars(Cluster)[c]
             file_path = os.path.join(os.path.expanduser('~'), "chip_command_run", "commands",
                                file )
             read_text_file(file_path)
    else:
        all()
