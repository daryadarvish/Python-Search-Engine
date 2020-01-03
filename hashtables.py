"""Lab 8
CPE202

Darya Darvish
"""
from linked_list import LinkedList


def hash_string(string, size):
    """hash function for string key weighted by a prime number.
    Args:
        string(str): string key
        size(int): size of hash table
    Returns:
        Int: hash value
    """
    hashy = 0
    for c in string:
        hashy = (hashy * 31 + ord(c)) % size
    return hashy


def import_stopwords(filename, hashtable):
    """this function imports a file and stores it in a hash
    table.
    Args:
        filename(str): name of file to be imported
        hashtable(arr): hash table
    Returns:
        hash table filled with hash values
    """
    file = open(filename)
    file_arr = file.read()
    file_arr = file_arr.split()
    for item in file_arr:
        hashtable.put(item, item)
    return hashtable


class HashTableSepchain:
    def __init__(self, table_size=11):
        """A Hash Table is one of
        - HashTableSepchain(hash_table): A Hash Table
        Attributes:
            table_size(int): Size of the Hash Table
        class(a hash table using separate chaining)
        """
        self.hash_table = [None]*table_size
        self.table_size = table_size
        self.num_items = 0
        self.num_collisions = 0

    def __repr__(self):
        """This function accepts the argument self.  The purpose of this
        function is to give a string representation of the class when the class
        is printed
         """
        return "HashTableSepChain(%s)" % self.hash_table

    def __eq__(self, other):
        """This function accepts the argument self and other.  The purpose of
        this function is to check equality between the class objects and what
        they are supposed to be.
        """
        return isinstance(other, HashTableSepchain) and self.hash_table == other.hash_table

    def __contains__(self, key):
        """This function accepts the argument key.  The purpose of
            this function is to override the in operator, and by doing
            so it will use self.contains to see if the key is in the graph
        """
        return self.contains(key)

    def __setitem__(self, key, data):
        """This function accepts the argument key and data.  The purpose of
            this function is so that items can be hashed in to the hash table.
            It overrides  []
            """
        key1, data1 = self.get(key).data
        return data1

    def __getitem__(self, key):
        """This function accepts the argument key.  The purpose of
            this function is so that items can be searched for in the table
            and overrides []
            """
        key1, data1 = self.get(key).data
        return data1

    def put(self, key, data):
        """this function puts values into the hash table.
        Args:
            key(str): key value in string
            data(arr): value stored
        """
        hash_value = hash_string(key, self.table_size)
        if self.hash_table[hash_value] is None:
            self.hash_table[hash_value] = LinkedList((key, data))
            self.num_items += 1
        else:
            self.num_collisions += 1
            temp = self.hash_table[hash_value]
            self.hash_table[hash_value] = LinkedList((key, data))
            self.hash_table[hash_value].next = temp
            self.num_items += 1
        if self.load_factor() > 1.5:
            self.rehash()

    def rehash(self):
        """this function is called when the load factor is greater than
        1.5.  It temporarily stores the old hash table and re-inserts the
        old values into a newly created hash table
        """
        temp = self.hash_table
        temp_num_items = self.num_items
        self.num_items = 0
        self.num_collisions = 0
        self.table_size = 2 * self.table_size + 1
        self.hash_table = [None] * self.table_size
        for item in temp:
            if item is not None:
                while item.next is not None:
                    key1, data1 = item.data
                    self.put(key1, data1)
                    item = item.next
                key1, data1 = item.data
                self.put(key1, data1)
        self.num_items = temp_num_items

    def get(self, key):
        """ this function takes a key and returns the item (key, item) pair from the
        hash table associated with the key. If no key-item pair is associated with
        the key, the function raises a LookupError exception.
        Attributes:
            key(str): key that is being searched for
        Returns:
            key_pair(tuple): key value pair in correct hash location
            """
        hash_value = hash_string(key, self.table_size)
        temp = self.hash_table[hash_value]
        if temp is None:
            return False
        while temp.next is not None:
            key1, data1 = temp.data
            if key1 == key:
                return key1, data1
            temp = temp.next
        key1, data1 = temp.data
        if key1 == key:
            return key1, data1
        return False
        # hash_value = hash_string(key, self.table_size)
        # try:
        #     key_pair = self.hash_table[hash_value]
        # except LookupError:
        #     raise LookupError
        # return key_pair

    def contains(self, key):
        """ this function searches the hash table and finds if the key
        is in the hash table
        Attributes:
            key(str): key to be searched for based on its hash value
        Returns:
            True if the key is in the hash table and False if the key is
            not in the hash table.
            """
        hash_value = hash_string(key, self.table_size)
        temp = self.hash_table[hash_value]
        if temp is None:
            return False
        while temp.next is not None:
            key1, data1 = temp.data
            if key1 == key:
                return True
            temp = temp.next
        key1, data1 = temp.data
        if key1 == key:
            return True
        return False

    def remove(self, key):
        """ this function searches the hash table and finds if the key
        is in the hash table.  it then removes that key-data pair from the hash table
        Attributes:
            key(str): key to be searched for based on its hash value
        Returns:
            key(str), data(str,int): key-value pair that is removed
            """
        self.num_items -= 1
        hash_value = hash_string(key, self.table_size)
        temp = self.hash_table[hash_value]
        if temp is None:
            raise LookupError
        while temp.next is not None:
            key1, data1 = temp.data
            if key1 == key:
                temp1 = temp.data
                temp.data = temp.next
                if temp.data is None:
                    self.hash_table[hash_value] = None
                return temp1
            temp = temp.next
        key1, data1 = temp.data
        if key1 == key:
            temp1 = temp.data
            temp.data = temp.next
            if temp.data is None:
                self.hash_table[hash_value] = None
            return temp1
        raise LookupError

    def size(self):
        """This function returns the number of key-value pairs
        currently stored in the hash table.
            Returns:
                self.num_items[int]
        """
        return self.num_items

    def load_factor(self):
        """This function returns the load factor of the
        hash table.
            Returns:
                self.num_items[int]
        """
        load_factor = self.num_items/self.table_size
        return load_factor

    def collisions(self):
        """This function returns the number of collisions
        that have occurred.
            Returns:
                self.num_items[int]
        """
        return self.num_collisions


