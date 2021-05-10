#!/usr/bin/env python2.7

from random import shuffle, randrange
import os

W = 1
w = 1
A = -9
a = -9
S = -1
s = -1
D = 9
d = 9
valid_moves = [W, w, A, a, S, s, D, d]

def welcome():
    print "Welcome to the aMAZEing Maze"
    print "Your goal is to get from one side of the board to the other."
    print "Your character is represented by \"OO\" and the finish will be \"FF\""
    print "W/w - Move up!"
    print "A/a - Move left!"
    print "S/s - Move down!"
    print "D/d - Move right!"

def make_move(maze):
    print maze
    move = input("Make your move: ")
    if move not in valid_moves:
        raise NameError
    # TODO: Move the player around the board
    # Was a little cruched for time this year so I didn't feel like writing
    # the gameplay. I hope that's okay :/
    return True

def replace_last(s, replace_what, replace_with):
    head, _sep, tail = s.rpartition(replace_what)
    return head + replace_with + tail

# Randomly generate the gameboard and insert start/finish
def make_maze(w = 16, h = 16):
    vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]
    ver = [["|  "] * w + ['|'] for _ in range(h)] + [[]]
    hor = [["+--"] * w + ['+'] for _ in range(h + 1)]

    def walk(x, y):
        vis[y][x] = 1
        d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        shuffle(d)
        for (xx, yy) in d:
            if vis[yy][xx]: continue
            if xx == x: hor[max(y, yy)][x] = "+  "
            if yy == y: ver[y][max(x, xx)] = "   "
            walk(xx, yy)

    walk(randrange(w), randrange(h))

    s = ""
    for (a, b) in zip(hor, ver):
        s += ''.join(a + ['\n'] + b + ['\n'])
    s = s.replace(" ", "O", 2)
    s = replace_last(s, "  ", "FF")
    return s

def __main__():
    welcome()
    still_playing = True
    maze = make_maze()
    while(still_playing):
        still_playing = make_move(maze)
    print "Congrats! You've finished the maze! Here's your flag:"
    os.system("/bin/cat flag.txt")

__main__()