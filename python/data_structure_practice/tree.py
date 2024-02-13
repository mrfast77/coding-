class TreeNode:
    def __init__(self, name, designation):
        self.name = name
        self.designation = designation
        self.children = []
        self.parent = None

    def add_child(self, child):
        child.parent = self
        self.children.append(child)

    def get_level(self):
        level = 0
        p = self.parent
        while p:
            level += 1
            p = p.parent

        return level


    def print_tree(self):
        spaces = "   " * self.get_level()
        print(spaces + self.name)
        if self.children:
            for child in self.children:
                child.print_tree()

def build_tree():
    root = TreeNode("Nilupul", "CEO")

    cto = TreeNode("Chinmay", "CTO")

    infra_head = TreeNode("Vishwa", "Infrastructure Head")
    infra_head.add_child(TreeNode("Dhaval", "Cloud Manager"))
    infra_head.add_child(TreeNode("Abhijit", "App Manager"))

    cto.add_child(infra_head)
    cto.add_child(TreeNode("Aamir", "Application Head"))


    hr = TreeNode("Gels", "HR Head")
    hr.add_child(TreeNode("Peter", "Recruitment Manager"))
    hr.add_child(TreeNode("Waqas", "Policy Manager"))

    root.add_child(cto)
    root.add_child(hr)

    root.print_tree()

build_tree()


    