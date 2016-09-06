import random,operator,math,pickle,Tkinter,os,gc
from copy import deepcopy

master=Tkinter.Tk()
canvas=Tkinter.Canvas(master,width=300,height=300,bg='black')
canvas.pack()

def setDirectory() :
    if(os.path.isdir("GP Data") is False): os.mkdir("GP Data")
    os.chdir("GP Data")
    run_no=len(os.listdir(os.getcwd()))
    run_no+=1
    os.mkdir("GP Run - %d"%(run_no))
    os.chdir("GP Run - %d"%(run_no))
    

class snake :
    def __init__(self,snake_coords,snakelogic):
        self.snakeloc=snake_coords
        self.snakelogic=snakelogic

    def get_snakeloc(self) : return self.snakeloc

    def get_snakelogic(self) : return self.snakelogic

    def set_snakeloc(self,snakeloc) : self.snakeloc=snakeloc

    def set_snakelogic(self,snakelogic) : self.snakelogic=snakelogic

    def increase_size(self) :
        size=len(self.snakeloc)
        tail_direction=tuple(map(operator.sub,self.snakeloc[size-1],self.snakeloc[size-2]))
        new_tail_coord=tuple(map(operator.add,self.snakeloc[size-1],tail_direction))
        self.snakeloc+=[new_tail_coord]

    def decrease_size(self) :
        if(len(self.snakeloc)>1):
            self.snakeloc=self.snakeloc[:len(self.snakeloc)-1]

    def changeSize(self,change):
        if change>0:
            for i in range(change):self.increase_size()
        elif change<0:
            for i in range(-change):self.decrease_size()

    def get_size(self) : return len(self.snakeloc)



class fwrapper :
    def __init__(self,function,childcount,name):
        self.function=function
        #self.childcount=childcount
        #self.name=name


class node :
    def __init__(self,fw,children):
        self.function=fw.function
        self.children=children
        self.name=fw.name

    def evaluate(self,inp):
        results=[n.evaluate(inp) for n in self.children]
        return self.function(results)

class paramnode :
    def __init__(self,idx):
        self.idx=idx

    def evaluate(self,inp):
        return inp[self.idx]

class constnode :
    def __init__(self,v):
        self.v=v

    def evaluate(self,inp):
        return self.v


    

class funcnode :
    obstacles=[]
    snakeloc=[]
    food=()
    def __init__(self,fw,obs=[],snakelocation=[],foodloc=()):
        self.function=fw.function
        self.name=fw.name
        funcnode.obstacles=obs
        funcnode.snakeloc=snakelocation
        funcnode.food=foodloc

    def evaluate(self,inp):
        return self.function(funcnode.snakeloc,funcnode.obstacles,funcnode.food)

class ifnode :
    obstacles=[]
    snakeloc=[]
    food=()
    doubleMove=False
    nextMove=-1
    def __init__(self,fw,children):
        self.function=fw.function
        #self.name=fw.name
        self.children=children

    def evaluate(self,inp):
        if ifnode.doubleMove is True :
            ifnode.doubleMove=False
            return ifnode.nextMove
        if self.function(ifnode.snakeloc,ifnode.obstacles,ifnode.food) is True :
            return self.children[0].evaluate(inp)
        else :
            return self.children[1].evaluate(inp)

class doublemovenode :
    def __init__(self,children):
        self.children=children

    def evaluate(self,inp):
        if ifnode.doubleMove==False :
            ifnode.doubleMove=True
            ifnode.nextMove=self.children[1].evaluate(inp)
            return self.children[0].evaluate(inp)



def add(l):
    return l[0]+l[1]

def subtract(l):
    return l[0]-l[1]

def multiply(l):
    return l[0]*l[1]

addw=fwrapper(add,2,'add')
subw=fwrapper(subtract,2,'subtract')
mulw=fwrapper(multiply,2,'multiply')

def iffunc(l):
    if l[0]>0 : return l[1]
    else : return l[2]
ifw=fwrapper(iffunc,3,'if')

def isgreater(l):
    if l[0]>l[1]: return 1
    else: return 0
gtw=fwrapper(isgreater,2,'isgreater')

def isequal(l):
    if l[0]==l[1]: return 1
    else: return 0
etw=fwrapper(isequal,2,'isequal')

