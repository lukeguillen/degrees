from util import Node, StackFrontier, QueueFrontier

class Searcher():
    def __init__(self,borderline):
        self.searcher_frontier=borderline
        self.visited=[]
        
    """ recibe a Node"""

    def add_visited(self,Node):
        self.visited.append(Node)
        
    def is_visited (self,option):
        answer=False
        for visited_node in self.visited:
            for state in visited_node.state:
                if state==option:
                    answer=True
        return answer
    
    def push_in_frontier(self, expanded_frontier):
        #by each element in source, to convert to Node and add to list
        #print(expanded_frontier)
        for option in expanded_frontier:
            self.searcher_frontier.frontier.append(option)

    def pop_frontier(self):
        node=self.searcher_frontier.remove()
        return node
        
    def is_goal(self,target,Node):
        answer= False
        if target in Node.state:
            answer=True
        return answer
    
    def frontier_is_empty(self):
        return self.searcher_frontier.empty()
    
    def neighbors_to_nodes(self,neighbors):
        pass
    