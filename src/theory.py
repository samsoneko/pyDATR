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
            if node.is_resolved == False:
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
        self.sentences = []
        self.is_resolved = False
        for sentence in parsed_node[2]:
            self.add_sentence(sentence, False)

    def get_name(self):
        return self.name
    
    def add_sentence(self, parsed_sentence, is_resolved):
        new_sentence = Sentence(parsed_sentence[1][1], parsed_sentence[2][1], parsed_sentence[2][0], is_resolved)
        self.sentences.append(new_sentence)
    
    def present(self):
        pretty_string = ""
        pretty_string += "\n  Node: " + self.name
        for sentence in self.sentences:
            pretty_string += sentence.present()
        return pretty_string
    
    def build_local(self, theory): # Resolve all local inheritance
        for sentence in self.sentences:
            if sentence.is_resolved == False:
                sentence.build_local(theory, self)

    def get_matching_sentences(self, desc): # Returns all matching sentences that are at least as specific as the given desc (more or equally)
        matching_sentences = []
        for sentence in self.sentences: # Loop through all sentences in the node (as candidates)
            candidate_path = sentence.lhs
            is_fitting = True
            for i in range(len(candidate_path)): # Loop through the elements of the candidate lhs
                if len(desc) > i:
                    if candidate_path[i][1] != desc[i][1]:
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
        print(self.lhs)
        print(self.rhs)
        print("\n")

    def present(self):
        pretty_string = ""
        pretty_string += "\n    Sentence(" + self.type + "): " + str(self.lhs) + " -> " + str(self.rhs)
        return pretty_string
    
    def build_local(self, theory, parent_node): # Resolve all local inheritance
        if self.type == "extensional":
            self.is_resolved = True
            return # If the sentence is extensional, no inheritance needs to be resolved # TODO Return copy of self?
        if self.type == "definitional":
            new_sentences = []
            for element in self.rhs:
                if element[0] == "atom":
                    pass # If the current element of the RHS is an atom, it can't be resolved further
                elif element[0] == "global_pointer":
                    pass # If the current element of the RHS is inherited globally, we handle it later
                elif element[0] == "local_pointer":
                    # Resolve the local inheritance
                    node_to_inherit_from = element[1] if element[1] != None else parent_node.get_name() # Insert local node name if reference is none
                    giving_node = theory.find_node_or_none(node_to_inherit_from) # Get the node to inherit from from the theory

                    if giving_node == None: # If the node does not exist, raise a name error
                        raise NameError
                    else: # If the node exists, inheritance can be continued
                        if element[2] == None:
                            inher_desc = self.lhs # If there is no descriptor in the path, the descriptor is equal to the lhs
                        else:
                            inher_desc = element[2] # If there is a descriptor in the path, it is used as a desc

                        print(parent_node.get_name() + " inherits " + str(inher_desc) + " from " + giving_node.get_name()) # DEBUG Printing

                        new_sentences = giving_node.get_matching_sentences(inher_desc) # Get the matching sentences from the giving node

                        for sentence in new_sentences:
                            parent_node.sentences.append(sentence) # WRONG
                            # TODO Construct new lhs and rhs accordingly
                            lhs_prefix = self.lhs # Use own lhs as prefix for new lhs
                            path_cutoff = inher_desc # Cut off the rhs path used for referencing
                            sentence_content = sentence.rhs # Use the content of the inherited sentence
                            
                        # TODO Check if node already exist
                else:
                    raise SyntaxError
        else:
            raise SyntaxError # If the sentence is neither extensional nor definitional, something went horribly wrong
    
    def evaluate_desc(self, theory, parent_node, desc):
        pass