def getSnakeDirection(snakeloc,obstacles,food) :
    direction=tuple(map(operator.sub,snakeloc[0],snakeloc[1]))
    if direction==(15,0) : return 0
    elif direction==(0,15) : return 3
    elif direction==(-15,0) : return 2
    else : return 1
dirw=fwrapper(getSnakeDirection,0,'direction')
    

def verticalFoodDistance(snakeloc,obstacles,food):
    return food[1]-snakeloc[0][1]
vfdw=fwrapper(verticalFoodDistance,0,'verticalFoodDistance')


def horizontalFoodDistance(snakeloc,obstacles,food) :
    return food[0]-snakeloc[0][0]
hfdw=fwrapper(horizontalFoodDistance,0,'horizontalFoodDistance')

def getLeftObstacleDistance(snakeloc,obstacles,food) :
    obs=obstacles+snakeloc[1:]
    direction=getSnakeDirection(snakeloc,obstacles,food)
    head=snakeloc[0]
    if direction is 0 :
        for y in range(head[1]-15,-15,-15) :
            for obstacle in obs :
                if obstacle==(head[0],y) : return head[1]-y
        return head[1]
    elif direction is 1 :
        for x in range(head[0]-15,-15,-15) :
            for obstacle in obs :
                if obstacle==(x,head[1]) : return head[0]-x
        return head[0]
    elif direction is 2 :
        for y in range(head[1]+15,300,15) :
            for obstacle in obs :
                if obstacle==(head[0],y) : return y-head[1]
        return 300-head[1]
    else :
        for x in range(head[0]+15,300,15) :
            for obstacle in obs :
                if obstacle==(x,head[1]) : return x-head[0]
        return 300-head[0]
lodw=fwrapper(getLeftObstacleDistance,0,'leftObstacleDistance')


def getRightObstacleDistance(snakeloc,obstacles,food) :
    obs=obstacles+snakeloc[1:]
    direction=getSnakeDirection(snakeloc,obstacles,food)
    head=snakeloc[0]
    if direction is 2 :
        for y in range(head[1]-15,-15,-15) :
            for obstacle in obs :
                if obstacle==(head[0],y) : return head[1]-y
        return head[1]
    elif direction is 3 :
        for x in range(head[0]-15,-15,-15) :
            for obstacle in obs :
                if obstacle==(x,head[1]) : return head[0]-x
        return head[0]
    elif direction is 0 :
        for y in range(head[1]+15,300,15) :
            for obstacle in obs :
                if obstacle==(head[0],y) : return y-head[1]
        return 300-head[1]
    else :
        for x in range(head[0]+15,300,15) :
            for obstacle in obs :
                if obstacle==(x,head[1]) : return x-head[0]
        return 300-head[0]
rodw=fwrapper(getRightObstacleDistance,0,'rightObstacleDistance')


def getStraightObstacleDistance(snakeloc,obstacles,food) :
    obs=obstacles+snakeloc[1:]
    direction=getSnakeDirection(snakeloc,obstacles,food)
    head=snakeloc[0]
    if direction is 1 :
        for y in range(head[1]-15,-15,-15) :
            for obstacle in obs :
                if obstacle==(head[0],y) : return head[1]-y
        return head[1]
    elif direction is 2 :
        for x in range(head[0]-15,-15,-15) :
            for obstacle in obs :
                if obstacle==(x,head[1]) : return head[0]-x
        return head[0]
    elif direction is 3 :
        for y in range(head[1]+15,300,15) :
            for obstacle in obs :
                if obstacle==(head[0],y) : return y-head[1]
        return 300-head[1]
    else :
        for x in range(head[0]+15,300,15) :
            for obstacle in obs :
                if obstacle==(x,head[1]) : return x-head[0]
        return 300-head[0]
sodw=fwrapper(getStraightObstacleDistance,0,'straightObstacleDistance')

def dangerLeft(snakeloc,obstacles,food):
    #return getLeftObstacleDistance(snakeloc,obstacles,food)==1
    obs=obstacles+snakeloc[1:]
    head=snakeloc[0]
    direction=getSnakeDirection(snakeloc,obstacles,food)
    if direction is 0 : return (head[0],head[1]-15) in obs
    elif direction is 1: return (head[0]-15,head[1]) in obs
    elif direction is 2: return (head[0],head[1]+15) in obs
    else : return (head[0]+15,head[1]) in obs
dlw=fwrapper(dangerLeft,0,'dangerLeft')

