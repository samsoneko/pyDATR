class DATRPathError(LookupError):
    # Raised when the path given in the query can not be resolved
    def __init__(self, node, path):
        self.node = node
        self.path = path
        super().__init__(self.node, self.path)

class DATRNodeError(LookupError):
    # Raised when a node in the given query can not be resolved
    def __init__(self, node):
        self.node = node
        super().__init__(self.node)

class DATRSyntaxError(SyntaxError):
    # Raised when a query is of invalid form
    def __init__(self, query_element):
        self.query_element = query_element
        super().__init__(self.query_element)

class DATRResolvementError(SystemError):
    # Raised when resolvement of the rhs fails
    def __init__(self, rhs):
        self.rhs = rhs
        super().__init__(self.rhs)