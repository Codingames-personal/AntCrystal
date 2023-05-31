##
#%%
from cell import Cell
from map import Map
from src.cell import Cell
import numpy
##
#%%

class score(Map):
    number_of_ants = 0
    number_of_eggs = 0
    number_of_crystals = 0

    def __init__(self, number_of_cells: int, list_cell: list[Cell], my_bases: list[int], op_bases: list[int]) -> None:
        super().__init__(number_of_cells, list_cell, my_bases, op_bases)
        self.max_level = max(self.levels)
        
    def updatde(self, new_cells):
        self.actions = []
        self.resources = []
        self.number_of_ants = 0
        for i, (resources, my_ants, op_ants) in enumerate(new_cells):
            self.cells[i].resources = resources
            self.cells[i].my_ants = my_ants
            self.cells[i].op_ants = op_ants

            self.number_of_ants+=my_ants
            if self.cells[i].cell_type:
                if self.cells[i].cell_type == 1:
                    self.number_of_eggs+=resources
                elif self.cells[i].cell_type == 2:
                    self.number_of_crystals+=resources
                self.resources.append(self.cells[i])
                
        self.paths_update()

    def strenght(self, resource_cell : Cell) -> float:
        crystal_egg_ratio = self.number_of_crystals/(self.number_of_crystals+self.number_of_eggs)
        if self.number_of_eggs and resource_cell.cell_type == 1:#eggs
            ratio = numpy.exp(self.max_level)*(100+resource_cell.resources)*crystal_egg_ratio
        elif self.number_of_crystals:
            ratio = numpy.exp(self.max_level)*self.number_of_ants*resource_cell.resources*(1-crystal_egg_ratio)
        else:
            ratio = 1
        return ratio/self.levels[resource_cell.index]


    def strenght_cells_generator(self):
        """Calculate the strenght of each cell"""
        self.strenght_cells = [[0] for _ in range(self.number_of_cells)]

        for path in self.paths:
            resource_cell = self.cells[path[-1]]
            strenght_ = self.strenght(resource_cell)

            for cell_id in path:
                self.strenght_cells[cell_id][0] += strenght_ 
                self.strenght_cells[cell_id].append(strenght_)

    def strenght_paths_generator(self):
        self.strenght_paths = {}
        #Calculate the strenght of each path
        for index, path in enumerate(self.paths):
            strenght_path = sum(
                [self.strenght_cells[cell_id][0]+self.cells[cell_id].my_ants for cell_id in path]
            )
            self.strenght_paths[strenght_path] = index
        
    def chose_best_paths(self):
        """
        Choose the best paths thanks to the cell's strenght
        and recalculate a new strenght for those cells
        """
        #Create a cumulativ sum with the strenght of each path
        total_sum = sum(self.strenght_paths.keys())
        cumulative_sum = [[0,0]]
        for strenght_, index in sorted(self.strenght_paths.items()):
            cumulative_sum.append(
                [cumulative_sum[-1][0]+strenght_/total_sum, index]
            )
        #Choose the best paths
        resources_already_past = [False]*self.number_of_cells
        chosen_paths = []
        for prob, index in reversed(cumulative_sum):
            if prob < 1-1/len(self.paths):
                break
            path = self.paths[index]
            if not resources_already_past[path[-1]]:
                chosen_paths.append(path)
                resources_already_past[path[-1]] = True
        
        self.chosen_cells = []
        already_past = [False]*self.number_of_cells
        for path in chosen_paths:
            for cell_id in path:
                if not already_past[cell_id]:
                    self.chosen_cells.append([cell_id, round(min(self.strenght_cells[cell_id]))])
                    already_past[cell_id] = True



    def action_generator(self):
        self.strenght_cells_generator()
        self.strenght_paths_generator()
        self.chose_best_paths()
        self.actions = ["BEACON {} {}".format(cell_id, strenght_)
            for cell_id, strenght_ in self.chosen_cells
        ]


    def cells_scoring(self):
        self.paths_update()

    def output(self):
        self.action_generator()
        if self.actions:
            print(";".join(self.actions))
        else:
            print("WAIT")