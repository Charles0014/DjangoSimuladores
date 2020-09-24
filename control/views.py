# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.contrib import messages
from subprocess import Popen, PIPE
import subprocess
import os 
 
PATH = os.path.abspath(os.getcwd())

PATH_ = '{}/scripts'.format(PATH) 

EMULADORES = {}

class Emulador:
    def __init__(self, filename, path, port, pid, status):
        self.filename = filename
        self.path = path 
        self.port = port
        self.pid = pid
        self.status = status        

emulators_file = open("{}/ports.txt".format(PATH_), "r")
emulators = emulators_file.readlines()
emulators_file.close()

for line in emulators:
    emul = line.rstrip().split(';')
    EMULADORES[emul[0]] = Emulador(filename=emul[2],
                                       path=emul[2],
                                       port=emul[1],
                                       pid="",
                                       status="Stoped")
                                                                          
def run(command):
    process = Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    JOB_PID = process.pid
    return JOB_PID

def start(key):
    path = os.path.join(PATH_, EMULADORES[key].path, EMULADORES[key].filename)
    command = "python2 {}.pyw".format(path)
    process_id = verify_process(EMULADORES[key].port)
    if process_id != 0:
        EMULADORES[key].status = "Running"
        EMULADORES[key].pid = process_id
    else:
        run(command)
        updateStatus()
        process_id = verify_process(EMULADORES[key].port)
        if process_id != 0:
            updateStatus()
        else:
            EMULADORES[key].status = "Error"
            EMULADORES[key].pid = ""
   

def verify_process(porta):
    try:
        return subprocess.check_output(["lsof", "-t", "-i:{}".format(porta)])
    except:
        return 0

def stop(key):
    emulator = EMULADORES[key]
    process_id = verify_process(emulator.port)
    if process_id != 0:
        command = "kill -9 $(ps aux | grep python2 | grep {}.pyw | grep -v 'bin/sh' | awk '{{print $2}}')".format(key)
        try:
            run(command)
            updateStatus()
        except:
            print("error")
    emulator.status = "Stoped"
    EMULADORES[key] = emulator

def restart(key):
    stop(key)
    start(key)
    
def updateStatus():
    for key, emulator in EMULADORES.items():
        process_id = verify_process(emulator.port)
        if process_id > 0:
            emulator.status = "Running"
            emulator.pid = process_id
        else:
            emulator.status = "Stoped"
            emulator.pid = ""     
    
def render_page(request): 
    return render(request, 'control/control_send.html', {
        "e":EMULADORES,
    }, content_type='text/html')
        
def control_send(request):
    if request.method in ("POST",):
        input_keys = [key for key in request.POST.keys() if key.startswith('control_send_')]
        action = input_keys[0].split('_')[2]
        key = input_keys[0].split("_")[3]
        if action == "start":
            start(key)
        elif action == "stop":
            stop(key)
        else:
            restart(key)
        return render_page(request)
    updateStatus()
    return render_page(request)
