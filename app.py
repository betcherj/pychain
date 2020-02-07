from flask import Flask, jsonify, request
from uuid import uuid4
from blockChain import BlockChain
import json
import hashlib
import wager
import sportsEvent

app = Flask(__name__)
blockchain = BlockChain()
node_identifier = str(uuid4()).replace('-', '')


@app.route('/mine', methods=['GET'])
def mine():
    values = request.get_json()

    last_block = blockchain.last_block

    new_proof = blockchain.proof_of_work(last_block['proof'])
    prev_hash = blockchain.hash(last_block)

    block = blockchain.new_block(prev_hash, new_proof)

    response = {
        'message': "New Block Forged",
        'index': block['index'],
        'wagers': block['wagers'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }

    return jsonify(response), 200

@app.route('/bet/new', methods=['POST'])
def new_NBA_bet():
    values = request.get_json()

    event = sportsEvent.SportsEvent('nba', [values['team1'], values['team2']], values['date'])
    new_wager = wager.Wager('bob', event, values['winner'], values['amount'])
    blockchain.new_bet(new_wager)

    return 'posting new NBA bet'

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000)

