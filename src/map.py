from src.cell import Cell
import numpy


Matrix = list[list[int]]

class Map:
    number_of_cells : int
    list_cell : list[Cell]
    id_my_base : int
    id_op_base : int
    well : Cell
    flow : list[0]
    capacity : Matrix
    adjancy_matrix : Matrix
    list

    def __init__(self, number_of_cells : int, list_cell : list[Cell], id_my_base : int, id_op_base : int) -> None:
        self.number_of_cells = number_of_cells
        self.list_cell = list_cell
        self.id_my_base = id_my_base
        self.id_op_base = id_op_base
        
        self.well = Cell(number_of_cells, -1, 0, [])
        self.adjancy_matrix = [[-1]*6]*number_of_cells
        self.flow = [-1]*number_of_cells
        self.capacity = [[0]*6]*(number_of_cells+1) 
        self.list_cell_resources = []
        self.number_ants = 0

        for cell in self.list_cell:
            
            for labelle, neighbor_id in enumerate(cell.neighbors):
                self.adjancy_matrix[cell.id][labelle] = neighbor_id 
            
            if cell.type_ == 2:
                self.well.neighbors.append(cell.id)
                self.list_cell_resources.append(cell.id)
                self.capacity[self.well.id][cell.id] = cell.resources
                self.capacity[cell.id][self.well.id] = cell.resources
            
          


            self.wide_route_capacity_calculation()

            
        

    def wide_route_capacity_calculation(self):
        already_past = [False]*self.number_of_cells
        already_past[self.id_my_base] = True
        stack = [[self.id_my_base, 0]]
        id_stack = 0
        
        while id_stack == len(stack):
            id_father, level = stack[id_stack]
            
            id_stack +=1
            for id_child in self.list_cell[id_father]:
                if filter(id_child) and not already_past[id_child]:
                    self.capacity[id_child][id_father] = level
                    self.capacity[id_father][id_child] = level
                    
                    stack.append([id_child, level+1])
                    already_past[id_child] = True






    def capacity_calculation(self):
        for cell in self.list_cell:



    def update(self, list_cell_value : list[Cell]) -> None:
        for cell, cell_value in zip(self.list_cell, list_cell_value):
            cell.update(*cell_value)

        
