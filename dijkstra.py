from heapq import *

class Data:
    
    def __init__(self, dist, index):
        self.dist, self.index = dist, index
        
    def __lt__(self, other):
        return self.dist < other.dist
    
    def __repr__(self):
        return str(self.dist)
    

def initDijkstra(width, height):
    global dists, used
    dists = [[10 ** 8] * height for _ in range(width)]
    used = [[False] * height for _ in range(width)]


def Dijkstra(begin, matrix):
    global dists, used    
    priorities = []
    dists[begin[0]][begin[1]] = 0
    heappush(priorities, Data(0, begin))
    while priorities:
        x = heappop(priorities)
        a, b = x.index
        if used[a][b]:
            continue
        used[a][b] = True
        for i in (-1, 0), (1, 0), (0, -1), (0, 1):
            try:
                assert a + i[0] != -1 and b + i[1] != -1
                to = (a + i[0], b + i[1])
                dist = matrix[to[0]][to[1]]
            except:                
                continue
            else:
                if not used[to[0]][to[1]] and dists[to[0]][to[1]] > dist + dists[a][b]:                    
                    dists[to[0]][to[1]] = dist + dists[a][b]
                    heappush(priorities, Data(dists[to[0]][to[1]], to))
    return dists