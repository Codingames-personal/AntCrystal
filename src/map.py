##
#%%
from cell import Cell
from tools import FIFO, path_to_graph
##
#%%

Matrix = list[list[int]]

class Map:
    number_of_cells : int
    cells : list[Cell]
    my_bases : list[int]
    op_bases : list[int]    
    levels : list[int]

    def __init__(self, number_of_cells : int, list_cell : list[Cell], my_bases : list[int], op_bases : list[int]) -> None:
        self.number_of_cells = number_of_cells
        self.list_cell = list_cell
        self.my_bases = my_bases
        self.op_bases = op_bases

        self.resources = [cell.index for cell in self.cells if cell.cell_type in [1, 2]]

        self.levels = [10**5]*number_of_cells
        for id_my_base in my_bases:
            queue = FIFO(tab=[id_my_base], max_length=100)
            levels_base = [-1]*number_of_cells
            levels_base[id_my_base] = 1
            while queue.length:
                for _ in range(queue.length):
                    id_father = queue.pop()
                    for id_child in self.cells[id_father].neighbors:
                        if levels_base[id_child] == -1: #Not init
                            levels_base[id_child] = levels_base[id_father] + 1
                            queue.push(id_child)


            for i, (l1, l2) in enumerate(zip(self.levels, levels_base)):
                self.levels[i] = min(l1, l2)
        

    def paths_update(self):
        self.paths = []
        for id_resource in self.resources:
            path = [id_resource]
            def recurrence(id, level):
                if level <= 0:
                    return self.paths.append(list(reversed(path)))
                for id_child in self.cells[id].neighbors:
                    if self.levels[id_child] < self.levels[id]:
                        path.append(id_child)
                        recurrence(id_child, self.levels[id_child])
                        path.pop()
            recurrence(id_resource, self.levels[id_resource])
        
    
        