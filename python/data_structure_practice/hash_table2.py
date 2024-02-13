# Hash Table implemented with linear probing
class HashTable:
    def __init__(self):
        self.MAX = 10
        self.array = [None for _ in range(self.MAX)]

    def hash(self, key):
        hash = 0
        for char in key:
            hash += ord(char)
        return hash % self.MAX
    
    def get(self, key):
        for _, element in enumerate(self.array):
            if not element:
                continue
            if element[0] == key:
                return element[1]
    
    def is_empty(self, hash):
        if self.array[hash] == None:
            return True
        return False
    
    def insert(self, key, value):
        hash = self.hash(key)
        for _ in range(self.MAX):
            if not self.is_empty(hash):
                if hash + 1 < self.MAX:
                    hash += 1
                else:
                    hash = 0
            else: 
                self.array[hash] = (key, value)
                return
                
            
        


        
    

t = HashTable()
t.insert('march 4', 10)
t.insert('march 6', 20)
t.insert('march 17', 30)
t.insert('march 6', 40)
t.insert('march 6', 50)

print(t.get('march 4'))