


memorylength=10
depth=20
inputsize=5



memory=[0]*memorylength
snakeinp=[]
loopvar=[None,-1]


class fwrapper :
    def __init__(self,function,childcount):
        self.function=function
        self.childcount=childcount


class node :
    def __init__(self,fw,children):
        self.function=fw.function
        self.children=children

    def evaluate(self):
        results=[n.evaluate() for n in self.children]
        return self.function(results)


class valnode :
    def __init__(self,string):
        self.string=string

    def evaluate(self):
        c=self.string[0]
        if c is 'p':return snakeinp[int(self.string[1:])]
        elif c is 'c':return int(self.string[1:])
        elif c is 'm':return memory[int(self.string[1:])]


class loopnode :
    def __init__(self,condnode,execnode,exitnode):
        self.condnode=condnode
        self.execnode=execnode
        self.exitnode=exitnode

    def evaluate(self):
        condition=self.condnode.evaluate()
        while condition is True:
            self.execnode.evaluate()
            condition=self.condnode.evaluate()
        self.exitnode.evaluate()
            



def add(l):
    return l[0]+l[1]
addw=fwrapper(add,2)

def subtract(l):
    return l[0]-l[1]
subw=fwrapper(subtract,2)

def multiply(l):
    return l[0]*l[1]
mulw=fwrapper(multiply,2)

def divide(l):
    if l[1] is 0:
        return 0
    return l[0]/l[1]
divw=fwrapper(divide,2)

def modulo(l):
    if l[1] is 0:
        return l[0]
    return l[0]%l[1]
modw=fwrapper(modulo,2)

def iffunc(l):
    if l[0] is True:
        return l[1]
    return l[2]
ifw=fwrapper(iffunc,3)


def looplistcond(l):
    if loopvar[0] is None:
        loopvar[0]=l[0]
        loopvar[1]=0
        return True
    elif loopvar[1]==len(l):
        loopvar[0]=None
        loopvar[1]=-1
        return False
    else:
        loopvar[1]+=1
        loopvar[0]=l[loopvar[1]]
        return True

def greater(l):
    return l[0]>l[1]

def negation(l):
    return !l[0]

def equal(l):
    return l[0]==l[1]

def andfunc(l):
    return l[0] and l[1]

def orfunc(l):
    return l[0] or l[1]

    
