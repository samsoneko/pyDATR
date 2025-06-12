class Theory(object): # Object for holding the information of a theory
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
        new_node = Node(parsed_node)
        self.nodes.append(new_node)

    def present(self):
        pretty_string = ""
        pretty_string += "Theory: " + self.name
        for node in self.nodes:
            pretty_string += node.present()
        return pretty_string
    
    def build(self):
        # 1. Resolve local inheritance
        for node in self.nodes:
            node.build_local(self)
        
        # 2. Resolve global inheritance
        pass

    def find_node_or_none(self, node_name):
        for node in self.nodes:
            if node.get_name() == node_name:
                return node
        return None

class Node(object): # Object for holding the information of a node
    def __init__(self, parsed_node):
        self.name = parsed_node[1]
        self.equations = []
        for equation in parsed_node[2]:
            self.add_equation(equation)

    def get_name(self):
        return self.name
    
    def add_equation(self, parsed_equation):
        new_equation = Equation(parsed_equation)
        self.equations.append(new_equation)
    
    def present(self):
        pretty_string = ""
        pretty_string += "\n  Node: " + self.name
        for equation in self.equations:
            pretty_string += equation.present()
        return pretty_string
    
    def build_local(self, theory): # Resolve all local inheritance
        for equation in self.equations:
            equation.build_local(theory, self)
        pass

    def get_all_equations(self):
        return self.equations
    
class Equation(object): # Object for holding the information of an equation
    def __init__(self, parsed_equation):
        self.lhs = parsed_equation[1][1]
        if parsed_equation[2][0] == "defrhs": # Equation is definitional
            self.type = "definitional"
            rhs = []
            for element in parsed_equation[2][1]:
                rhs.append(element)
            self.rhs = rhs
        elif parsed_equation[2][0] == "extrhs": # Equation is definitional
            self.type = "extensional"
            self.rhs = parsed_equation[2][1]
        print(self.lhs)
        print(self.rhs)
        print("\n")

    def present(self):
        pretty_string = ""
        pretty_string += "\n    Equation(" + self.type + "): " + str(self.lhs) + " -> " + str(self.rhs)
        return pretty_string
    
    def build_local(self, theory, parent_node): # Resolve all local inheritance
        if self.type == "extensional":
            return # If the equation is extensional, no inheritance needs to be resolved
        if self.type == "definitional":
            for element in self.rhs:
                if element[0] == "atom":
                    pass # If the current element of the RHS is an atom, it can't be resolved further
                elif element[0] == "global_pointer":
                    pass # If the current element of the RHS is inherited globally, we handle it later
                elif element[0] == "local_pointer":
                    # Resolve the local inheritance
                    if element[1] != None:
                        # The element is inherited from another node
                        giving_node = theory.find_node_or_none(element[1])
                        if giving_node == None: # If the node does not exist, raise a name error
                            raise NameError
                        else: # If the node exists, continue
                            if element[2] == None:
                                # Everything is inherited
                                print("inherit all")
                                new_equations = giving_node.get_all_equations()
                                for new_equation in new_equations:
                                    parent_node.equations.append(new_equation) # Very very bad code
                                # TODO Check if node already exist
                            else:
                                print("inherit part")
                                # TODO
                    else:
                        # The element is inherited from the current node
                        # TODO
                        pass
                else:
                    raise SyntaxError