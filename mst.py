import heapq

class Solution:
    """
    Minimum Spanning Tree (MST)

    Kruskal's algorithm

    Time complexity: O(ElgV)
    """
    # 1584. Min Cost to Connect All Points
    def minCostConnectPointsKruskal(self, points: List[List[int]]) -> int:
        res = 0
        
        parents, ranks = self.makeset(len(points))
        
        edges = self.get_all_edges(points)
        edges.sort()
        
        for edge in edges:
            weight, u, v = edge[0], edge[1], edge[2]
            u_root = self.find(parents, u)
            v_root = self.find(parents, v)
            if u_root != v_root:
                res += weight
                self.union(u_root, v_root, parents, ranks)
        
        return res
    
    
    def union(self, x, y, parents, ranks):
        if ranks[x] > ranks[y]:
            parents[y] = x
        else:
            parents[x] = y
            if ranks[x] == ranks[y]:
                # increase rank only when ties
                ranks[y] += 1
            
    
    def find(self, parents, node):
        while parents[node] != node:
            node = parents[node]
        return node
        
    
    def makeset(self, n):
        return [i for i in range(n)], [0 for i in range(n)]
    
    
    def get_all_edges(self, points):
        edges = []
        n = len(points)
        for i in range(n):
            for j in range(i + 1, n):
                weight = self.get_manhattan_distance(i, j, points)
                edges.append((weight, i, j))
        return edges
    

    """
    Minimum Spanning Tree (MST)

    Prim's algorithm

    Time complexity: O((V + E)lgV) = O(ElgV)
    """
    # 1584. Min Cost to Connect All Points
    def minCostConnectPointsPrim(self, points: List[List[int]]) -> int:
        n = len(points)
        
        # key: node, value: min weight of edge connecting node to current mst
        key = {i: float("inf") for i in range(n)}
        key[0] = 0
        
        # nodes popped out from heap = visited = nodes in current mst
        mst = set()
        
        # initiate the heap
        heap = [(0, 0)]
        
        while heap:
            # get the node with min weight to current mst and add it to mst (cut property)
            # we can also use an int variable to collect the "_" as the return result 
            _, node = heapq.heappop(heap)
            mst.add(node)
            
            # iterate through neighbors of node
            # this is a complete graph so we don't need adj list here
            for neighbor in range(n):
                if neighbor in mst:
                    continue
                
                # get w(node, neighbor), i.e. weight of the edge(node, neighbor)
                weight_to_node = self.get_manhattan_distance(neighbor, node, points)
                
                # update(decrease) the key of neighbor if needed 
                # key[neighbor] stores the neighbor's min weight to the previous mst
                # now we add node to previous mst, so key[neighbor] might change 
                # if w(node, neighbor) is smaller than the min weight to the previous mst
                # w(node, neighbor) then becomes the new min weight
                if weight_to_node < key[neighbor]:
                    key[neighbor] = weight_to_node
                    # decrease key
                    heapq.heappush(heap, (weight_to_node, neighbor))
        
        # key.values() stores all weights in the final mst
        return sum(key.values())
                  
    
    def get_manhattan_distance(self, i, j, points):
        return abs(points[i][0] - points[j][0]) + abs(points[i][1] - points[j][1])