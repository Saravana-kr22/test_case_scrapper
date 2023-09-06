import subprocess
import os
from pathlib import Path

def file():
    path = Path(Path(__file__).parents[2])
    html_file = "chip-test-plans/build/html"
    #delete the old build
    
    cmd_del = "sudo rm -rf build"
    #subprocess.run(cmd_del , shell = True)
    
    file_path = os.path.join(path, html_file)
    build_path = os.path.join(path,"chip-test-plans")
    os.chdir(build_path)
    #copy the old html to desiginated dir
    cp_cmd = "cp -r " + build_path + "/build/html/ " + str(Path(__file__).parent.parent)

    #subprocess.run(cp_cmd , shell= True)
    
    #subprocess.run(cmd_del , shell = True)
    # Pull the latest changes
    pull_cmd = "git pull"
    #subprocess.run(pull_cmd, shell=True)
    # create new html file
    cmd_build = "sudo make html && sudo make html-clusters"
    #subprocess.run(cmd_build, shell=True)
    
    new_file = []
    for filename in os.listdir(file_path):
        html_path = os.path.join(file_path, filename)
        new_file.append(html_path)
    print(new_file)

    old_file = []
    old_path = str(Path(__file__).parent.parent) + "/build"
    for filename in os.listdir(old_path):
        html_path = os.path.join(old_path, filename)
        old_file.append(html_path)
    print (old_file)
    keys=['app', 'main']
    file_list = {}
    
    for i in range(len(keys)):
        file_list[keys[i]] = (new_file[i],old_file[i])


    os.chdir(Path(__file__).parent)

    print(file_list)

    return(file_list)
