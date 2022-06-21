#Omri Ben Hemo, 313255242, Ben Ganon, 318731007
import base64
import binascii
import hashlib
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import *
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature

class Node:
    def __init__(self, father = None, data = '1'.encode(),  left = None, right = None):
        self.father = father
        self.data = data
        self.left = left
        self.right = right

    def toHex(self):
        return self.data

class MerkleTree:

    def __init__(self, root=None, leaves=[]):
        self.root = root
        self.leaf_array = leaves

    def addnode(self, data):
        node = Node(data=get_hash(data))
        self.leaf_array.append(node)
        self.root = build_tree(self.leaf_array)

    def depth(self):
        if self.left is None:
            return 1
        return 1 + self.left.depth()

    def find_right_leaf(self, node):
        if node.right is None and node.left is not None:
            return node.left
        if node.right is None and node.left is None:
            return node
        return self.find_right_leaf(node.right)

    def open_right_leaf(self, node):
        if node.right is None and node.left is not None:
            return True
        if node.right is None and node.left is None:
            return False
        return self.open_right_leaf(node.right)
    def calculateHexRoot(self):
            return self.root.toHex() #check if big or little endian

    def proofOfInclusion(self, numOfLeaf):
            if len(self.leaf_array) <= numOfLeaf:
                return
            node = self.leaf_array[numOfLeaf]
            return self.root.toHex() + " " + self.getProof(node, node.data)

    def getProof(self, leaf, hash):
            fatherNode = leaf.father
            if fatherNode is None:
                return ""
            else:
                if fatherNode.left.data == hash:
                    if fatherNode.right is not None:
                        return "1"+fatherNode.right.toHex() + " " + self.getProof(fatherNode, fatherNode.data)
                    # else:
                    #     return "00"+fatherNode.data + " " + self.getProof(fatherNode, fatherNode.data)
                else:
                    return "0"+fatherNode.left.toHex() + " " + self.getProof(fatherNode, fatherNode.data)

    def findNode(self, splitProof):
        leaf = self.root
        for i in range(len(splitProof)-1, 0, -1):
            if leaf.right is None:
                leaf = leaf.left
                continue
            if splitProof[i] == leaf.left.data:
                leaf = leaf.right
            elif splitProof[i] == leaf.right.data:
                leaf = leaf.left
            else:
                return ""
        return leaf

    def buildFatherData(self, leftData, rightData):
        return hashlib.sha256(leftData + rightData).hexdigest()

    def checkProofOfInclusion(self, stringOfLeaf, proof=None):
        if proof is None or proof == "" or proof == [] or proof == " ":
            return ""
        # splitProof = proof.split()
        splitProof = proof
        stringOfLeaf = get_hash(stringOfLeaf)
        for i in range(1, len(splitProof)):
            if splitProof[i][0:1] == "0":
                # if splitProof[i][0:2] == "00":
                #     stringOfLeaf = get_hash(stringOfLeaf)
                # else:
                stringOfLeaf = get_hash(splitProof[i][1:], stringOfLeaf)
            if splitProof[i][0:1] == "1":
                stringOfLeaf = get_hash(stringOfLeaf, splitProof[i][1:])
        if stringOfLeaf == splitProof[0]:
            return True
        else:
            return False

    def sign(self, key):
        key = serialization.load_pem_private_key(key.encode(), password=None)
        message = self.root.data.encode()
        # message = binascii.hexlify(message.encode())
        signature = key.sign(
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return binascii.b2a_base64(signature).decode()


    def verify(self, public_key, sign, text_verify):
        public_key = serialization.load_pem_public_key(public_key.encode())
        try:
           public_key.verify(
            binascii.a2b_base64(sign),
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

def find_depth(root):
    if root.left is None:
        return 1
    return 1 + find_depth(root.left)


def build_hash_leaves(node_array):
    for i in range(0, len(node_array), 1):
        hash = get_hash(node_array[i].data)
        node_array[i].data = hash
#uddd

def print_tree(root, level):
    if root is not  None:
        print_tree(root.right, level + 2)
        print(' ' * 5 * level + '-> ' +root.toHex()[0:3])
        print_tree(root.left, level + 2)


def build_tree(node_array):
    if len(node_array) == 2:
        hash = get_hash(node_array[0].data, node_array[1].data)
        root = Node(None, hash, node_array[0], node_array[1])
        node_array[0].father = root
        node_array[1].father = root
        return root
    if len(node_array) == 1:
        hash = node_array[0].data
        root = Node(data=hash)
        return root
    new_array = []
    i = 0
    for i in range(0, len(node_array)- 1, 2):
        hash = get_hash(node_array[i].data, node_array[i +1].data)
        node = Node(None, hash, node_array[i], node_array[i+1])
        node_array[i].father = node
        node_array[i+1].father = node
        new_array.append(node)
    if i < len(node_array)-2:
        # hash = get_hash(node_array[-1].data)
        # node = Node(None, hash, node_array[-1], None)
        # node_array[-1].father = node
        new_array.append(node_array[-1])
    return build_tree(new_array)


def get_hash(data1=None, data2=''):
    data1 = data1.encode()
    data2 = data2.encode()
    rootdata = hashlib.sha256()
    rootdata.update(data1)
    rootdata.update(data2)
    hash = rootdata.hexdigest()
    return hash

def getKeys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    public_key = private_key.public_key()
    pem_pub = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    # return pem.join(pem_pub) pem
    return (pem+b"\n"+pem_pub).decode()
    # return "-----BEGIN RSA PRIVATE KEY-----\n"+private_key+"\n-----END RSA PRIVATE KEY-----\n\n"+\
    #        "-----BEGIN PUBLIC KEY-----\n"+public_key+"\n-----END PUBLIC KEY-----"


merkle = MerkleTree()
while True:
    input_str = input()
    inputs = input_str.split(" ")
    choice = inputs[0]
    data = None
    data2 = None
    data3 = None
    if(len(inputs) > 1):
        data = inputs[1]
    if(len(inputs) > 2):
        data2 = inputs[2]
    if (len(inputs) > 3):
        data3 = inputs[3]
    if choice != "1" and merkle.root is None:
        print("")
        continue

    match choice:
        case "1":
            if data is None or data == " " or data == "":
                print("")
                continue
            merkle.addnode(data)
        case "2":
            print(merkle.calculateHexRoot())
        case "3":
            if data is None:
                print("")
                continue
            print(merkle.proofOfInclusion(int(data)))
        case "4":
            data = inputs[1]
            data2 = inputs[2:]
            if data is None or data2 is None:
                print("")
                continue
            print(merkle.checkProofOfInclusion(data, data2))
        case "5":
            print(getKeys())
        case "6":
            data = ' '.join(inputs[1:]) + "\n"
            temp_dat = input()
            while "-----END RSA PRIVATE KEY-----" not in temp_dat:
                data =  data + temp_dat + "\n"
                temp_dat = input()
            data = data + temp_dat
            print(merkle.sign(data))
        case "7":
            if data is None or data2 is None or data3 is None:
                print("")
                continue
            data = ' '.join(inputs[1:]) + "\n"
            temp_dat = input()
            while "-----END PUBLIC KEY-----" not in temp_dat:
                data = data + temp_dat + "\n"
                temp_dat = input()
            data = data + temp_dat + "\n"
            empty = input()
            sig_root = input().split(' ')
            data2 = sig_root[0]
            data3 = sig_root[1]
            print(merkle.verify(data, data2, data3))
        case "8":
            print_tree(merkle.root, 3)
        case _:
            print("")
            continue

