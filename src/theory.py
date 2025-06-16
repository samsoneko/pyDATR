import regex as re

class Theory(object): # Object for holding the information of a theory
    def __init__(self, name, parsed_datr):
        self.name = name
        self.nodes = []
        for entry in parsed_datr:
            if entry[0] == "node":
                self.add_node(entry)

    # Adds a node to the theory
    def add_node(self, parsed_node):
        if parsed_node[1] in [node.get_name() for node in self.nodes]: # Node with same identifier already exists
            print("pyDATR Error: Duplicate node names")
            return
        new_node = Node(parsed_node)
        self.nodes.append(new_node)

    # Returns a pretty print of the theory content
    def present(self):
        pretty_string = ""
        pretty_string += "Theory: " + self.name
        for node in self.nodes:
            pretty_string += node.present()
        return pretty_string
    
    # Prepares a query for resolvement
    def query(self, query):
        try:
            # Split the query into node and path
            split_query = query.split(":")
            node_name = split_query[0]
            path = split_query[1]
            path = path.strip()[1:-1].split() # Prepare the path for resolvement
            node_regex = re.compile(r"[A-ZÀ-ÖØ-Þ][^\W!:<>\(\)=\"'\.%]*")
            path_regex = re.compile(r"[^\WA-Z!:<>\(\)=\"'\.%][^\W!:<>\(\)=\"'\.%]*")
            if not node_regex.match(node_name):
                raise SyntaxError
            for path_element in path:
                if not path_regex.match(path_element):
                    raise SyntaxError

        except:
            print("pyDATR Error: Query is of invalid form")
            raise SyntaxError

        print("The query will be executed for node: " + node_name + " and path: " , path, "\n")

        # Resolves the query, setting bot the local and the global context to the initial node
        return self.resolve(node_name, path, node_name)
    
    # Resolves a query inside the theory
    def resolve(self, node_name, path, global_node_name):
        # Find the specified node and process the path
        node = self.find_node_or_none(node_name)

        # Only evaluate further if the specified node exists in the theory
        if node:
            print("Resolving query for: ", path)
            for descriptor in path:
                if type(descriptor) != str:
                    print("Inheritance in descriptor found: ", descriptor)
                    resolved_descriptor = self.resolve_rhs([], [descriptor], node_name, global_node_name)
                    index = path.index(descriptor) # This raises ValueError if there's no 'b' in the list.
                    path[index:index+1] = resolved_descriptor
            print(path)
            best_match = node.get_best_match(path)
            node_rhs = best_match.rhs
            remaining_path = path[len(best_match.lhs):]
            print("The remaining path after the match is: ", remaining_path, "\n")
            result = self.resolve_rhs(remaining_path, node_rhs, node_name, global_node_name)
        else:
            print("pyDATR Error: The specified node does not exist")
            raise NameError
        
        return result
    
    # Resolves the rhs of a sentence in the context of the given node
    def resolve_rhs(self, remaining_path, rhs, context_node_name, global_node_name):

        # If the current rhs consists of only one element
        if type(rhs) == list and len(rhs) == 1:
            rhs = rhs[0]
            # If the current rhs element is an atom and the remaining path is empty, return the atom
            # EVERY RECURSIVE CALL OF THIS FUNCTION HAS TO ARRIVE HERE AT SOME POINT, OTHERWISE THE QUERY FAILS
            if type(rhs) == str:
                print("Atom found: " + rhs)
                return [rhs]
            
            # TODO Add variable handling

            # If the current rhs element is a pointer, resolve it
            if type(rhs) == tuple:
                if rhs[0] == "local_pointer":
                    # Handle local inheritance
                    local_node_name = rhs[1] if rhs[1] != None else context_node_name
                    local_path = rhs[2] + remaining_path if rhs[2] != None else remaining_path
                    print("Local pointer found, continuing evaluation in node: " + local_node_name)
                    return self.resolve(local_node_name, local_path, global_node_name)
                elif rhs[0] == "global_pointer":
                    # Handle global inheritance
                    rhs = rhs[1]
                    local_node_name = rhs[1] if rhs[1] != None else global_node_name
                    local_path = rhs[2] + remaining_path if rhs[2] != None else remaining_path
                    print("Global pointer found, continuing evaluation in node: " + global_node_name)
                    return self.resolve(local_node_name, local_path, global_node_name)
                else:
                    # If the evaluation reaches this point, something went horribly wrong
                    print("pyDATR Error: RHS invalid, an error in the parser must have occured")
                    raise TabError
        
        # If the current rhs is a list of multiple elements, recursively restart for each element
        elif type(rhs) == list and len(rhs) > 1:
            values = []
            print("Multiple elements were found in the rhs, starting recursive resolvement")
            for descriptor in rhs:
                print("Rsolvement is startet for path: ", remaining_path, " and rhs: ", descriptor)
                values.extend(self.resolve_rhs(remaining_path, [descriptor], context_node_name, global_node_name))
            return values

        print("pyDATR Error: At least one element of the RHS is invalid")
        raise TabError

    # Finds a node and returns it or returns None
    def find_node_or_none(self, node_name):
        for node in self.nodes:
            if node.get_name() == node_name:
                return node
        return None