def dangerRight(snakeloc,obstacles,food):
    #return getRightObstacleDistance(snakeloc,obstacles,food)==1obs=obstacles+snakeloc[1:]
    obs=obstacles+snakeloc[1:]
    head=snakeloc[0]
    direction=getSnakeDirection(snakeloc,obstacles,food)
    if direction is 0 : return (head[0],head[1]+15) in obs
    elif direction is 1: return (head[0]+15,head[1]) in obs
    elif direction is 2: return (head[0],head[1]-15) in obs
    else : return (head[0]-15,head[1]) in obs
drw=fwrapper(dangerRight,0,'dangerRight')

def dangerAhead(snakeloc,obstacles,food):
    #return getStraightObstacleDistance(snakeloc,obstacles,food)==1
    obs=obstacles+snakeloc[1:]
    head=snakeloc[0]
    direction=getSnakeDirection(snakeloc,obstacles,food)
    if direction is 0 : return (head[0]+15,head[1]) in obs
    elif direction is 1: return (head[0],head[1]-15) in obs
    elif direction is 2: return (head[0]-15,head[1]) in obs
    else : return (head[0],head[1]+15) in obs
daw=fwrapper(dangerAhead,0,'dangerAhead')

def dangerForwardLeft(snakeloc,obstacles,food):
    obs=obstacles+snakeloc[1:]
    head=snakeloc[0]
    direction=getSnakeDirection(snakeloc,obstacles,food)
    if direction is 0 : return (head[0]+15,head[1]-15) in obs
    elif direction is 1: return (head[0]-15,head[1]-15) in obs
    elif direction is 2: return (head[0]-15,head[1]+15) in obs
    else : return (head[0]+15,head[1]+15) in obs
dflw=fwrapper(dangerForwardLeft,0,'dangerForwardLeft')

def dangerForwardRight(snakeloc,obstacles,food):
    obs=obstacles+snakeloc[1:]
    head=snakeloc[0]
    direction=getSnakeDirection(snakeloc,obstacles,food)
    if direction is 0 : return (head[0]+15,head[1]+15) in obs
    elif direction is 1: return (head[0]+15,head[1]-15) in obs
    elif direction is 2: return (head[0]-15,head[1]-15) in obs
    else : return (head[0]-15,head[1]+15) in obs
dfrw=fwrapper(dangerForwardRight,0,'dangerForwardRight')

def foodAhead(snakeloc,obstacles,food):
    direction=getSnakeDirection(snakeloc,obstacles,food)
    if direction is 0 : return (snakeloc[0][1]==food[1])and(food[0]>snakeloc[0][0])
    elif direction is 1 : return (snakeloc[0][0]==food[0])and(food[1]<snakeloc[0][1])
    elif direction is 2 : return (snakeloc[0][1]==food[1])and(food[0]<snakeloc[0][0])
    else : return (snakeloc[0][0]==food[0])and(food[1]>snakeloc[0][1])
faw=fwrapper(foodAhead,0,'foodAhead')

def foodLeft(snakeloc,obstacles,food):
    direction=getSnakeDirection(snakeloc,obstacles,food)
    if direction is 0 : return (snakeloc[0][0]==food[0])and(food[1]<snakeloc[0][1])
    elif direction is 1 : return (snakeloc[0][1]==food[1])and(food[0]<snakeloc[0][0])
    elif direction is 2 : return (snakeloc[0][0]==food[0])and(food[1]>snakeloc[0][1])
    else : return (snakeloc[0][1]==food[1])and(food[0]>snakeloc[0][0])
flw=fwrapper(foodLeft,0,'foodLeft')

def foodRight(snakeloc,obstacles,food):
    direction=getSnakeDirection(snakeloc,obstacles,food)
    if direction is 2 : return (snakeloc[0][0]==food[0])and(food[1]<snakeloc[0][1])
    elif direction is 3 : return (snakeloc[0][1]==food[1])and(food[0]<snakeloc[0][0])
    elif direction is 0 : return (snakeloc[0][0]==food[0])and(food[1]>snakeloc[0][1])
    else : return (snakeloc[0][1]==food[1])and(food[0]>snakeloc[0][0])
frw=fwrapper(foodRight,0,'foodRight')

def movingRight(snakeloc,obstacles,food):
    return getSnakeDirection(snakeloc,obstacles,food)==0
mrw=fwrapper(movingRight,0,'movingRight')

def movingLeft(snakeloc,obstacles,food):
    return getSnakeDirection(snakeloc,obstacles,food)==2
