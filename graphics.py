import Tkinter,random,operator,time


master=Tkinter.Tk()
canvas=Tkinter.Canvas(master,width=750,height=600,bg='black')
canvas.pack()

def getcellno(coord,spacing) :
    return (750/spacing)*(int)(coord[1]/spacing)+coord[0]%spacing

def is_valid_coord(coord,snake_coords):
    if coord[0]<0 or coord[0]>750 or coord[1]<0 or coord[1]>600 :
        return False
    for coords in snake_coords :
        if coord==coords :
            return False
    return True
    
def get_random_snake(size):
    snake_coords=[]
    head=(15*(int)(random.randrange(0,750)/15),15*(int)(random.randrange(0,600)/15))
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
            return get_random_snake(size)
        next_coord=random.choice(possibles)
        snake_coords+=[next_coord]
        prev=next_coord
    return [snake_coords,gplib.makerandomtree(4,100)]

def change_canvas(snake,prev_snake_indices,food,spacing):
    for idx in prev_snake_indices :
        canvas.delete(idx)
    snakelogic=snake.get_snakelogic()
    snakeloc=snake.get_snakeloc()
    direction=tuple(map(operator.sub,snakeloc[0],snakeloc[1]))
    head=snakeloc[0]
    size=len(snakeloc)
    possible_moves=[(spacing,0),(0,-spacing),(-spacing,0),(0,spacing)]
    moves_available=[]
    neg_direction=tuple(map(operator.mul,direction,(-1,-1)))
    possible_moves.remove(neg_direction)
    move=(snakelogic.evaluate([snakeloc[0][0],snakeloc[0][1],food[0],food[1]]))%len(possible_moves)
    move_direction=possible_moves[move]
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
    snake[0]=snakeloc
    master.after(1000,change_canvas,snake,snake_indices,food,spacing)


def display_grid(w=500,h=500,spacing=25,food=(0,0),snake=get_random_snake(4)) :
    for i in range(0,w,spacing):
        canvas.create_line(i,0,i,h,fill='white')
    for i in range(0,h,spacing) :
        canvas.create_line(0,i,w,i,fill='white')
    canvas.create_oval(food[0]+1,food[1]+1,food[0]+spacing-1,food[1]+spacing-1,fill='yellow')
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
    master.after(1000,change_canvas,snake,snake_indices,food,spacing)
    master.mainloop()
            
    
#foodloc=(15*(int)(random.randrange(0,750)/15),15*(int)(random.randrange(0,600)/15))
#display_grid(w=750,h=600,spacing=15,food=foodloc,snake=get_random_snake(10))
