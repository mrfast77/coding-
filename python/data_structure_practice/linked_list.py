class Node:
    def __init__(self, data = None, next = None):
        self.data = data
        self.next = next

   

class Linked_list():
    def __init__(self):
        self.head = None

    def insert_at_beginning(self, data):
        node = Node(data, self.head)
        self.head = node

    def insert_at_end(self, data):
        if not self.head:
            self.head = Node(data, None)
            return
        
        current = self.head
        while current.next:
            current = current.next
        
        current.next = Node(data, None)
        
    def insert_values(self, data_list):
        self.head = None

        for data in data_list:
            self.insert_at_end(data)

    def find_length(self):
        count = 0
        
        current = self.head
        while current:
            count += 1
            current = current.next

        return count
    
    def remove_at(self, index):
        if not self.head:
            return None
        
        if index < 0 or index >= self.find_length():
            raise Exception("Invalid index")
        
        if index == 0:
            self.head = self.head.next
            return

        current = self.head
        for _ in range(index - 1):
            current = current.next
        
        current.next = current.next.next

    def insert_at(self, index, data):
        if index < 0 or index > self.find_length():
            raise Exception("Invalid index")
        
        if index == 0:
            self.insert_at_beginning()
            return
        
        current = self.head
        for _ in range(index - 1):
            current = current.next
    
        current.next = Node(data, current.next)
        
    def print(self):
        if self.head is None:
            print("Linked list is empty")
            return

        current = self.head

        while current:
            print(current.data)
            current = current.next

    def insert_after_value(self, data_after, new_data):
        current = self.head
        while current.data != data_after:
            current = current.next
        current.next = Node(new_data, current.next)

    def remove_by_value(self, data):
        if self.head.data == data:
            self.head = self.head.next
            return
        current = self.head
        while current.next.data != data:
            current = current.next
            if not current.next:
                raise Exception("Value does not exist in list")
        current.next = current.next.next

            
 
def main():
    list = Linked_list()
    list.insert_values([1, 2, 3, 4])
    list.remove_by_value(5)
    list.print()

    
if __name__ == "__main__":
    main()  