mlw=fwrapper(movingLeft,0,'movingLeft')

def movingUp(snakeloc,obstacles,food):
    return getSnakeDirection(snakeloc,obstacles,food)==1
muw=fwrapper(movingUp,0,'movingUp')

def movingDown(snakeloc,obstacles,food):
    return getSnakeDirection(snakeloc,obstacles,food)==3
mdw=fwrapper(movingDown,0,'movingDown')

def foodUp(snakeloc,obstacles,food):
    return (food[1]-snakeloc[0][1]<0)
fuw=fwrapper(foodUp,0,'foodUp')

def foodToRight(snakeloc,obstacles,food):
    return (food[0]-snakeloc[0][0]>0)
ftrw=fwrapper(foodRight,0,'foodToRight')



flist=[ifw,gtw,addw,subw,mulw]
fnlist=[vfdw,hfdw,lodw,rodw,sodw]
condlist=[dlw,drw,daw,faw,frw,flw,mrw,mlw,muw,mdw,dfrw,dflw,fuw,ftrw]


def tunetree(root,possibles=[-1,0,1,2]):
    if isinstance(root,constnode) is True and root.evaluate([]) not in possibles :
        root.v=random.choice(possibles)
        if root.v is -1 : root.v=0
        return root
    elif isinstance(root,ifnode) is False :
        return root
    trueFuncPossibles={'dangerLeft':[0,2],'dangerRight':[0,1],'dangerAhead':[1,2]}
    name=root.name
    #if isinstance(root.children[0],constnode) and name in trueFuncPossibles.keys() and root.children[0].evaluate([]) not in trueFuncPossibles[name] :
    #    root.children[0].v=random.choice(trueFuncPossibles[name])
    root.children[1]=tunetree(root.children[1],possibles)
    #root.children[1]=tunetree(root.children[1])
    if name is 'dangerLeft' and 1 in possibles :
        possibles.remove(1)
        root.children[0]=tunetree(root.children[0],possibles)
    elif name is 'dangerRight' and 2 in possibles :
        possibles.remove(2)
        root.children[0]=tunetree(root.children[0],possibles)
    elif name is 'dangerForward' and 0 in possibles :
        possibles.remove(0)
        root.children[0]=tunetree(root.children[0],possibles)
    return root



def makerandomtree(pc,maxdepth=4,fpr=0.6,ppr=0,fnpr=0):    # default fpr=0.5,ppr=0.6
    #if random.random()<fpr and maxdepth>0:
    #    f=random.choice(flist)
    #    children=[makerandomtree(pc,maxdepth-1,fpr,ppr,fnpr)
    #    for i in range(f.childcount)]
    #    return node(f,children)
    #elif random.random()<fnpr:
    #    return funcnode(random.choice(fnlist))
    #elif random.random()<ppr:
    #    return paramnode(random.randint(0,pc-1))
    #else:
    #    return constnode(random.randint(0,300))


    
    if random.random()<fpr and maxdepth>0:
        c=random.choice(condlist)
        children=[makerandomtree(pc,maxdepth-1,fpr,ppr,fnpr),makerandomtree(pc,maxdepth-1,fpr,ppr,fnpr)]
        return (ifnode(c,children))
    elif random.random()<ppr:
        return doublemovenode([constnode(random.choice([0,1,2])),constnode(random.choice([0,1,2]))])
    else :
        return constnode(random.choice([0,1,2]))

    #left=ifnode(dlw,[constnode(2),ifnode(drw,[constnode(0),ifnode(daw,[constnode(1),constnode(0)])])])
    #right=ifnode(daw,[ifnode(dlw,[constnode(2),constnode(1)]),ifnode(dlw,[ifnode(drw,[constnode(0),constnode(1)]),doublemovenode([constnode(1),constnode(2)])])])
    #return ifnode(faw,[left,right])



def mutate(t,pc,probchange=0.1):
    if random.random()<probchange:
        return makerandomtree(pc)
    else:
        result=deepcopy(t)
    if isinstance(t,ifnode):
        result.children=[mutate(c,pc,probchange) for c in t.children]
    return result

def crossover(t1,t2,probswap=0.7,top=1):
    if random.random()<probswap and not top:
        return deepcopy(t2)
    else:
        result=deepcopy(t1)
    if isinstance(t1,ifnode) and isinstance(t2,ifnode):
        result.children=[crossover(c,random.choice(t2.children),probswap,0)
                        for c in t1.children]
    return result

