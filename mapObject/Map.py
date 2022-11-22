import numpy as np
from mapObject.Wall import Wall


class Map:
    def __init__(self):
        self.map = np.zeros((241,241),dtype=np.int64)
