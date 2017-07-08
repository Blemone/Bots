import hlt
from hlt import NORTH, EAST, SOUTH, WEST, STILL, Move, Square
directions = [NORTH, EAST, SOUTH, WEST]
import random
import math
f = open("debug.txt", "w")


myID, game_map = hlt.get_init()
hlt.send_init("Tony's Bot")



#This functions finds the direction with the highest production
#It will average the production in a triangle in each given direction, and then return the direction with the heighest.
def fhpd(square):
##    #Go through each direction
##    h = 0
##    d = STILL
##
##    for direction, neighbor in enumerate(game_map.neighbors(square)):
##        t = 0
##        current = square
##        ls = []
##        for x in range(5):
##            t += game_map.get_target(current, direction).production
##            ls.append(game_map.get_target(current, direction))
##            ls.append(game_map.get_target(current, direction))
##            current = game_map.get_target(current, direction)
##            
##        while len(ls) > 0:
##            q = 0
##            for l in ls:
##                if q%2 == 0:
##                    t += game_map.get_target(l, (direction + 1)%3).production
##                    ls.pop(0)
##                    ls.append(game_map.get_target(l, (direction + 1)%3))
##                else:
##                    t += game_map.get_target(l, (direction + 3)%3).production
##                    ls.pop(0)
##                    ls.append(game_map.get_target(l, (direction + 3)%3))
##
##                q += 1
##            ls.pop(0)
##            ls.pop(0)
##
##        if t > h and neighbor.strength < square.strength:
##            h = t
##            d = direction
##    
##        return d
    h = 0
    d = STILL

    for direction, neighbor in enumerate(game_map.neighbors(square)):
        t = 0
        current = square
        for x in range(7):
            t += game_map.get_target(current, direction).production
            current = game_map.get_target(current, direction)
        if t > h and neighbor.strength < square.strength * 1.3 and (neighbor.owner != myID or game_map.get_target(neighbor, direction).owner != myID):
            h = t
            d = direction

    return d
            

#Returns amount of nearby enemies

def ne(square):
    total = 0
    for direction, neighbor in enumerate(game_map.neighbors(square)):
        for direction1, neighbor1 in enumerate(game_map.neighbors(neighbor)):
            if neighbor1.owner != myID and neighbor1.owner != 0:
                total += 1
        if neighbor.owner != myID and neighbor.owner != 0:
            total += 1

    return total


#Returns the strength of nearby enemies.
def nes(square):
    total = 0
    for direction, neighbor in enumerate(game_map.neighbors(square)):
        for direction1, neighbor1 in enumerate(game_map.neighbors(neighbor)):
            if neighbor1.owner != myID and neighbor1.owner != 0:
                total += neighbor1.strength
        if neighbor.owner != myID and neighbor.owner != 0:
            total += neighbor.strength

    return total

#Returns true if in deep territory, i.e. 2 layers of friendlies around it.
def dt(square):
    deep = True
    for direction, neighbor in enumerate(game_map.neighbors(square)):
        for direction1, neighbor1 in enumerate(game_map.neighbors(neighbor)):
            if neighbor1.owner != myID:
                deep = False
        if neighbor.owner != myID:
            deep = False

    return False

#Returns strength of nearby friendlies
def nfs(square):
    total = square.strength
    for direction, neighbor in enumerate(game_map.neighbors(square)):
        for direction1, neighbor1 in enumerate(game_map.neighbors(neighbor)):
            if neighbor1.owner == myID:
                total += neighbor1.strength
        if neighbor.owner == myID:
            total += neighbor.strength

    return total
        
#Get the weakest enemy (called when not surrounded by own territory preferably)
#Return still when not surrounded by  (takable) enemy
def fwe(square):
    mins = square.strength
    d = STILL
    for direction, neighbor in enumerate(game_map.neighbors(square)):
        if neighbor.strength < mins and neighbor.owner != myID:
            mins = neighbor.strength
            d = direction
    
    return d

#Find nearest enemy. Returns 12 if no enemy within half map size.
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



    
#Find neaerest border

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
        
    
#Find highest production
def fhp(square):
    m = 0
    f = NORTH
    for direction, neighbor in enumerate(game_map.neighbors(square)):
        if neighbor.production > m and neighbor.strength < square.strength:
            f = direction
        
    

    return direction




