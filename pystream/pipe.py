def pipe(*fns):
    """
    Pipe the output of one function to the input of another.
    """
    def piped(x):
        for fn in fns:
            x = fn(x)
        return x
    return piped
