import heapq
 
class PriorityQueue(object):
    """Priority queue based on heap, capable of inserting a new node with
    desired priority, updating the priority of an existing node and deleting
    an abitrary node while keeping invariant"""
 
    def __init__(self, heap=[]):
        """if 'heap' is not empty, make sure it's heapified"""
 
        heapq.heapify(heap)
        self.heap = heap
        self.entry_finder = dict({i[-1]: i for i in heap})
        self.REMOVED = '<remove_marker>'
 
    def insert(self, node, priority=0):
        """'entry_finder' bookkeeps all valid entries, which are bonded in
        'heap'. Changing an entry in either leads to changes in both."""
 
        if node in self.entry_finder:
            self.delete(node)
        entry = [priority, node]
        self.entry_finder[node] = entry
        heapq.heappush(self.heap, entry)
 
    def delete(self, node):
        """Instead of breaking invariant by direct removal of an entry, mark
        the entry as "REMOVED" in 'heap' and remove it from 'entry_finder'.
        Logic in 'pop()' properly takes care of the deleted nodes."""
 
        entry = self.entry_finder.pop(node)
        entry[-1] = self.REMOVED
        return entry[0]
 
    def pop(self):
        """Any popped node marked by "REMOVED" does not return, the deleted
        nodes might be popped or still in heap, either case is fine."""
 
        while self.heap:
            priority, node = heapq.heappop(self.heap)
            if node is not self.REMOVED:
                del self.entry_finder[node]
                return priority, node
        raise KeyError('pop from an empty priority queue')

    def __len__(self):
        return len(self.heap)


def dijkstra(source, edges):
    """Returns the shortest paths from the source to all other nodes.
    'edges' are in form of {head: [(tail, edge_dist), ...]}, contain all
    edges of the graph, both directions if undirected."""
 
    shortest_path = {i: [float("inf"), None] for i in edges}
    shortest_path[source] = [0, source]

    pq = PriorityQueue([[float("inf"), i] for i in edges if i != source])
    pq.insert(source)

    while len(pq):
        min_dist, new_node = pq.pop()
        shortest_path[new_node][0] = min_dist
        for tail, edge_dist in edges[new_node]:
            new_dist = min_dist + edge_dist
            if new_dist < shortest_path[tail][0]:
                shortest_path[tail][0] = new_dist
                shortest_path[tail][1] = new_node
                pq.insert(tail, new_dist)
    return shortest_path
