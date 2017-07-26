#!/bin/python

import base64, os, sys
from sys import platform

def backup(dir, svs):
    dirname = dir + "/" + input("\n(backup directory name)> ")
    if os.path.exists(dirname):
        print("Directory already exists.")
        backup(dir, svs)
        exit()
    os.mkdir(dirname)
    for i in svs:
        with open(dir + "/" + i, "r") as infile, open(dirname + "/" + i, "w") as outfile:
            outfile.write(infile.read())
    print("Backed up.")

def switch(dir, svs):
    save = dir + "/" + input("(Which save? - full filename)> ")
    if not os.path.exists(save):
        print("Save was not found.")
        switch(dir, svs)
        exit()
    with open(save, "br+") as file:
        stats = base64.b64decode(file.read())
        if b"\"CH\": 1" in stats:
            stats = stats.replace(b"\"CH\": 1", b"\"CH\": 0")
            print("Switched to Default Drifter.")
        if b"\"CH\": 0" in stats:
            stats = stats.replace(b"\"CH\": 0", b"\"CH\": 1")
            print("Switched to Alt Drifter.")
        file.seek(0)
        file.truncate()
        file.write(base64.b64encode(stats))

if platform == "linux" or platform == "linux2":
    gamedir = os.path.expanduser("~/.config/HyperLightDrifter")
elif platform == "darwin":
    gamedir = os.path.expanduser("~/Library/Application\ Support/com.HeartMachine.HyperLightDrifter")
elif platform == "win32":
    gamedir = os.path.expanduser("~/AppData/Local/HyperLightDrifter")

if platform != "darwin":
    if not os.path.exists(gamedir):
        print("Could not find game directory.")
        exit()

files = os.listdir(gamedir)
saves = []
for i in files:
    if "Record" in i:
        saves.append(i)

print("\nSaves: ")
for i in saves:
    char = ""
    with open(gamedir + "/" + i, "r") as infile:
        dat = infile.read()
        dat = base64.b64decode(dat)
        if b"\"CH\": 1" in dat:
            char = "Alt Drifter"
        else:
            char = "Default Drifter"
    print(i + " // " + char)

print("\n1. Backup\n2. Switch Character\n3. Exit")
chosen = False
while not chosen:
    choice = input("> ")
    if choice == "1":
        backup(gamedir, saves)
        chosen = True
    elif choice == "2":
        switch(gamedir, saves)
        chosen = True
    elif choice == "3":
        chosen = True
