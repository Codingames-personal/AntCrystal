
def wide_route(matrix, id_father, function_per_level, filter):


    def recurrence(id, level):

        for id_child in matrix[id]:
            