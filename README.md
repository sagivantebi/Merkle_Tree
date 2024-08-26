



# Merkle Tree with RSA Signature Verification

This project implements a Merkle Tree structure in Python with the ability to generate cryptographic proofs and verify them using RSA keys. The Merkle Tree is a binary tree where each node contains the hash of the concatenation of its child nodes. The implementation includes functions to build the tree, generate proofs, and verify signatures.

![Merkle-Tree-1](https://user-images.githubusercontent.com/84729141/172680878-3ba2eef2-1766-4f5e-af20-e72153207f59.png)


## Features

- **Build Merkle Tree**: Construct a Merkle Tree from a list of leaves, each representing data values.
- **Generate Proofs**: Generate a cryptographic proof for any leaf in the Merkle Tree.
- **Sign Root Hash**: Sign the root hash of the Merkle Tree using RSA private keys.
- **Verify Signatures**: Verify the signature of the Merkle Tree root hash using RSA public keys.
- **Interactive Menu**: An interactive console menu to perform all operations.

## Requirements

- Python 3.x
- `cryptography` library

You can install the required package using pip:
```bash
pip install cryptography
```

## How to Use

1. **Building the Merkle Tree:**
   - Select option `1` from the menu and input the values of the leaves.

2. **Displaying the Merkle Tree Root Hash:**
   - Select option `2` to display the root hash of the current Merkle Tree.

3. **Generate a Proof for a Node:**
   - Select option `3` and input the index of the leaf for which you want to generate a proof.

4. **Compare a Given Proof:**
   - Select option `4` to compare an external proof with the generated proof.

5. **Generate RSA Keys:**
   - Select option `5` to generate a pair of RSA public and private keys.

6. **Sign the Merkle Tree Root Hash:**
   - Select option `6` to sign the root hash with a private RSA key.

7. **Verify a Signature:**
   - Select option `7` to verify the signature of the Merkle Tree root hash using a public RSA key.

## Example

```bash
1. Input Leaf: 'Leaf1'
2. Input Leaf: 'Leaf2'
3. Build Merkle Tree
4. Display Root Hash
5. Generate Proof for Leaf Index 0
6. Sign Root Hash
7. Verify Signature
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Sagiv Antebi
