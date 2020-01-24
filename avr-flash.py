#!/bin/python3
import argparse
import subprocess
import os
import sys
import base64

def printinfo(msg):
    print("\033[1m\33[33m[!] "+msg+"\033[0m")

def printsuccess(msg):
    print("\033[1m\33[34m[+]"+msg+"\033[0m")

def printfailure(msg):
    print("\033[1m\33[31m[-] "+msg+"\033[0m")

banner=b"ICAgICAgICAgICAgIOKWiOKWiOKWiOKWiOKWiOKVlyDilojilojilZcgICDilojilojilZfilojilojilojilojilojilojilZcgICAgICAgICAgICAgICDilojilojilojilojilojilojilojilZfilojilojilZcgICAgICDilojilojilojilojilojilZcg4paI4paI4paI4paI4paI4paI4paI4pWX4paI4paI4pWXICDilojilojilZcKICAgICAgICAgICAg4paI4paI4pWU4pWQ4pWQ4paI4paI4pWX4paI4paI4pWRICAg4paI4paI4pWR4paI4paI4pWU4pWQ4pWQ4paI4paI4pWXICAgICAgICAgICAgICDilojilojilZTilZDilZDilZDilZDilZ3ilojilojilZEgICAgIOKWiOKWiOKVlOKVkOKVkOKWiOKWiOKVl+KWiOKWiOKVlOKVkOKVkOKVkOKVkOKVneKWiOKWiOKVkSAg4paI4paI4pWRCiAgICAgICAgICAgIOKWiOKWiOKWiOKWiOKWiOKWiOKWiOKVkeKWiOKWiOKVkSAgIOKWiOKWiOKVkeKWiOKWiOKWiOKWiOKWiOKWiOKVlOKVnSAgICDilojilojilojilojilojilZcgICAg4paI4paI4paI4paI4paI4pWXICDilojilojilZEgICAgIOKWiOKWiOKWiOKWiOKWiOKWiOKWiOKVkeKWiOKWiOKWiOKWiOKWiOKWiOKWiOKVl+KWiOKWiOKWiOKWiOKWiOKWiOKWiOKVkQogICAgICAgICAgICDilojilojilZTilZDilZDilojilojilZHilZrilojilojilZcg4paI4paI4pWU4pWd4paI4paI4pWU4pWQ4pWQ4paI4paI4pWXICAgIOKVmuKVkOKVkOKVkOKVkOKVnSAgICDilojilojilZTilZDilZDilZ0gIOKWiOKWiOKVkSAgICAg4paI4paI4pWU4pWQ4pWQ4paI4paI4pWR4pWa4pWQ4pWQ4pWQ4pWQ4paI4paI4pWR4paI4paI4pWU4pWQ4pWQ4paI4paI4pWRCiAgICAgICAgICAgIOKWiOKWiOKVkSAg4paI4paI4pWRIOKVmuKWiOKWiOKWiOKWiOKVlOKVnSDilojilojilZEgIOKWiOKWiOKVkSAgICAgICAgICAgICAg4paI4paI4pWRICAgICDilojilojilojilojilojilojilojilZfilojilojilZEgIOKWiOKWiOKVkeKWiOKWiOKWiOKWiOKWiOKWiOKWiOKVkeKWiOKWiOKVkSAg4paI4paI4pWRCiAgICAgICAgICAgIOKVmuKVkOKVnSAg4pWa4pWQ4pWdICDilZrilZDilZDilZDilZ0gIOKVmuKVkOKVnSAg4pWa4pWQ4pWdICAgICAgICAgICAgICDilZrilZDilZ0gICAgIOKVmuKVkOKVkOKVkOKVkOKVkOKVkOKVneKVmuKVkOKVnSAg4pWa4pWQ4pWd4pWa4pWQ4pWQ4pWQ4pWQ4pWQ4pWQ4pWd4pWa4pWQ4pWdICDilZrilZDilZ0KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAtUHVrYXIgR2lyaSBKYW4gMjAyMA=="

print("\n\033[1m\33[31m"+base64.decodebytes(banner).decode()+"\033[0m")
print("\n")

parser=argparse.ArgumentParser()
parser.add_argument("-m","--mmcu",help="The name of the avr microcontroller you want to flash to.",required=True)
parser.add_argument("-p",help="The partname of the avr microcontroller you want to flash to.",required=True)
parser.add_argument("in_File",help="Name of file to be flashed")
args=parser.parse_args()

printinfo("Starting compilation Sequence..")
compile_process=subprocess.Popen("avr-gcc {} -o out.o -mmcu={}".format(args.in_File,args.mmcu),shell=True,stderr=subprocess.PIPE)
_,out1=compile_process.communicate()
if not "error" in out1.decode():
    printsuccess("Compilation successful !")
    printinfo("Converting to ihex format ..")
    convert_process=subprocess.Popen("avr-objcopy -j .text -j .data -O ihex out.o out.hex",shell=True,stderr=subprocess.PIPE)
    _,out2=convert_process.communicate()
    if not "error" in out2.decode():
        printsuccess("Conversion successful !")
        printinfo("starting flash sequence...")
        print("\033[1m\33[35m ")
        os.system("avrdude -p {} -c usbasp -U flash:w:out.hex".format(args.p)) 
        print("\033[0m")
    else:
        print(out2.decode())
        printfailure("Conversion failed Check error above !")
        sys.exit()
else:
    print(out1.decode())
    printfailure("Compilation failed Check error above !")
    sys.exit()

printinfo("removing temporary files...")
os.remove("out.o")
os.remove("out.hex")
printsuccess("Successful!")
printinfo("script completed!")

    