class Node(object): # Object for holding the information of a node
    def __init__(self, parsed_node):
        self.name = parsed_node[1]
        self.sentences = []
        self.is_resolved = False
        for sentence in parsed_node[2]:
            self.add_sentence(sentence, False)

    # Returns its own name
    def get_name(self):
        return self.name
    
    # Adds a sentence to the node
    def add_sentence(self, parsed_sentence, is_resolved):
        new_sentence = Sentence(parsed_sentence[1][1], parsed_sentence[2][1], parsed_sentence[2][0], is_resolved)
        self.sentences.append(new_sentence)
    
    # Returns a pretty print of the theory content
    def present(self):
        pretty_string = ""
        pretty_string += "\n  Node: " + self.name
        for sentence in self.sentences:
            pretty_string += sentence.present()
        return pretty_string
    
    # Evaluates a path from a query
    def get_best_match(self, path):
        candidates = []
        for sentence in self.sentences: # Get all paths in the node that could match the query path
            if sentence.matches_path(path):
                candidates.append(sentence)
        print(str(len(candidates)) + " candidates were found")

        if len(candidates) == 0:
            print("pyDATR Error: No fitting path at node " + self.get_name() + " exists")
            raise NameError
        else:
            best_match = candidates[0]
            for candidate in candidates:
                if len(candidate.lhs) > len(best_match.lhs):
                    best_match = candidate
            print("The best sentence is returned: ", best_match.lhs, " -> ", best_match.rhs , " at node: " + self.name)
            return best_match

    # Returns all matching sentences that are at least as specific as the given desc (more or equally)
    def get_matching_sentences(self, desc):
        matching_sentences = []
        for sentence in self.sentences: # Loop through all sentences in the node (as candidates)
            candidate_path = sentence.lhs
            is_fitting = True
            for i in range(len(candidate_path)): # Loop through the elements of the candidate lhs
                if len(desc) > i:
                    if candidate_path[i] != desc[i]:
                        is_fitting = False # If the desc is specified until this point, but not matching candidate, disqualify candidate
            if is_fitting:
                matching_sentences.append(sentence)
            
        return matching_sentences
    
class Sentence(object): # Object for holding the information of a sentence
    def __init__(self, lhs, rhs, type, is_resolved):
        self.is_resolved = is_resolved
        self.lhs = lhs
        self.type = type
        self.rhs = rhs

    # Returns a pretty print of the theory content
    def present(self):
        pretty_string = ""
        pretty_string += "\n    Sentence(" + self.type + "): " + str(self.lhs) + " -> " + str(self.rhs)
        return pretty_string
    
    # Returns true if the lhs does not conflict with the path, hence everything less or equally specified
    def matches_path(self, path):
        for i in range(len(self.lhs)): # Loop through the elements of the candidate lhs
            if i < len(path):
                if self.lhs[i] != path[i]:
                    print("Path: ", self.lhs, " does not fit path ", path, " because an element of it is not equal")
                    return False # If the lhs is specified until this point, but not matching the path, disqualify candidate
            else:
                print("Path: ", self.lhs, " does not fit path ", path, " because it is more specific")
                return False # If the lhs is longer than the path (and hence more specific), disqualify candidate
        return True