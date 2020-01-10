from flask import Flask, jsonify, request
from uuid import uuid4
from .blockChain import BlockChain
import json
import hashlib


app = Flask(__name__)
blockchain = BlockChain()
node_identifier = str(uuid4()).replace('-', '')


@app.route('/mine', methods=['GET'])
def mine():
    values = request.getjson()

    last_block = blockchain.last_block

    #Reward for minining
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )

    new_proof = blockchain.proof_of_work(last_block['proof'])
    prev_hash = blockchain.hash(last_block)

    block = blockchain.new_block(prev_hash, new_proof)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.getjson()
    blockchain.new_transaction(values.sender, values.recepit, values.ammount)
    return 'posting new transaction'

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000)