class HashTableLinear:
    def __init__(self, table_size=11):
        """A Hash Table is one of
        - HashTableLinear(hash_table): A Hash Table
        Attributes:
            table_size(int): Size of the Hash Table
        class(a hash table using separate chaining)
        """
        self.hash_table = [None] * table_size
        self.table_size = table_size
        self.num_items = 0
        self.num_collisions = 0
        self.s = 1

    def __repr__(self):
        """This function accepts the argument self.  The purpose of this
        function is to give a string representation of the class when the class
        is printed
         """
        return "HashTableLinear(%s)" % self.hash_table

    def __eq__(self, other):
        """This function accepts the argument self and other.  The purpose of
        this function is to check equality between the class objects and what
        they are supposed to be.
        """
        return isinstance(other, HashTableLinear) and self.hash_table == other.hash_table

    def __contains__(self, key):
        """This function accepts the argument key.  The purpose of
            this function is to override the in operator, and by doing
            so it will use self.contains to see if the key is in the graph
        """
        return self.contains(key)

    def __setitem__(self, key, data):
        """This function accepts the argument key and data.  The purpose of
            this function is so that items can be hashed in to the hash table.
            It overrides  []
            """
        self.remove(key)
        self.put(key, data)

    def __getitem__(self, key):
        """This function accepts the argument key.  The purpose of
            this function is so that items can be searched for in the table
            and overrides []
            """
        if self.get(key) is None:
            return None
        key1, data1 = self.get(key)
        return data1

    def linear_rehash(self, hash_value):
        hash = hash_value + self.s
        if hash > self.table_size - 1:
            hash = 0
        return hash

    def put(self, key, data):
        """this function puts values into the hash table.
        Args:
            key(str): key value in string
            data(arr): value stored
        """
        hash_value = hash_string(key, self.table_size)
        if self.hash_table[hash_value] is None:
            self.hash_table[hash_value] = (key, data)
            self.num_items += 1
        else:
            while self.hash_table[hash_value] is not None:
                self.num_collisions += 1
                hash_value = self.linear_rehash(hash_value)
                if hash_value > self.table_size - 1:
                    hash_value = 0
            self.hash_table[hash_value] = (key, data)
            self.num_items += 1
        if self.load_factor() >= 0.75:
            self.rehash()

    def rehash(self):
        """this function is called when the load factor is greater than
        1.  It temporarily stores the old hash table and re-inserts the
        old values into a newly created hash table
        """
        temp = self.hash_table
        temp_num_items = self.num_items
        self.num_items = 0
        self.num_collisions = 0
        self.table_size = 2 * self.table_size + 1
        self.hash_table = [None] * self.table_size
        for item in temp:
            if item is not None:
                key1, data1 = item
                self.put(key1, data1)
        self.num_items = temp_num_items

    def get(self, key):
        """ this function takes a key and returns the item (key, item) pair from the
        hash table associated with the key. If no key-item pair is associated with
        the key, the function raises a LookupError exception.
        Attributes:
            key(str): key that is being searched for
        Returns:
            key_pair(tuple): key value pair in correct hash location
            """
        hash_value = hash_string(key, self.table_size)
        while self.hash_table[hash_value] is not None:
            key1, data1 = self.hash_table[hash_value]
            if key1 == key:
                return self.hash_table[hash_value]
            hash_value = self.linear_rehash(hash_value)
        return None

    def contains(self, key):
        """ this function searches the hash table and finds if the key
        is in the hash table
        Attributes:
            key(str): key to be searched for based on its hash value
        Returns:
            True if the key is in the hash table and False if the key is
            not in the hash table.
            """
        hash_value = hash_string(key, self.table_size)
        while self.hash_table[hash_value] is not None:
            key1, data1 = self.hash_table[hash_value]
            if key1 == key:
                return True
            hash_value = self.linear_rehash(hash_value)
        return False
        # for item in self.hash_table:
        #     if item is None:
        #         continue
        #     key1, data1 = item
        #     if key1 == key:
        #         return True
        # return False

    def remove(self, key):
        """deletes an entry from hash table
        Args:
        table (list) : hash table
        key (int) : the key of an entry to be deleted
        """
        if not self.contains(key):
            return
        m, i = self.table_size, hash_string(key, self.table_size)
        key1, data1 = self.hash_table[i]
        while key != key1:
            i = (i + 1) % m
        self.hash_table[i] = None
        i = (i + 1) % m
        while self.hash_table[i]:
            key_to_redo, val_to_redo = self.hash_table[i]
            self.hash_table[i] = None
            self.put(key_to_redo, val_to_redo)
            i = (i + 1) % m
        return key1, data1

    def size(self):
        """This function returns the number of key-value pairs
        currently stored in the hash table.
            Returns:
                self.num_items[int]
        """
        return self.num_items

    def load_factor(self):
        """This function returns the load factor of the
        hash table.
            Returns:
                self.num_items[int]
        """
        load_factor = self.num_items/self.table_size
        return load_factor

    def collisions(self):
        """This function returns the number of collisions
        that have occurred.
            Returns:
                self.num_items[int]
        """
        return self.num_collisions