def is_valid_coord(coord,snake_coords,obstacles=[]):
    if coord[0]<0 or coord[0]>=300 or coord[1]<0 or coord[1]>=300 :
        return False
    for coords in snake_coords :
        if coord==coords :
            return False
    for coords in obstacles :
        if coord==coords :
            return False
    return True

def is_over_itself(coords,snake_coords):
    for coord in snake_coords :
        if coord==coords : return True
    return False

def get_inverse_coord(coord):
    if coord[0]<0 : return (285,coord[1])
    elif coord[0]>=300 : return (0,coord[1])
    elif coord[1]<0 : return (coord[0],285)
    elif coord[1]>=300 : return (coord[0],0)
    else : return coord

def get_random_snake_coords(size):
    snake_coords=[]
    head=(15*(int)(random.randrange(0,300)/15),15*(int)(random.randrange(0,300)/15))
    snake_coords+=[head]
    prev=head
    for i in range(1,size):
        raw_possibles=[(1,0),(0,-1),(-1,0),(0,1)]
        possibles=[]
        for possible in raw_possibles:
            change=tuple(map(operator.mul,possible,(15,15)))
            new_coord=tuple(map(operator.add,prev,change))
            if is_valid_coord(new_coord,snake_coords) :
                possibles+=[new_coord]
        if len(possibles) is 0 :
            return get_random_snake_coords(size)
        next_coord=random.choice(possibles)
        snake_coords+=[next_coord]
        prev=next_coord
    return [(15,0),(0,0)]
    #return snake_coords

def get_random_obstacle_coords(size):
    snake_coords=[]
    head=(15*(int)(random.randrange(0,300)/15),15*(int)(random.randrange(0,300)/15))
    snake_coords+=[head]
    prev=head
    for i in range(1,size):
        raw_possibles=[(1,0),(0,-1),(-1,0),(0,1)]
        possibles=[]
        for possible in raw_possibles:
            change=tuple(map(operator.mul,possible,(15,15)))
            new_coord=tuple(map(operator.add,prev,change))
            if is_valid_coord(new_coord,snake_coords) :
                possibles+=[new_coord]
        if len(possibles) is 0 :
            return get_random_obstacle_coords(size)
        next_coord=random.choice(possibles)
        snake_coords+=[next_coord]
        prev=next_coord
    #return [(15,0),(0,0)]
    return snake_coords

def get_random_foodloc(obstacles):
    foodloc=(15*(int)(random.randrange(0,300)/15),15*(int)(random.randrange(0,300)/15))
    while(foodloc in obstacles):foodloc=(15*(int)(random.randrange(0,300)/15),15*(int)(random.randrange(0,300)/15))
    return foodloc

def get_random_snake(size,pc):
    return snake(get_random_snake_coords(2),makerandomtree(pc,30))

def get_input(snake_,food,obstacles=[],foods=1):
    snakeloc=snake_.get_snakeloc()
    inp=[food[0],food[1],len(snakeloc),snakeloc[0][0],snakeloc[0][1]]
    #inp=[food[0],food[1],len(snakeloc),snakeloc[0][0],snakeloc[0][1]]
    #size=len(snakeloc)
    #inp=inp+[snakeloc[size/2][0],snakeloc[size/2][0],snakeloc[size-1][0],snakeloc[size-1][0]]
    #for obstacle in range(obstacles):
    #    inp+=[snakeloc[((int)((len(snakeloc)-1)*obstacle/obstacles))][0],snakeloc[((int)((len(snakeloc)-1)*obstacle/obstacles))][1]]
    return inp


