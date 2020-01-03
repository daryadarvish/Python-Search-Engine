"""Lab 8
CPE202

Darya Darvish
"""


class LinkedList:
    """
    This class serves as an abstract data type that
    creates a linked list.  Data points to the value in the list
    and next points to the next item in the list.
    """
    def __init__(self, data, nxt=None):
        """A Linked List is one of
        - None, or
        - Node(data, next): A Linked List
        Attributes:
            data(int): int value in this example but can be any data type
            nxt(Node): an object of Node

        class(a linked list)
        """
        self.data = data
        self.next = nxt

    def __repr__(self):
        """This function accepts the argument self.  The purpose of this
        function is to give a string of the class when the class is printed
         """
        return "LinkedList(%s,%s)"\
               % (self.data, self.next)

    def __eq__(self, other):
        """This function accepts the argument self and other.  The purpose of
        this function is to check equality between the class objects and what
        they are supposed to be.
        """
        return isinstance(other, LinkedList) and self.data == other.data \
            and self.next == other.next