##def findenemy(square):
##    current = square 
##    #This should find and return the nearest direction towards an enemy.
##    ls1 = []
##    ls2 = []
##    ls3 = []
##
##    #go through each neighbor
##    for direction, neighbor in enumerate(game_map.neighbors(square)):
##        ls1.append(neighbor)
##        for x in range(2):
##        #for loops less than length of map
##            for current in ls1:
##                for direction1, neighbor1 in enumerate(game_map.neighbors(current)):
##                    ls2.append(neighbor1)
##            #add all neighbors from list to another list
##            ls1 = []
##            #clear first list
##            #check if anything in second list is not our own piece
##            for o in ls2:
##                if o.owner != myID and o.owner != 0:
##                    ls3.append([direction, x])
##                #if so, return direction
##            ls1 = ls2
##            ls2 = []
##            #list 1 = list 2, clear list 2
##    i = 0
##    for k in range(len(ls3)):
##        m = game_map.width
##        
##        if ls3[k][1] < m:
##            m = ls3[k][1]
##            i = k
##
##    if len(ls3) != 0:
##        f.write("test")
##        return ls3[i][0]
##    return NORTH


#This finds the highest production in a particular direction however its decision-making is weighted based on strength and friendly strength and enemy strength.
def fhwpd(square):
    h = 0
    d = STILL

    for direction, neighbor in enumerate(game_map.neighbors(square)):
        t = 0
        ds = 0
        current = square
        for x in range(7):
            t += game_map.get_target(current, direction).production
            ds += game_map.get_target(current, direction).strength
            current = game_map.get_target(current, direction)
        if t > h and ds < square.strength * 2.5 + nfs(square) + square.production * 7 and (neighbor.owner != myID or game_map.get_target(neighbor, direction).owner != myID):
            h = t
            d = direction

    return d

#This secondary function ensures that if assign_move returns a value which will result in a high loss of strength
#or some other error, it will not do that.

def assign_movec(square):
    direction = assign_move(square)
    target = game_map.get_target(square, direction)

    #Check that merging won't cause a large loss. If it does, wait.
    if target.owner == myID and target.strength + square.strength > 290:
        return Move(square, STILL)

    #Check that it's not trying to take a stronger square
    if target.owner != myID and target.strength > square.strength:
        return Move(square, STILL)

    return Move(square, direction)


#This only returns a direction, as it needs to be checked by the check function
def assign_move(square):
      #Full strength squares should head to nearest border
    if square.strength == 255:
        if fne(square) == 12:
            return fnb(square)
        else:
            return fne(square)

    total = 0
     #Go through all neighbours
    for direction, neighbor in enumerate(game_map.neighbors(square)):
       
        c = True
        total += neighbor.strength
        if neighbor.owner != myID:
            #The square is not surrounded by its own team
            c = False
        
        #If it is next to a friendly neighbour and they are both relatively weak, try merge
        if neighbor.owner == myID and (square.strength < 50 and square.strength > 10) and (neighbor.strength < 50 and neighbor.strength > square.production):
            #remain still if the production is higher
            #make sure they do not waste too much:
            if neighbor.strength + square.strength >= 280:
                pass

            else:
                if square.production < neighbor.production:
                    return direction
                elif square.production == neighbor.production:
                    if random.randint(0, 1) == 1:
                        return direction
                    else:
                        return STILL
                else:
                    return STILL

  
    #If low on territory and high strength and at a border, move towards areas of high production
    if territory < 40 and square.strength > square.production * 4 and c == False:
        return fhwpd(square)
    
    #If low on territory and has medium strength, just go to nearest border (assuming it can take it)
    if territory < 40 and square.strength > square.production * 5:
        if dt(square) != True:
            return fwe(square)
        else:
            return fnb(square)
        
    #Move away from stronger enemies, and move towards weaker enemies. 
    if fne(square) != 12 and ne(square) > 3:
        #If weak, remain still
        if square.strength < square.production * 5:
            return STILL
        if nfs(square) < nes(square):
            return hlt.opposite_cardinal(fne(square))
        else:
            return fne(square)

    #If it is being attacked, i.e. has many enemies nearby, just attack
    if ne(square) > 4 and square.strength > square.production * 5:
        if fne(square) == 12:
            return fnb(square)
        else:
            return fne(square)


   
                
    #Otherwise if the square is in its territory and quite strong, move towards nearest enemy preferably, or near border
    if c == True and square.strength > 40 and territory > 30:
        if fne(square) == 12:
            return fnb(square)
        else:
            return fne(square)
        


    #If it is surrounded by weak neighbors of its own type, then stay still
    if c == True and total < square.production * 12 and square.strength < 200:
        return STILL

    

        

    
    #If it is next to an enemy, take the weakest enemy
    if c == False:
        return fwe(square)
    


        

    #Default just stay still
    return STILL


frame = 0
territory = 0
enemies = 0
while True:
    frame += 1
    enemies = 0
    f.write("TEST")
    game_map.get_frame()
    territory = 0
    for square in game_map:
        if square.owner == myID:
            territory += 1
            for direction, neighbor in enumerate(game_map.neighbors(square)):
                if neighbor.owner != myID and neighbor.owner != 0:
                    enemies += 1
            
    moves = [assign_movec(square) for square in game_map if square.owner == myID]
    hlt.send_frame(moves)
