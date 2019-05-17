import hlt
from hlt import NORTH, EAST, SOUTH, WEST, STILL, Move, Square
import random

frame = 0
myID, game_map = hlt.get_init()
hlt.send_init("ChrisBot")
directions = [NORTH,EAST,SOUTH,WEST]

def fnb(square):
    d = NORTH
    maxD = game_map.width
    
    current = square
    for direction, neighbor in enumerate(game_map.neighbors(square)):
        cd = direction
        current = neighbor
        dis = 0
        while dis < maxD and current.owner == myID:
            dis += 1
            for direction2, neighbor2 in enumerate(game_map.neighbors(current)):
                if direction2 == cd:
                    current = neighbor2

        if dis < maxD:
            maxD = dis
            d = cd
    return d



def relist(li):
    a = []
    for i in range(len(li)):
        a.append(max(li))
        li.remove(max(li))
    return a

def fne(square):
    d = 12
    maxD = game_map.width
    
    current = square
    for direction, neighbor in enumerate(game_map.neighbors(square)):
        cd = direction
        current = neighbor
        dis = 0
        while dis < maxD and (current.owner == myID or current.owner == 0):
            dis += 1
            for direction2, neighbor2 in enumerate(game_map.neighbors(current)):
                if direction2 == cd:
                    current = neighbor2

        if dis < maxD:
            maxD = dis
            d = cd
    return d

def write(a):
    f = open("debug.txt","a")
    f.write(str(a))
    f.close()

def fab(square):
    d = []
    maxD = game_map.width
    current = square
    for direction, neighbor in enumerate(game_map.neighbors(square)):
        cd = direction
        current = neighbor
        dis = 0
        while dis < maxD and current.owner == myID:
            dis += 1
            for direction2, neighbor2 in enumerate(game_map.neighbors(current)):
                if direction2 == cd:
                    current = neighbor2
        d.append(dis)
    return d


def assign_move(square):
    write((frame, " "))
    svind = 5
    c = True
    #Check if it is on the edge of mass
    for direction, neighbor in enumerate(game_map.neighbors(square)):
        if neighbor.owner != myID:
            c = False
    for direction, neighbor in enumerate(game_map.neighbors(square)):
        #If too big
        if square.strength >= 220:
            return Move(square, fnb(square))
        #If I can take it w some left over
        if neighbor.owner != myID and neighbor.strength+10 < square.strength:
            return Move(square, direction)
        #If I am a better factory
        if square.strength > square.production*svind:
            return Move(square, fnb(square))
    return Move(square, STILL)
        


while True:
    game_map.get_frame()
    moves = [assign_move(square) for square in game_map if square.owner == myID]
    hlt.send_frame(moves)
    frame += 1
