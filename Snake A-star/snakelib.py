import operator,math,Tkinter,random


master=Tkinter.Tk()
canvas=Tkinter.Canvas(master,width=300,height=300,bg='black')
canvas.pack()


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


def reconstruct_path(camefrom,current):
    total_path=[current]
    while current in camefrom:
        current=camefrom[current]
        total_path.append(current)

    return total_path

def h(start,goal,snakeloc):
    if start in snakeloc[1:]:
        i=snakeloc.index(start)
        return (int)(math.fabs(start[0]-goal[0])+math.fabs(start[1]-goal[1]))+i*500000
    return (int)(math.fabs(start[0]-goal[0])+math.fabs(start[1]-goal[1]))


def getMove(snakeloc,obs,food):

    obstacles=[]
    obstacles+=obs
    obstacles+=snakeloc[1:]
    
    closedset=[]
    openset=[snakeloc[0]]
    camefrom={}

    g={}
    f={}

    vertices=[(i,j) for i in range(300,0,15) for j in range(300,0,15)]
    for v in vertices:g[v]=9999999999999999

    g[snakeloc[0]]=0

    for v in vertices:f[v]=99999999999999999

    f[snakeloc[0]]=g[snakeloc[0]]+h(snakeloc[0],food,snakeloc)

    while len(openset) is not 0:
        current=None
        minval=None
        for node in openset:
            if minval is None:
                current=node
                minval=f[node]
            elif f[node]<minval:
                current=node
                minval=f[node]
        if current==food :
            path=reconstruct_path(camefrom,food)
            return path[len(path)-2]

        openset.remove(current)
        closedset.append(current)

        n1=(current[0]+15,current[1])
        n2=(current[0],current[1]-15)
        n3=(current[0]-15,current[1])
        n4=(current[0],current[1]+15)

        neighbours=[n1,n2,n3,n4]
        random.shuffle(neighbours)

        for n in neighbours:
            if n in obstacles:
                continue
            elif n in closedset:
                continue

            tentative_g=g[current]+1

            if n not in openset or tentative_g < g[n]:
                camefrom[n]=current
                g[n]=tentative_g
                f[n]=g[n]+h(n,food,snakeloc)
                if n not in openset:
                    openset.append(n)
    direction=(snakeloc[0][0]-snakeloc[1][0],snakeloc[0][1]-snakeloc[1][1])
    return (snakeloc[0][0]+direction[0],snakeloc[0][1]+direction[1])


def get_foodloc(snakeloc,obstacles):
    food=(15*(int)(random.randrange(0,300)/15),15*(int)(random.randrange(0,300)/15))
    while food in snakeloc or food in obstacles:food=(15*(int)(random.randrange(0,300)/15),15*(int)(random.randrange(0,300)/15))
    return food

def change_canvas(snake,prev_snake_indices,food,obstacles=[],spacing=15):
    for idx in prev_snake_indices :
        canvas.delete(idx)
    snakeloc=snake.get_snakeloc()
    size=len(snakeloc)
    for i in range(size-1,0,-1) :
        snakeloc[i]=snakeloc[i-1]
    snakeloc[0]=getMove(snakeloc,obstacles,food)
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
        food=get_foodloc(snakeloc,obstacles)
        canvas.create_oval(food[0]+1,food[1]+1,food[0]+spacing-1,food[1]+spacing-1,fill='yellow')
    #elif is_valid_coord(head,snakeloc[1:],obstacles) is False:master.destroy()
    master.after(50,change_canvas,snake,snake_indices,food,obstacles)


def display_grid(w=500,h=500,spacing=15,food=(0,0),snake=snake([],0),obstacles=[]) :
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

s=snake([(15,0),(0,0)],0)
obstacles=[]
for i in range(0,300,15):
    obstacles+=[(-15,i),(300,i),(i,-15),(i,300)]
for i in range(3):obstacles+=get_random_obstacle_coords(10)
display_grid(300,300,15,(270,270),s,obstacles)
            
    
