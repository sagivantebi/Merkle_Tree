# Sagiv Antebi, 318159282, Dvir Amram, 318192200
# !/usr/bin/python3
import hashlib

COUNT = [10]
ID_NUM = 0


class MerkleTreeNode:
    def __init__(self, value):
        self.left = None
        self.right = None
        self.neighbor = None
        self.parent = None
        self.value = value
        self.hashValue = hashlib.sha256(value.encode('utf-8')).hexdigest()


def build_tree(leaves):
    nodes = []
    for i in leaves:
        nodes.append(MerkleTreeNode(i))

    while len(nodes) != 1:
        temp = []
        lenOfNodes = len(nodes)
        for i in range(0, lenOfNodes, 2):
            node1 = nodes[i]
            if (i + 1) < lenOfNodes:
                node2 = nodes[i + 1]
            else:
                temp.append(nodes[i])
                break
            concatenatedHash = node1.hashValue + node2.hashValue
            parent = MerkleTreeNode(concatenatedHash)
            parent.left = node1
            parent.right = node2
            node1.parent = parent
            node2.parent = parent
            node1.neighbor = node2
            node2.neighbor = node1
            temp.append(parent)
        nodes = temp
    return nodes[0]


# Function to print binary tree in 2D
# It does reverse inorder traversal
def print_tree(root, space):
    if (root == None):
        return
    space += COUNT[0]
    print_tree(root.right, space)
    print()
    for i in range(COUNT[0], space):
        print(end=" ")
    print(root.hashValue)

    # Process left child
    print_tree(root.left, space)


# Wrapper over print2DUtil()
def print2D(root):
    # space=[0]
    # Pass initial space count as 0
    print_tree(root, 0)


def findNodeById(root, listLeafs, idNode):
    if root is None:
        return None
    if root.value == listLeafs[idNode]:
        return root
    toReturn = findNodeById(root.left, listLeafs, idNode)
    if toReturn != None:
        return toReturn
    toReturn = findNodeById(root.right, listLeafs, idNode)
    if toReturn != None:
        return toReturn
    return None

def recursive_get_proof(root, nodeMerkle):
    if root.value == nodeMerkle.value:
        return
    print(nodeMerkle.neighbor.hashValue)
    recursive_get_proof(root, nodeMerkle.parent)


def menu():
    # getting the input from user
    choice = input()
    firstChar = choice[0]
    root = 0
    listLeafs = []
    while choice != 0:
        if firstChar == '1':
            listLeafs.append(choice[2:])
            root = build_tree(listLeafs)
            # print2D(root)
        elif firstChar == '2':
            if root != 0:
                print(root.hashValue)
            else:
                print()
        elif firstChar == '3':
            print(root.hashValue)
            nodeMerkle = findNodeById(root, listLeafs, int(choice[2:]))
            recursive_get_proof(root, nodeMerkle)
        elif firstChar == '4':
            continue
        elif firstChar == '5':
            continue
        elif firstChar == '6':
            continue
        elif firstChar == '7':
            continue
        else:
            print("Invalid input")
        choice = input()
        firstChar = choice[0]


if __name__ == '__main__':
    menu()