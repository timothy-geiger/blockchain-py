from uuid import uuid4
from flask import Flask, jsonify, request
from blockchain import Blockchain


# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


# Mine endpoints -> tells the server to mine a new block
@app.route('/mine', methods=['GET'])
def mine():
    # calculate new proof
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # add transaction to the miner
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    # create new block
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }

    return jsonify(response), 200


# create a new transaction with the specified data
@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()
    required = ['sender', 'recipient', 'amount']

    # check if all necessary information are spcified
    if not all(k in values for k in required):
        return 'Missing values', 400

    # create a new transaction
    idx = blockchain.new_transaction(
        values['sender'],
        values['recipient'],
        values['amount'])

    response = {'message': f'Transaction will be added to Block {idx}'}

    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
