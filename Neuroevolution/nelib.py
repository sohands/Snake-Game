# Board Width=300
# Board Height=300
# Cell Size=15x15
import random,numpy,math

def activation_function(x):
    return 1/(1+math.exp(-x))

def get_input(snakeloc=[],obstacles=[],foods=[]):
    board=[0]*900
    for loc in snakeloc:board[loc]=1
    for loc in obstacles:board[loc]=-1
    for loc in foods:board[loc]=2
    if len(snakeloc)>0:
        board[snakeloc[0]]=3
    return board

class Brain:
    def __init__(self,theta1,theta2):
        self.theta1=theta1
        self.theta2=theta2

    def getOutput(self,inp=get_input()):
        inp=[1]+inp
        hidden=[]
        output=[]
        for row in self.theta1:
            hidden_node_value=0
            for i in range(len(row)):
                hidden_node_value+=row[i]*inp[i]
            hidden+=[activation_function(hidden_node_value)]
        hidden=[1]+hidden
        for row in self.theta2:
            output_node_value=0
            for i in range(len(row)):
                output_node_value+=row[i]*hidden[i]
            output+=[activation_function(output_node_value)]
        out=(0 if output[0]>output[1] and output[0]>output[2] else (1 if output[1]>output[0] and output[1]>output[2] else 2))
        return out

def get_random_brain():
    theta1=numpy.random.rand(600,401)*1000
    theta2=numpy.random.rand(3,201)*1000
    return Brain(theta1,theta2)

class Snake:
    def __init__(self,snakebrain=None,snakeloc=[1,0]):
        if snakebrain is None :
            self.brain=get_random_brain()
        else :
            self.brain=snakebrain
        self.snakeloc=snakeloc

    def increaseSize(self):
        self.snakeloc.append(-1)

    def moveSnake(self,direction):
        diff=self.snakeloc[0]-self.snakeloc[1]
        for i in range(1,len(self.snakeloc)):
            self.snakeloc[i]=self.snakeloc[i-1]
        if diff is 1:
            if self.snakeloc[0]%20 is 19:self.snakeloc[0]=-1
        elif diff is -1:
            if self.snakeloc[0]%20 is 0:self.snakeloc[0]=-1
        elif diff is 20:
            if (int)(self.snakeloc[0]/20) is 0:self.snakeloc[0]=-1
        elif diff is -20:
            if (int)(self.snakeloc[0]/20) is 19:self.snakeloc[0]=-1
        if self.snakeloc[0] is not -1:self.snakeloc[0]=self.snakeloc[0]+diff
        
def mutate(snake):
    layer=random.choice([0,1])
    mutation=random.choice([0,1,2])
    if layer is 0:
        node1=random.choice(range(402))
        node2=random.choice(range(201))
        if mutation is 0:
            theta1[node2][node1]=random.random()*1000
        elif mutation is 1:
            for i in range(200):
                theta1[i][node1]=random.random()*1000
        elif mutation is 2:
            theta1[node2][node1]*=-1
    else:
        node1=random.choice(range(202))
        node2=random.choice(range(4))
        if mutation is 0:
            theta1[node2][node1]=random.random()*1000
        elif mutation is 1:
            for i in range(3):
                theta1[i][node1]=random.random()*1000
        elif mutation is 2:
            theta1[node2][node1]*=-1


def scorefunction(snake,obstacles,foods,moves=2500):
    score=0
    foodindex=0
    food=foods[foodindex]
    for move in range(moves):
        snake.moveSnake(snake.brain.getOutput(get_input(snake.snakeloc,obstacles,[food])))
        if snake.snakeloc[0] is -1:
            return score
        elif snake.snakeloc[0] is food:
            score+=10000
    return score

def evolve(popsize,maxgen,moves=2500):
    population=[Snake() for i in range(popsize)]
    for gen in range(maxgen):
        foods=[random.choice(range(401)) for i in range(moves)]
        scores=[scorefunction(snake,[],foods,moves) for snake in population]
        del foods
        scores.sort()
        scores.reverse()
        print scores[0]


evolve(750,1)