def scorefunction(snake_,foods,obstacles=[],moves=1000,spacing=15) :
    score=0
    #food=(15*(int)(random.randrange(0,300)/15),15*(int)(random.randrange(0,300)/15))
    loopcheck=[]
    snakelogic=snake_.get_snakelogic()
    foodindex=0
    food=foods[foodindex]
    ifnode.doubleMove=False
    ifnode.nextMove=-1
    for j in range(moves) :
        snakeloc=snake_.get_snakeloc()
        ifnode.snakeloc=snakeloc
        ifnode.obstacles=obstacles
        ifnode.food=food
        direction=tuple(map(operator.sub,snakeloc[0],snakeloc[1]))
        head=snakeloc[0]
        size=len(snakeloc)
        #possible_moves=[(spacing,0),(0,-spacing),(-spacing,0),(0,spacing)]
        #moves_available=[]
        #neg_direction=tuple(map(operator.mul,direction,(-1,-1)))
        #try :
        #    possible_moves.remove(neg_direction)
        #except :
        #    possible_moves.remove(tuple(map(operator.mul,tuple(map(operator.sub,get_inverse_coord(snakeloc[0]),snakeloc[1])),(-1,-1))))
        #move=(snakelogic.evaluate(get_input(snake_,food,25)))%3
        #move_direction=possible_moves[move]
        if ifnode.doubleMove==True:
            move=ifnode.nextMove
            ifnode.doubleMove=False
        else:
            move=(snakelogic.evaluate(get_input(snake_,food)))%3
        move_direction=direction
        if move is 1 :                                                              # move left
            if direction==(15,0):move_direction=(0,15)
            elif direction==(0,15):move_direction=(-15,0)
            elif direction==(-15,0):move_direction=(0,-15)
            else:move_direction=(15,0)
        elif move is 2 :                                                            # move right
            if direction==(15,0):move_direction=(0,-15)
            elif direction==(0,15):move_direction=(15,0)
            elif direction==(-15,0):move_direction=(0,15)
            else:move_direction=(-15,0)
        for i in range(size-1,0,-1) :
            snakeloc[i]=snakeloc[i-1]
        snakeloc[0]=tuple(map(operator.add,snakeloc[0],move_direction))
        head=snakeloc[0]
        if head==food :
            score+=10000
            snake_.increase_size()
            if snake_.get_size() is 80 : score+=100000000
            #food=(15*(int)(random.randrange(0,300)/15),15*(int)(random.randrange(0,300)/15))
            foodindex+=1
            food=foods[foodindex]
        elif is_valid_coord(head,snakeloc[1:],obstacles) is False :
            if is_over_itself(head,snakeloc[1:]) is True : break#return score-5000000+2*j
            break#score-10000000+2*j
        score-=(math.fabs(head[0]-food[0])+math.fabs(head[1]-food[0]))*0.01
        loopcheck+=[(head,direction,food)]
    #datadump.changed_population.append(snake_)
    #datadump.scores.append(score)
    #print "Finished"
    looping=False
    for t in loopcheck :
        if loopcheck[loopcheck.index(t)+1:].count(t)>0 :
            i=loopcheck.index(t)
            j=loopcheck[i+1:].index(t)
            for k in range(i+1,j):
                if loopcheck[2]==loopcheck[k]:
                    looping=True
                    break
    return (score,looping)

class datadump:
    scores=[]
    changed_population=[]

def rankfunction(population,obstacles=[],moves=1000) :
    #datadump.scores=[]
    scores=[]
    loops=[]
    #obstacle_no=random.choice([0,1,2])
    #obs=obstacles
    #for n in range(obstacle_no):
    #    obs+=get_random_obstacle_coords(random.choice([5,6,7,8,9,10]))
    obs=get_random_obstacle_coords(8)
    if random.random()>0.6 :
        obs+=get_random_obstacle_coords(5)
    if random.random()>0.85 :
        obs+=get_random_obstacle_coords(4)
    #for o in obs :
    #    if o[0]<75 or o[1]<75 : obs.remove(o)
    #obs+=obstacles
    #obno=random.choice(range(15,25))
    #obs=[]
    #for i in range(obno):obs+=get_random_obstacle_coords(1)
    for o in obs :
        if o[0]<75 or o[1]<75 : obs.remove(o)
    obs+=obstacles
    foods=[get_random_foodloc(obs) for m in range(moves)]
    #datadump.changed_population=[]
    #i=0
    #threads=100
    #scores_length=0
    #start=True
    for snake in population :
        #scores+=[scorefunction(snake,foods,obs,moves)]
        score=scorefunction(snake,foods,obs,moves)
        scores+=[score[0]]
        loops+=[score[1]]
    #    try:thread.start_new_thread(scorefunction,(snake,foods,obstacles,moves))
    #    except:print "Thread error"
    #while len(datadump.scores)!=len(population):
    #    print len(datadump.scores)
    #    time.sleep(0.001)
    #    if start is False:
    #        threads=len(datadump.scores)-scores_length
    #    start=False
    #    for j in range(0,threads):
    #        try:
    #            if i<len(population):
    #                thread.start_new_thread(scorefunction,(population[i],foods,obstacles,moves))
    #                i+=1
    #            else:
    #                pass
    #        except:print "Thread error"
    #    scores_length=len(datadump.scores)
    #return datadump.scores,datadump.changed_population
    return scores,loops

