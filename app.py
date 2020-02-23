from flask import Flask, jsonify, request
from uuid import uuid4
from blockChain import BlockChain, Block
import json
import hashlib
import wager
import sportsEvent

app = Flask(__name__)
blockchain = BlockChain()
node_identifier = str(uuid4()).replace('-', '')
peers = set()


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

@app.route('/register_node', methods=['POST'])
def register_with_peers():
    nodes = request.get_json()['node_address']
    if not nodes:
        return "Invalid Data", 404
    for node in nodes:
        peers.add(node)

    return full_chain

@app.route('/register_with_node', mehoods=["POST"])
def register_with_node():
    node_address = request.get_json()['node_address']
    if not node_address:
        return "Error node address not found", 404
    data = {'node_address': request.host_url}
    headers = {'Content type': 'applications/json'}

    response = request.post(node_address + '/register_node', data=json.dumps(data), headers=json.dumps(headers))

@app.route('/add_block', methods=["POST"])
def validate_and_add_block():
    block_data = request.get_json()
    block = Block(block_data['index'], block_data['time'], block_data['wagers'], block_data['previous_hash'])
    if blockchain.new_block(block):
        return "Block added to the chain", 200
    else:
        return "Error block discarded", 400

@app.route('/pending_bets')
def get_pending_tx():
    return json.dumps(blockchain.current_unmatched_bets)




if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000)

