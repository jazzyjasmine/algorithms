import heapq
from typing import List
class Solution743:
    # 743. Network Delay Time
    # https://leetcode.com/problems/network-delay-time/
    """
    Dijkstra Algorithm
    
    O((V + E)lgV)
    
    """
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        key = {i: float("inf") for i in range(1, n + 1)}
        key[k] = 0
        
        visited = set()
        
        adjlist = self.get_adjlist(times)
        
        heap = [(0, k)]
        
        while heap:
            distance, node = heapq.heappop(heap)
            
            # Must do. Because heap in python does not have decrease_key method
            # (5, A) and (10, A) can both exist in the heap. We first pop (5, A)
            # and then pop (10, A), we should not use (10, A)
            
            # for Prim's algorithm, it does not run error if we omit this check,
            # because we don't use the information of the node in Prim's, instead
            # we only use the node itself. So the algorithm gets slower but no error
            if node in visited:
                continue
            
            visited.add(node)
            
            # for directed graph, a vertex with no out edges is not in adjlist
            # so we need to use adjlist.get(node, []) instead of adjlist[node]
            # for undirected graph, each edge has two directions, so every node
            # is in the adjlist
            for weight, neighbor in adjlist.get(node, []): 
                if neighbor in visited:
                    continue
                    
                if distance + weight < key[neighbor]:
                    key[neighbor] = distance + weight
                heapq.heappush(heap, (distance + weight, neighbor))
        
        return -1 if max(key.values()) == float("inf") else max(key.values())
    
    
    def get_adjlist(self, times):
        adjlist = {}
        for start, end, weight in times:
            if start in adjlist:
                adjlist[start].append((weight, end))
            else:
                adjlist[start] = [(weight, end)]
        return adjlist