class HashTableQuadratic:
    def __init__(self, table_size=11):
        """A Hash Table is one of
        - HashTableQuadratic(hash_table): A Hash Table
        Attributes:
            table_size(int): Size of the Hash Table
        class(a hash table using separate chaining)
        """
        self.hash_table = [None] * table_size
        self.table_size = table_size
        self.num_items = 0
        self.num_collisions = 0
        self.s = 1

    def __repr__(self):
        """This function accepts the argument self.  The purpose of this
        function is to give a string representation of the class when the class
        is printed
         """
        return "HashTableLinear(%s)" % self.hash_table

    def __eq__(self, other):
        """This function accepts the argument self and other.  The purpose of
        this function is to check equality between the class objects and what
        they are supposed to be.
        """
        return isinstance(other, HashTableLinear) and self.hash_table == other.hash_table

    def __contains__(self, key):
        """This function accepts the argument key.  The purpose of
            this function is to override the in operator, and by doing
            so it will use self.contains to see if the key is in the graph
        """
        return self.contains(key)

    def __setitem__(self, key, data):
        """This function accepts the argument key and data.  The purpose of
            this function is so that items can be hashed in to the hash table.
            It overrides  []
        """
        self.put(key, data)

    def __getitem__(self, key):
        """This function accepts the argument key.  The purpose of
            this function is so that items can be searched for in the table
            and overrides []
            """
        key1, data1 = self.get(key)
        return data1

    def quadratic_rehash(self, hash_value, i):
        hash = hash_value + i**2
        i += 1
        return hash

    def put(self, key, data):
        """this function puts values into the hash table.
        Args:
            key(str): key value in string
            data(arr): value stored
        """
        hash_value = hash_string(key, self.table_size)
        if self.hash_table[hash_value] is None:
            self.hash_table[hash_value] = (key, data)
            self.num_items += 1
        else:
            i = 1
            while self.hash_table[hash_value] is not None:
                self.num_collisions += 1
                hash_value = self.quadratic_rehash(hash_value, i)
                if hash_value > self.table_size - 1:
                    hash_value = 0
            self.hash_table[hash_value] = (key, data)
            self.num_items += 1
        if self.load_factor() >= 0.75:
            self.rehash()

    def rehash(self):
        """this function is called when the load factor is greater than
        1.  It temporarily stores the old hash table and re-inserts the
        old values into a newly created hash table
        """
        temp = self.hash_table
        temp_num_items = self.num_items
        self.num_items = 0
        self.num_collisions = 0
        self.table_size = 2 * self.table_size + 1
        self.hash_table = [None] * self.table_size
        for item in temp:
            if item is not None:
                key1, data1 = item
                self.put(key1, data1)
        self.num_items = temp_num_items

    def get(self, key):
        """ this function takes a key and returns the item (key, item) pair from the
        hash table associated with the key. If no key-item pair is associated with
        the key, the function raises a LookupError exception.
        Attributes:
            key(str): key that is being searched for
        Returns:
            key_pair(tuple): key value pair in correct hash location
            """
        hash_value = hash_string(key, self.table_size)
        try:
            key_pair = self.hash_table[hash_value]
        except LookupError:
            raise LookupError
        return key_pair

    def contains(self, key):
        """ this function searches the hash table and finds if the key
        is in the hash table
        Attributes:
            key(str): key to be searched for based on its hash value
        Returns:
            True if the key is in the hash table and False if the key is
            not in the hash table.
            """
        for item in self.hash_table:
            if item is None:
                continue
            key1, data1 = item
            if key1 == key:
                return True
        return False

    def remove(self, key):
        """deletes an entry from hash table
        Args:
        table (list) : hash table
        key (int) : the key of an entry to be deleted
        """
        if not self.contains(key):
            return
        m, i = self.table_size, hash_string(key, self.table_size)
        key1, data1 = self.hash_table[i]
        while key != key1:
            i = (i + 1) % m
        self.hash_table[i] = None
        i = (i + 1) % m
        while self.hash_table[i]:
            key_to_redo, val_to_redo = self.hash_table[i]
            self.hash_table[i] = None
            self.put(key_to_redo, val_to_redo)
            i = (i + 1) % m
        return key1, data1

    def size(self):
        """This function returns the number of key-value pairs
        currently stored in the hash table.
            Returns:
                self.num_items[int]
        """
        return self.num_items

    def load_factor(self):
        """This function returns the load factor of the
        hash table.
            Returns:
                self.num_items[int]
        """
        load_factor = self.num_items/self.table_size
        return load_factor

    def collisions(self):
        """This function returns the number of collisions
        that have occurred.
            Returns:
                self.num_items[int]
        """
        return self.num_collisions
