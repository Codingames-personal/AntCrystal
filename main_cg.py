import sys
import random
import numpy
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

    def push(self, e):
        self.length+=1
        if len(self.tab) == self.length:
            self.tab = self.tab[:self.index_1] + [None] + self.tab[self.index_1:]
            self.index_0 = (self.index_0+1)%len(self.tab)

        self.tab[self.index_1%len(self.tab)] = e
        self.index_1 = (self.index_1+1) % len(self.tab) 

    def pop(self):
        """Del and return the first element of this list"""
        if self.length == 0:
            raise EmptyQueue()

        self.length-=1
        value = self.tab[self.index_0]
        self.index_0 = (self.index_0+1)%len(self.tab)
        return value

class Cell(object):
    index: int
    cell_type: int
    resources: int
    neighbors: list[int]
    my_ants: int
    opp_ants: int

    def __init__(self, index: int, cell_type: int, resources: int, neighbors: list[int], my_ants: int, opp_ants: int):
        self.index = index
        self.cell_type = cell_type
        self.resources = resources
        self.neighbors = neighbors
        self.my_ants = my_ants
        self.opp_ants = opp_ants

    def __str__(self):
        return str(self.index)


cells: list[Cell] = []
number_of_cells = int(input())  # amount of hexagonal cells in this map
for i in range(number_of_cells):
    inputs = [int(j) for j in input().split()]
    cell_type = inputs[0] # 0 for empty, 1 for eggs, 2 for crystal
    initial_resources = inputs[1] # the initial amount of eggs/crystals on this cell
    neigh_0 = inputs[2] # the index of the neighbouring cell for each direction
    neigh_1 = inputs[3]
    neigh_2 = inputs[4]
    neigh_3 = inputs[5]
    neigh_4 = inputs[6]
    neigh_5 = inputs[7]
    cell: Cell = Cell(
        index = i,
        cell_type = cell_type,
        resources = initial_resources,
        neighbors = list(filter(lambda id: id > -1,[neigh_0, neigh_1, neigh_2, neigh_3, neigh_4, neigh_5])),
        my_ants = 0,
        opp_ants = 0
    )
    cells.append(cell)


number_of_bases = int(input())
my_bases: list[int] = []
for i in input().split():
    my_base_index = int(i)
    my_bases.append(my_base_index)
opp_bases: list[int] = []
for i in input().split():
    opp_base_index = int(i)
    opp_bases.append(opp_base_index)


list_level = [10**5]*number_of_cells
for id_my_base in my_bases:
    queue = FIFO(tab=[id_my_base], max_length=100)
    list_level_base = [-1]*number_of_cells
    list_level_base[id_my_base] = 0
    while queue.length:
        for _ in range(queue.length):
            id_father = queue.pop()
            for id_child in cells[id_father].neighbors:
                if list_level_base[id_child] == -1: #Not init
                    list_level_base[id_child] = list_level_base[id_father] + 1
                    queue.push(id_child)


    for i, (l1, l2) in enumerate(zip(list_level, list_level_base)):
        list_level[i] = min(l1, l2)


def in_depth_route_potential_path(resources_cells):
    """Find all the path that leads to a sources cell"""
    paths = []
    for id_resource in resources_cells:
        path = [id_resource]
        def recurrence(id, level):
            if level <= 0:
                return paths.append(list(reversed(path)))
            for id_child in cells[id].neighbors:
                if list_level[id_child] < list_level[id]:
                    path.append(id_child)
                    recurrence(id_child, list_level[id_child])
                    path.pop()
        recurrence(id_resource, list_level[id_resource])
    return paths

def choose_cells(paths):
    resource_cells = []
    for path in paths:
        if not path[-1]in resource_cells: resource_cells.append(path[-1])
    strenght_cells = [[0] for _ in range(number_of_cells)]
    #Calculate the strenght of each cell
    for path in paths:
        resource_cell = cells[path[-1]]
        strenght_ = strenght(resource_cell)

        for cell_id in path:
            strenght_cells[cell_id][0] += strenght_ 
            strenght_cells[cell_id].append(strenght_)
    strenght_paths = {}
    #Calculate the strenght of each path
    for index, path in enumerate(paths):
        strenght_path = sum(
            [strenght_cells[cell_id][0]+cells[cell_id].my_ants for cell_id in path]
        )
        strenght_paths[strenght_path] = index
    
    #Create a cumulativ sum with the strenght of each path
    total_sum = sum(strenght_paths.keys())
    cumulative_sum = [[0,0]]
    for strenght_, index in sorted(strenght_paths.items()):
        cumulative_sum.append(
            [cumulative_sum[-1][0]+strenght_/total_sum, index]
        )
    
    #Choose the best paths
    resources_already_past = [False]*number_of_cells
    chosen_paths = []
    for prob, index in reversed(cumulative_sum):
        if prob < 1-1/len(paths):
            break
        path = paths[index]
        if not resources_already_past[path[-1]]:
            chosen_paths.append(path)
            resources_already_past[path[-1]] = True
    already_past = [False]*number_of_cells
    for path in chosen_paths:
        for cell_id in path:
            if not already_past[cell_id]:
                yield [cell_id, round(min(strenght_cells[cell_id]))]
                already_past[cell_id] = True


number_of_crystals = 0
number_of_eggs = 0

number_of_ants = 0
print("List level :", *list_level, file=sys.stderr)
max_level = max(list_level)
# game loop
while True:
    cells_resources : list[Cell] = []

    for i in range(number_of_cells):
        inputs = [int(j) for j in input().split()]
        resources = inputs[0] # the current amount of eggs/crystals on this cell
        my_ants = inputs[1] # the amount of your ants on this cell
        opp_ants = inputs[2] # the amount of opponent ants on this cell
        number_of_ants += my_ants
        if cells[i].cell_type == 1:
            number_of_eggs += resources
        else:
            number_of_crystals += resources
        cells[i].resources = resources
        cells[i].my_ants = my_ants
        cells[i].opp_ants = opp_ants
        if resources:
            cells_resources.append(cells[i])

    # WAIT | LINE <sourceIdx> <targetIdx> <strength> | BEACON <cellIdx> <strength> | MESSAGE <text>
    crystal_egg_ratio = number_of_crystals/(number_of_crystals+number_of_eggs)
    
    def strenght(resource_cell): 
        if number_of_eggs and resource_cell.cell_type == 1:#eggs
            ratio = numpy.exp(max_level)*(100+resource_cell.resources)*crystal_egg_ratio
        elif number_of_crystals:
            ratio = numpy.exp(max_level)*number_of_ants*resource_cell.resources*(1-crystal_egg_ratio)
        else:
            ratio = 1
        return ratio/list_level[resource_cell.index]

    chosen_cells = choose_cells(
        in_depth_route_potential_path([cell.index for cell in cells_resources])
    )
    #print("Chosen cells : " ,*chosen_cells, file=sys.stderr)
    actions = ["BEACON {} {}".format(cell_id, strenght_)
        for cell_id, strenght_ in chosen_cells
    ]
    # TODO: choose actions to perform and push them into actions
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)
    
    if len(actions) == 0:
        print('WAIT')
    else:
        print(';'.join(actions))