def change_canvas(snake,prev_snake_indices,food,obstacles=[],spacing=15):
    for idx in prev_snake_indices :
        canvas.delete(idx)
    snakelogic=snake.get_snakelogic()
    snakeloc=snake.get_snakeloc()
    ifnode.snakeloc=snakeloc
    ifnode.obstacles=obstacles
    ifnode.food=food
    direction=tuple(map(operator.sub,snakeloc[0],snakeloc[1]))
    head=snakeloc[0]
    size=len(snakeloc)
    if ifnode.doubleMove==True:
            move=ifnode.nextMove
            ifnode.doubleMove=False
    else:
        move=(snakelogic.evaluate(get_input(snake,food)))%3
    move_direction=direction
    if move is 1 :                                                              # move left
        if direction==(15,0):move_direction=(0,15)
        elif direction==(0,15):move_direction=(-15,0)
        elif direction==(-15,0):move_direction=(0,-15)
        else:move_direction=(15,0)
    elif move is 2 :                                                            # move right
        if direction==(15,0):move_direction=(0,-15)
        elif direction==(0,15):move_direction=(15,0)
        elif direction==(-15,0):move_direction=(0,15)
        else:move_direction=(-15,0)
    for i in range(size-1,0,-1) :
        snakeloc[i]=snakeloc[i-1]
    snakeloc[0]=tuple(map(operator.add,snakeloc[0],move_direction))
    snake_head=snakeloc[0]
    prev=snake_head
    snake_indices=[]
    for coord in snakeloc :
        idx=canvas.create_rectangle(coord[0]+4,coord[1]+4,coord[0]+spacing-4,coord[1]+spacing-4,fill='red')
        snake_indices+=[idx]
        if coord!=snake_head :
            direction=tuple(map(operator.sub,coord,prev))
            idx=canvas.create_line(coord[0]+spacing/2,coord[1]+spacing/2,prev[0]+spacing/2,prev[1]+spacing/2,width=spacing-9,fill='red')
            snake_indices+=[idx]
        prev=coord
    idx=canvas.create_rectangle(snake_head[0]+4,snake_head[1]+4,snake_head[0]+spacing-4,snake_head[1]+spacing-4,fill='orange')
    snake_indices+=[idx]
    snake.set_snakeloc(snakeloc)
    head=snakeloc[0]
    if head==food :
        snake.increase_size()
        canvas.create_oval(food[0]+1,food[1]+1,food[0]+spacing-1,food[1]+spacing-1,fill='black')
        idx=canvas.create_rectangle(snake_head[0]+4,snake_head[1]+4,snake_head[0]+spacing-4,snake_head[1]+spacing-4,fill='orange')
        snake_indices+=[idx]
        food=get_random_foodloc(obstacles)
        canvas.create_oval(food[0]+1,food[1]+1,food[0]+spacing-1,food[1]+spacing-1,fill='yellow')
    #elif is_valid_coord(head,snakeloc[1:],obstacles) is False:master.destroy()
    master.after(100,change_canvas,snake,snake_indices,food,obstacles)


def display_grid(w=500,h=500,spacing=15,food=(0,0),snake=get_random_snake(2,4),obstacles=[]) :
    for i in range(0,w,spacing):
        canvas.create_line(i,0,i,h,fill='white')
    for i in range(0,h,spacing) :
        canvas.create_line(0,i,w,i,fill='white')
    canvas.create_oval(food[0]+1,food[1]+1,food[0]+spacing-1,food[1]+spacing-1,fill='yellow')
    for o in obstacles :
        canvas.create_rectangle(o[0]+2,o[1]+2,o[0]+spacing-2,o[1]+spacing-2,fill='gray')
    snakeloc=snake.get_snakeloc()
    snake_head=snakeloc[0]
    prev=snake_head
    snake_indices=[]
    for coord in snakeloc :
        idx=canvas.create_rectangle(coord[0]+4,coord[1]+4,coord[0]+spacing-4,coord[1]+spacing-4,fill='red')
        snake_indices+=[idx]
        if coord!=snake_head :
            direction=tuple(map(operator.sub,coord,prev))
            idx=canvas.create_line(coord[0]+spacing/2,coord[1]+spacing/2,prev[0]+spacing/2,prev[1]+spacing/2,width=spacing-9,fill='red')
            snake_indices+=[idx]
        prev=coord
    idx=canvas.create_rectangle(snake_head[0]+4,snake_head[1]+4,snake_head[0]+spacing-4,snake_head[1]+spacing-4,fill='orange')
    snake_indices+=[idx]
    master.after(1000,change_canvas,snake,snake_indices,food,obstacles)
    master.mainloop()

