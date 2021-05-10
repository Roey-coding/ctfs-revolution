#!/usr/bin/python3

import pickle
import base64

CANVSIZE = 16

canvas = [[" " for i in range(CANVSIZE)] for j in range(CANVSIZE)]

def print_canvas(canvas):
    print("#" * (CANVSIZE + 2))
    for line in canvas:
        print("#", end="")
        for char in line:
            print(char, end="")
        print("#")
    print("#" * (CANVSIZE + 2))

def print_help():
    print("Listing commands...")
    print("display             Display the canvas")
    print("clearall            Clear the canvas")
    print("set [row] [col]     Set a particular pixel")
    print("clear [row] [col]   Clear a particular pixel")
    print("export              Export the canvas state")
    print("import [canvas]     Import a previous canvas")
    print("exit                Quit the program")

def change_pixel(command):
    row = int(command[1])
    col = int(command[2])
    if row < 0 or row >= CANVSIZE or col < 0 or col >= CANVSIZE:
        print("Index out of range!")
        return
    canvas[row][col] = "0" if command[0] == "set" else " "
    print_canvas(canvas)

# PROGRAM STARTS BELOW

print("Welcome to the Paint Program!")
print("Paint us a new poster for the Jellyspotters 2021 convention. Make Kevin proud.")
print("Type 'help' for help.")

while True:
    userinput = input("> ")
    split = userinput.split(" ")
    cmd = split[0]
    if cmd == "?" or cmd == "help":
        print_help()
    elif cmd == "":
        continue
    elif cmd == "display":
        print_canvas(canvas)
    elif cmd == "clearall":
        canvas = [[" " for i in range(CANVSIZE)] for j in range(CANVSIZE)]
    elif cmd == "set" or cmd == "clear":
        change_pixel(split)
    elif cmd == "export":
        out = base64.b64encode(pickle.dumps(canvas)).decode("ascii")
        print("Exported canvas string:")
        print(out)
    elif cmd == "import":
        if len(split) < 2:
            print("Expected argument (canvas export string). Import failed.")
            continue
        print("Importing...")
        imp = pickle.loads(base64.b64decode(split[1]))
        print("Done!")
        canvas = imp
        print_canvas(canvas)
        pass
    elif cmd == "exit" or cmd == "quit":
        break
    else:
        print(f"Unrecognized command '{cmd}'.")

print("Thank you for using the Paint Program! Goodbye.")