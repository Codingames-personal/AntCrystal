##
#%%
from cell import Cell
from map import Map
##
#%%



class flow(Map):
    
    graph : list[list[int]] #graph[i][j] -> from i to j exist
    capacities : list[dict[int, int]] #capacities[i][j] -> c(i, j)
    index_cells : list[int]
    source : Cell #virtual cell that represent the final source of resources
    base : Cell #virtual cell that represent the final base
    

    def __init__(self, **kargs):
        super().__init__(self, **kargs)
        
        source = Cell(self.number_of_cells, 0, 0, self.resources)
        base = Cell(self.number_of_cells+1, 0, 0, self.my_bases)
        #graph generated from self.paths : only the cell that appears in the paths are interesting
        self.graph = [[] for _ in range(self.number_of_cells+2)]
        self.flow = [[] for _ in range(self.number_of_cells+2)]

        for id_base in self.my_bases:
            self.graph[base.index].append(id_base)
        for source_paths in self.paths:
            self.graph[source_paths[0][-1]].append(source.index)
            for path in source_paths:
                for i in range(len(path)-1):
                    from_vertices = path[i]
                    to_vertices = path[i+1]
                    if not to_vertices in self.graph[from_vertices]:
                        self.graph.append(to_vertices)

        self.capacities = [{} for _ in range(self.number_of_cells)]


    def capacities_calculation(self, number_of_ants):
        #capacities generated from graph
        for from_vertice, edges  in enumerate(self.graph):
            for to_vertice in edges:
                self.capacities[from_vertice][to_vertice] = number_of_ants/self.levels[to_vertice]
        
        for resource in self.resources:
            self.capacities[resource][self.source.index] = self.cells[resource].resources

        for base in self.my_bases:
            self.capacities[self.base.index][base] = number_of_ants


    def flow(self):
        
