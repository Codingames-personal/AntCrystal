##
#%%

class EmptyQueue(Exception):
    pass

class FIFO:
    index_0 = 0
    index_1 = 0
    tab = []

    def __init__(self, tab : list = [], max_length=0):
        self.tab = tab
        self.index_0 = 0
        self.index_1 = len(tab) 
        self.length = len(tab)
        if max_length > len(tab):
            self.tab.extend([None]*(max_length-len(tab)))

    def __iter__(self):
        self.pointer = self.index_0
        return self
    
    def __next__(self):
        if self.pointer == self.index_1:
            raise StopIteration
        value = self.tab[self.pointer]
        self.pointer = (self.pointer+1)%len(self.tab)
        return value

    def add(self, e):
        self.length+=1
        if len(self.tab) == self.length:
            self.tab = self.tab[:self.index_1] + [None] + self.tab[self.index_1:]
            self.index_0 = (self.index_0+1)%len(self.tab)

        self.tab[self.index_1%len(self.tab)] = e
        self.index_1 = (self.index_1+1) % len(self.tab) 

    def push(self):
        """Del and return the first element of this list"""
        if self.length == 0:
            raise EmptyQueue("nothing to push")

        self.length-=1
        value = self.tab[self.index_0]
        self.index_0 = (self.index_0+1)%len(self.tab)
        return value

# Scare matrix
def path_to_graph(paths):
    graph = {}
    for path in paths:
        for i in range(len(path)-1):
            from_top = path[i]
            to_top = path[i+1]
            if graph.get(from_top):
                graph[from_top].append(to_top)
            else:
                graph[from_top] = [to_top]
            

def wide_route(matrix, id_father, function_per_level, filter):

    def recurrence(id, level):

        for id_child in matrix[id]:
            pass            


# %%
