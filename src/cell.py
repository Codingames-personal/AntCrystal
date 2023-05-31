##
#%%
class Cell:
    id : int
    cell_type: int
    resources : int
    neighbors : list[int]
    my_ants = 0
    op_ants = 0
    
    def exist(id : int):
        return id >= 0

    def __init__(self, id : int, cell_type : int, resources : int, neighbors : int) -> None:
        self.id = id
        self.cell_type = cell_type
        self.resources = resources
        self.neighbors = neighbors

    def update(self, resources : int, my_ants : int, op_ants : int) -> None:
        self.resources = resources
        self.my_ants = my_ants
        self.op_ants = op_ants





# %%
