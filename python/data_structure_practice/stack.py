from collections import deque

class Stack:
    def __init__(self):
        self.container = deque()

    def push(self, value):
        self.container.append(value)

    def pop(self):
        return self.container.pop()
    
    def peek(self):
        return self.container[-1]
    
    def is_empty(self):
        return len(self.container)==0
    
    def size(self):
        return len(self.container)
    
stack = Stack()
    
def insert_string(string):
    for char in string:
        stack.push(char)

def reverse_string(string):
    insert_string(string)

    reverse = ""
    while stack.size() != 0:
        reverse += stack.pop()
    
    return reverse

def main():
    string = "What is my deal?"
    print(reverse_string(string))


if __name__ == "__main__":
    main()
    