# Sagiv Antebi
# !/usr/bin/python3
import binascii
import hashlib

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

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


def findNodeByIdInt(root, listLeafs, idNode):
    if root is None:
        return None
    if root.value == listLeafs[idNode]:
        return root
    toReturn = findNodeByIdInt(root.left, listLeafs, idNode)
    if toReturn != None:
        return toReturn
    toReturn = findNodeByIdInt(root.right, listLeafs, idNode)
    if toReturn != None:
        return toReturn
    return None


def findNodeByIdStr(root, listLeafs, idNode):
    if root is None:
        return None
    if root.value == idNode:
        return root
    toReturn = findNodeByIdStr(root.left, listLeafs, idNode)
    if toReturn != None:
        return toReturn
    toReturn = findNodeByIdStr(root.right, listLeafs, idNode)
    if toReturn != None:
        return toReturn
    return None


def recursive_get_proof(nodeMerkle, str):
    parent_node = nodeMerkle.parent
    if parent_node is None:
        return ""
    else:
        if parent_node.left.hashValue == str:
            if parent_node.right is not None:
                return "1" + parent_node.right.hashValue + " " + recursive_get_proof(parent_node, parent_node.hashValue)
        else:
            return "0" + parent_node.left.hashValue + " " + recursive_get_proof(parent_node, parent_node.hashValue)


def sign(root, key):
    key = serialization.load_pem_private_key(key.encode(), password=None)
    message = root.hashValue.encode()
    signature = key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return binascii.b2a_base64(signature).decode()


def checkValid(public_key, sig, text_verify):
    public_key = serialization.load_pem_public_key(public_key.encode())
    try:
        public_key.verify(
            binascii.a2b_base64(sig),
            text_verify.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
    except InvalidSignature:
        return False
    return True


def menu():
    # getting the input from user
    choice = input()
    firstChar = choice[0]
    root = 0
    listLeafs = []
    while (1):
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
            nodeMerkle = findNodeByIdInt(root, listLeafs, int(choice[2:]))
            toPrint = root.hashValue + " " + recursive_get_proof(nodeMerkle, nodeMerkle.hashValue)
            print(toPrint[:-1])
        elif firstChar == '4':
            splitBySpaces = choice.split(" ", 2)
            value = splitBySpaces[1]
            inputCompare = splitBySpaces[2]
            nodeMerkle = findNodeByIdStr(root, listLeafs, value)
            toCompare = root.hashValue + " " + recursive_get_proof(nodeMerkle, nodeMerkle.hashValue)
            print(inputCompare == toCompare[:-1])
        elif firstChar == '5':
            private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
            public_key = private_key.public_key()

            pem_public = public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                                 format=serialization.PublicFormat.SubjectPublicKeyInfo)
            pem_private = private_key.private_bytes(encoding=serialization.Encoding.PEM,
                                                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                                                    encryption_algorithm=serialization.NoEncryption())
            print(pem_private.decode())
            print(pem_public.decode())

        elif firstChar == '6':
            data = choice.split(" ")
            # good check if the given text is by spaces
            data_of_proof = ' '.join(data[1:]) + "\n"
            temp = input()
            while "-----END RSA PRIVATE KEY-----" not in temp:
                data_of_proof = data_of_proof + temp + "\n"
                temp = input()
            data_of_proof = data_of_proof + temp
            value_to_print = sign(root, data_of_proof)
            print(value_to_print, end="")

        elif firstChar == '7':
            data = choice.split(" ")
            # good check if the given text is by spaces
            data_of_proof = ' '.join(data[1:]) + "\n"
            temp = input()
            while "-----END PUBLIC KEY-----" not in temp:
                data_of_proof = data_of_proof + temp + "\n"
                temp = input()
            data_of_proof = data_of_proof + temp + "\n"
            one_raw_to_dump = input()
            root_signature = input().split(' ')
            sig = root_signature[0]
            text_verify = root_signature[1]
            print(checkValid(data_of_proof, sig, text_verify))
        else:
            print("Invalid input")
        choice = input()
        while len(choice) == 0:
            choice = input()
        firstChar = choice[0]


if __name__ == '__main__':
    menu()