def evolve(pc,popsize,maxgen=500,obstacles=[],mutationrate=0.1,breedingrate=0.4,pexp=0.7,pnew=0.5):
    #best_snakes=[]
    best_scores_high=[]
    best_scores_low=[]
    mean_scores=[]
    population=[get_random_snake(2,pc) for i in range(popsize)]
    def selectindex( ):
        return int(math.log(random.random())/math.log(pexp))
    #moves=1000
    for gen in range(maxgen) :
        #if gen%100==0 : moves+=1000
        scores,loops=rankfunction(population,obstacles,5000)
        zipped_snakes=zip(scores,population)
        zipped_snakes.sort()
        zipped_snakes.reverse()
        sorted_=list(zip(*zipped_snakes))
        del zipped_snakes
        sorted_snakes=list(sorted_[1])
        del sorted_
        del population
        population=sorted_snakes[:5]
        #best_snakes+=[sorted_snakes[0]]
        while len(population)<popsize :
            if random.random()>pnew :
                population.append(snake(get_random_snake_coords(2),mutate(
                crossover(sorted_snakes[selectindex( )].get_snakelogic(),
                sorted_snakes[selectindex( )].get_snakelogic(),
                probswap=breedingrate),
                pc,probchange=mutationrate)))
            else :
                population.append(get_random_snake(2,pc))
        del sorted_snakes
        for s in population : s.set_snakeloc(get_random_snake_coords(2))
        #population=new_population
        #del new_population
        d=zip(scores,loops)
        scores.sort()
        scores.reverse()
        print "Generation",gen,"completed | Best scores obtained =",scores[0],"-",scores[4],d[0][1]
        del d
        best_scores_high+=[scores[0]]
        best_scores_low+=[scores[4]]
        mean_scores+=[float(sum(scores)/len(population))]
        del scores
        gc.collect()
    setDirectory()
    best_snake=population[0]
    del population
    print "Saving data for analysis..."
    data_file_high=open('Best scores high.txt','w')
    data_file_low=open('Best scores low.txt','w')
    data_file_mean=open('Mean scores.txt','w')
    for score in best_scores_high : data_file_high.write("%d "%(score))
    for score in best_scores_low : data_file_low.write("%d "%(score))
    for score in mean_scores : data_file_mean.write("%d "%(score))
    data_file_mean.close()
    data_file_high.close()
    data_file_low.close()
    gen_no=input("Enter the generation whose best snake you want to simulate : ")
    if gen_no is -1 :
        pass
    #best_snake=best_snakes[gen_no]
    print "Saving best snake data..."
    data_file_snake=open("Best snake.txt","w")
    pickle.dump(best_snake,data_file_snake)
    data_file_snake.close()
    print "Simulating best snake..."
    foodloc=(15*(int)(random.randrange(0,300)/15),15*(int)(random.randrange(0,300)/15))
    best_snake.set_snakeloc(get_random_snake_coords(2))
    display_grid(300,300,15,foodloc,best_snake,obstacles)

def simulate_saved_snake(obstacles):
    data_file=open("GP Data/GP Run - 76/Best snake.txt","r")
    snake_=pickle.load(data_file)
    data_file.close()
    foodloc=get_random_foodloc(obstacles)
    snake_.set_snakeloc(get_random_snake_coords(2))
    display_grid(300,300,15,foodloc,snake_,obstacles)


obstacles=[]
#for i in range(10) : obstacles+=get_random_obstacle_coords(1)
#for o in obstacles :
#    if o[0]<75 or o[1]<75 : obstacles.remove(o)
for i in range(0,300,15):
    obstacles+=[(-15,i),(300,i),(i,-15),(i,300)]
#for i in range(20):obstacles+=get_random_obstacle_coords(1)
evolve(5,500,100,obstacles)
#obstacles+=get_random_obstacle_coords(15)
#simulate_saved_snake(obstacles)

    
