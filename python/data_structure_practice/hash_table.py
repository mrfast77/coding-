# Hash table implemented with chaining

import csv

class HashTable:
    def __init__(self): 
        self.MAX = 10
        self.arr = [[] for i in range(self.MAX)]

    def hash(self, key):
        hash = 0
        for char in key:
            hash += ord(char)
        return hash % self.MAX
    
    def insert(self, key, value):
        hash = self.hash(key)
        found = False
        #for index, element in enumerate(self.arr[hash]):
            #if len(element) == 2 and element[0] == key:
                #self.arr[hash][index] = (key, value)
                #found = True
        if not found:
            self.arr[hash].append((key, value))

    def get(self, key):
        hash = self.hash(key)
        value = []
        for index, element in enumerate(self.arr[hash]):
            if element[0] == key:
                value.append(element[1])

        if len(value) == 1:
            return value[0]
        else:
            return value
        
    def print_hash_values():
        table = HashTable()
        list = [table.hash(f'Jan {i}') for i in range(30)]
        for item in enumerate(list):
            print(item)


def main():
    table = HashTable()

    with open('nyc_weather.csv', newline='') as file:
        reader = csv.DictReader(file)

        for row in reader:
            table.insert(row['date'], row['temperature(F)'])

    print(table.arr)

    print(table.get('Jan 4'))

if __name__ == "__main__":
    main()