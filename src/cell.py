##
#%%
class Cell:
    id : int
    type_ : int
    resources : int
    neighbors : list
    my_ants = 0
    op_ants = 0
    
    def __init__(self, id : int, type_ : int, resources : int, neighbors : int) -> None:
        self.id = id
        self.type_ = type_
        self.resources = resources
        self.neighbors = neighbors

    def update(self, resources : int, my_ants : int, op_ants : int) -> None:
        self.resources = resources
        self.my_ants = my_ants
        self.op_ants = op_ants





# %%
