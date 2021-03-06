import heapq

class Solution1584:
    # 1584. Min Cost to Connect All Points
    """
    Minimum Spanning Tree (MST)

    Kruskal's algorithm

    Time complexity: O(ElgV)
    """
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
            
    # see a revised version of find in Boruvka's algorithm
    # def find(self, parents, node):
    #     while parents[node] != node:
    #         node = parents[node]
    #     return node
        
    
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

            if node in mst:
                continue

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


    """
    Minimum Spanning Tree (MST)

    Boruvka's algorithm

    O((V+E)lgV) = O(ElgV)

    Reference: https://www.geeksforgeeks.org/boruvkas-algorithm-greedy-algo-9/
    """
    def minCostConnectPointsBoruvka(self, points: List[List[int]]) -> int:
        n = len(points)
        
        parents, ranks = self.makeset(n)
        edges = self.get_all_edges(points)
        
        # store the min edge with one endpoint in the connected component
        # rooted in "index", and one endpoint outside the connected component
        min_edges = [-1 for i in range(n)]
        
        # the number of trees is n initially, treat each vertex as a tree
        tree_num = n
        
        # the sum of weight in mst
        mst_weight = 0
        
        # loop until we only have one tree, which is the mst
        while tree_num > 1:
            # iterate through all edges
            for (weight, i, j) in edges:
                # find the root of the connected component that i is in
                i_root = self.find(parents, i)
                # find the root of the connected component that j is in
                j_root = self.find(parents, j)
                
                # if the edge does not make a cycle, i.e. endpoints
                # are in different connected components
                if i_root != j_root:
                    # maintain the min_edges by updating
                    # update only at start or the new edge's weight is less than the existed weight
                    if min_edges[i_root] == -1 or min_edges[i_root][0] > weight:
                        min_edges[i_root] = (weight, i, j)
                    
                    if min_edges[j_root] == -1 or min_edges[j_root][0] > weight:
                        min_edges[j_root] = (weight, i, j)
            
            # iterate through all vertices
            # connect the current connected components by the min_edge of their roots
            # for a connected component, use the min_edge of its root (min_edges[root]) to connect
            # to another connected component and thus decrease the number of trees (connected components)
            for node, min_edge in enumerate(min_edges):
                # if the node is not a root, ignore
                if min_edge == -1:
                    continue
                    
                weight, i, j = min_edge[0], min_edge[1], min_edge[2]
                
                i_root = self.find(parents, i)
                j_root = self.find(parents, j)
                
                # need to check if the roots are the same because the edge might already be used by a previous vertex
                # if so, the current node is already in the same connected component with the previous vertex (the other endpoint of the edge)
                # example: {(0,1,4),(3,1,3),(2,1,9),(0,2,13),(2,3,10),(0,3,7)} format: (u,v,weight)
                # node 1 and node 3 have the same min_edge
                if i_root != j_root:
                    self.union(i_root, j_root, parents, ranks)
                    mst_weight += weight
                    # decrease the number of trees after each union behavior
                    tree_num -= 1
            
            # IMPORTANT: clean up the min_edges
            min_edges = [-1 for i in range(n)]
            
        return mst_weight
            
    
    def find(self, parents, node):
        while parents[node] != node:
            parents[node] = parents[parents[node]]  # reduce the time complexity for find to O(1)
            node = parents[node]
        return node


class Solution1135:
    # 1135. Connecting Cities With Minimum Cost
    """
    Kruskal's algorithm
    """
    def minimumCostKruskal(self, n: int, connections: List[List[int]]) -> int:
        parents, ranks = self.makeset(n)
        
        connections.sort(key=lambda x: x[2])
        
        mst_weight = 0
        
        for u, v, weight in connections:
            u_root = self.find(u, parents)
            v_root = self.find(v, parents)
            if u_root != v_root:
                mst_weight += weight
                self.union(u_root, v_root, parents, ranks)
            
        root_num = len([i for i in parents if parents[i] == i])
        
        return mst_weight if root_num == 1 else -1
        
    def makeset(self, n):
        return {i: i for i in range(1, n + 1)}, {i: 0 for i in range(1, n + 1)}
    
    def find(self, u, parents):
        while parents[u] != u:
            parents[u] = parents[parents[u]] # make find O(1) run time
            u = parents[u]
        return u
    
    def union(self, u_root, v_root, parents, ranks):
        if ranks[u_root] < ranks[v_root]:
            parents[u_root] = v_root
        else:
            parents[v_root] = u_root
            if ranks[u_root] == ranks[v_root]:
                ranks[u_root] += 1
    
    """
    Prim's algorithm
    """
    def minimumCost(self, n: int, connections: List[List[int]]) -> int:
        key = {i: float("inf") for i in range(1, n + 1)}
        key[1] = 0
        
        mst = set()
        
        adjlist = self.get_adjlist(connections)
        
        heap = [(0, 1)]
        
        while heap:
            min_weight, node = heapq.heappop(heap)
            if node in mst:
                continue
            mst.add(node)

            for neighbor, edge_weight in adjlist[node]:
                if neighbor in mst:
                    continue
                    
                if edge_weight < key[neighbor]:
                    key[neighbor] = edge_weight
                heapq.heappush(heap, (key[neighbor], neighbor))
            
        return sum(key.values()) if len(mst) == n else -1
           
    
    def get_adjlist(self, connections):
        adjlist = {}
        for u, v, weight in connections:
            self.add_to_adjlist(adjlist, u, v, weight)
            self.add_to_adjlist(adjlist, v, u, weight)
        return adjlist
    
    
    def add_to_adjlist(self, adjlist, u, v, weight):
        if u in adjlist:
            adjlist[u].append((v, weight))
        else:
            adjlist[u] = [(v, weight)]