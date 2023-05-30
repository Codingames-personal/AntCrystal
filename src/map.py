##
#%%
from cell import Cell

##
#%%

Matrix = list[list[int]]

class Map:
    number_of_cells : int
    list_cell : list[Cell]
    id_my_base : int
    id_op_base : int
    sink : Cell
    capacity : Matrix
    adjancy_matrix : Matrix
    list

    def __init__(self, number_of_cells : int, list_cell : list[Cell], id_my_base : int, id_op_base : int) -> None:
        self.number_of_cells = number_of_cells
        self.list_cell = list_cell
        self.id_my_base = id_my_base
        self.id_op_base = id_op_base
        
        self.sink = Cell(number_of_cells, -1, 0, [])
        self.adjancy_matrix = [[-1]*6 for _ in range(number_of_cells)]
        self.capacity = [[0]*6 for _ in range(number_of_cells+1)]
        self.paths = []
        self.list_level = [-1]*self.number_of_cells
        self.list_cell_resources = []
        self.list_capacities = []
        self.number_ants = 0

        for cell in self.list_cell:
            
            for labelle, neighbor_id in enumerate(cell.neighbors):
                self.adjancy_matrix[cell.id][labelle] = neighbor_id 
            
            if cell.type_ == 2:
                self.sink.neighbors.append(cell.id)
                self.list_cell_resources.append(cell.id)
                
        self.wide_route_level_calculation()
        self.in_depth_route_potential_path()


    """def wide_route_cell(self, 
            id_father,
            function_per_level : function = lambda x : x,
            filter : function = lambda **kargs : True, 
            **kargs
            ):
        already_past = [False]*self.number_of_cells
        already_past[id_father] = True

        def recurrence(id, level):
            already_past[id] = True
            done = True
            for id_child in self.list_cell[id].neighbors:
                if not already_past[id_child] and filter(**kargs):
                    done = False
                    function_per_level(**kargs)

            if not done:
                for id_child in self.list_cell[id].neighbors:
                    if not already_past[id_child]:
                        recurrence(level+1)"""


    def update(self):
        self.number_ants = 0
        for cell in self.list_cell:
            resources, my_ants, op_ants = list(map, input().split())  
            cell.update(resources, my_ants, op_ants)
            self.number_ants += my_ants
            
    def play(self):
        pass

    def wide_route_level_calculation(self):
        list_id_father = [self.id_my_base]
        already_past = [False]*self.number_of_cells
        already_past[self.id_my_base] = True
        self.list_level[self.id_my_base] = 0
        level = 1
        while list_id_father:
            new_list_id_father = []
            for id_father in list_id_father:
                for id_child in self.list_cell[id_father].neighbors:
                    if not(id_child == -1 or already_past[id_child]):
                        self.list_level[id_child] = level
                        new_list_id_father.append(id_child)
                        already_past[id_child] = True
            list_id_father = new_list_id_father[:]
            level +=1

    def in_depth_route_potential_path(self):
        self.paths = [[]]
        for id_father in self.list_cell_resources:
            already_past = [False]*self.number_of_cells
            def recurrence(id, level):
                if level == 0:
                    print(*self.paths[-1])
                    self.paths.append([])
                else:
                    already_past[id] = True
                    for id_child in self.list_cell[id].neighbors:
                        if not already_past[id_child] and self.list_level[id_child] < level:
                            self.paths[-1].append(id_child)
                            recurrence(id_child, level-1)
            recurrence(id_father, self.list_level[id_father])
        

    def wide_route_capacity_calculation(self):
        already_past = [False]*self.number_of_cells
        
        def recurrence(id, level):
            done = True
            for labelle, id_child in enumerate(self.list_cell[id].neighbors):
                if not id_child == -1 and not already_past[id_child]:
                    done = False
                    self.capacity[id][labelle] = self.number_ants/level

            if not done:
                for id_child in self.list_cell[id].neighbors:
                    if not already_past[id_child]:
                        recurrence(id_child, level+1)
                        already_past[id_child] = True

        already_past[self.id_my_base] = True
        recurrence(self.id_my_base, 1)


    def capacity_update(self):
        for index, cell_resources in enumerate(self.list_cell_resources):
            if not cell_resources.resource:
                del self.list_cell_resources[index]
                continue

            self.capacity[self.sink.id][cell_resources.id] = cell_resources.resources
            self.capacity[cell_resources.id][self.sink.id] = cell_resources.resources


    def verification_map(self):
        oppose = lambda x : (x+3)%6
        for cell in self.list_cell:
            for labelle, neighbor_id in enumerate(cell.neighbors):
                if not neighbor_id == -1:
                    neighbor = self.list_cell[neighbor_id]
                    if not neighbor.neighbors[oppose(labelle)] == cell.id:
                        print("ERROR : cell {} | neighbor {}".format(cell.id, neighbor_id))
                        return False
        return True


    def find_potential_path(self):
        pass

    def update(self, list_cell_value : list[Cell]) -> None:
        for cell, cell_value in zip(self.list_cell, list_cell_value):
            cell.update(*cell_value)

        

# %%
