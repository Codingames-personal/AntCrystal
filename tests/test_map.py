##
#%%

import unittest

from cell import Cell
from map import Map


flat_map = Map(
    number_of_cells=3,
    list_cell=[
        Cell(id=0, type_=0, resources=0, neighbors=[1, -1, -1, -1, -1, -1]), 
        Cell(id=1, type_=0, resources=0, neighbors=[2, -1, -1, 0, -1, -1]), 
        Cell(id=2, type_=2, resources=20, neighbors=[-1, -1, -1, 1, -1, -1])
        ],
    id_my_base=0,
    id_op_base=-1
    )


flat_map_middle = Map(
    number_of_cells=3,
    list_cell=[
        Cell(id=0, type_=2, resources=10, neighbors=[1, -1, -1, -1, -1, -1]), 
        Cell(id=1, type_=0, resources=0, neighbors=[2, -1, -1, 0, -1, -1]), 
        Cell(id=2, type_=2, resources=20, neighbors=[-1, -1, -1, 1, -1, -1])
        ],
    id_my_base=1,
    id_op_base=-1
    )

star_map_middle = Map(
    number_of_cells=7,
    list_cell=[
        Cell(id=0, type_=0, resources=0, neighbors=[1, 2, 3, 4, 5, 6]), 
        Cell(id=1, type_=2, resources=10, neighbors=[-1, -1, 2, 0, 6, -1]), 
        Cell(id=2, type_=2, resources=20, neighbors=[-1, -1, -1, 3, 0, 1]),
        Cell(id=3, type_=2, resources=20, neighbors=[2, -1, -1, -1, 4, 0]),
        Cell(id=4, type_=2, resources=20, neighbors=[0, 3, -1, -1, -1, 5]),
        Cell(id=5, type_=2, resources=20, neighbors=[6, 0, 4, -1, -1, -1]),
        Cell(id=6, type_=2, resources=20, neighbors=[-1, 1, 0, 5, -1, -1]),
        ],
    id_my_base=0,
    id_op_base=-1
    )


class TestMap(unittest.TestCase):

    def test_wide_route_level_calculation(self):
        flat_map.wide_route_level_calculation()
        self.assertEqual(
            flat_map.list_level, 
            [0, 1, 2]
        )

##
#%%
if __name__ == '__main__':
    unittest.main()