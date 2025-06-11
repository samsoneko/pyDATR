def build_theory(parsed_datr):
    theory = Theory("default", parsed_datr)
    return theory

class Theory(object):
    def __init__(self, name, parsed_datr):
        self.name = name
        self.nodes = []
        for entry in parsed_datr:
            if entry[0] == "node":
                self.add_node(entry)

    def add_node(self, parsed_node):
        if parsed_node[1] in [node.get_name() for node in self.nodes]: # Node with same identifier already exists
            print("error: duplicate node names")
            return
        new_node = Node(parsed_node[1])
        self.nodes.append(new_node)


class Node(object):
    def __init__(self, name):
        self.name = name
        self.equations = []

    def get_name(self):
        return self.name
    
class Equation(object):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs