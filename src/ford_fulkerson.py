
Graph = dict[int, list[int]]


class ford_fulkerson:
    
    graph : Graph
    capacity : list[dict[int, float]]

    source : int
    sink : int
    flow_number : int

    def __init__(self, graph : dict[int, list[int]], capacity : list[dict[int, float]], source : int, sink : int, flow_number : int) -> None:
        self.graph = graph
        self.capacity = capacity
        self.source = source
        self.sink = sink
        self.flow_number = flow_number
        self.flow = [0]*len(self.capacity)
        
    def initiate_first_flow(self):

        def recurrence(id):
            if id == self.sink:
                pass
            else:
                