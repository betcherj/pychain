from flask import Flask, jsonify, request
from uuid import uuid4
from blockChain import BlockChain, Block
import json
import wager
import sportsEvent
import requests

app = Flask(__name__)
blockchain = BlockChain()

node_identifier = str(uuid4()).replace('-', '')
peers = set()


@app.route('/bet/new', methods=['POST'])
def new_NBA_bet():
    values = request.get_json()
    event = sportsEvent.SportsEvent('nba', [values['team1'], values['team2']], values['date'])
    new_wager = wager.Wager('bob', event, values['winner'], values['amount'])
    if blockchain.new_bet(new_wager):
        announce_new_block(blockchain.last_block)
    return 'posting new NBA bet'


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200


@app.route('/add_nodes', methods=['POST'])
def register_new_peers():
    nodes = request.get_json()['node_address']
    if not nodes:
        return "Invalid Data", 404
    for node in nodes:
        peers.add(node)
    return full_chain()


@app.route('/register_with', methods=['POST'])
def register_with_existing_node():
    node_address = request.get_json()["node_address"]
    if not node_address:
        return "Invalid data", 400
    data = {"node_address": request.host_url}
    headers = {'Content-Type': "application/json"}
    response = requests.post(node_address + "/register_node", data=json.dumps(data), headers=headers)

    if response.status_code == 200:
        global blockchain
        global peers
        chain_dump = response.json()['chain']

        blockchain = create_chain_from_dump(chain_dump)

        peers.update(response.json()['peers'])

        return "Registration successful", 200
    else:
        return response.content, response.status_code



@app.route('/add_block', methods=["POST"])
def validate_and_add_block():
    block_data = request.get_json()

    block = Block(block_data['index'], block_data['time'], block_data['wagers'], block_data['previous_hash'])
    if consensus() and blockchain.wagers_aligned(block.wagers[0], block.wagers[1]):
        blockchain.add_block(block)
        return "Block added to the chain", 200
    else:
        return "Error block discarded", 400

@app.route('/pending_bets')
def get_pending_tx():
    return json.dumps(blockchain.current_unmatched_bets)


def create_chain_from_dump(chain_dump):

    generated_blockchain = BlockChain()

    for idx, block_data in enumerate(chain_dump):
        if idx == 0:
            continue
        block = Block(block_data["index"], block_data["time"], block_data["wagers"], block_data["previous_hash"])
        added = generated_blockchain.add_block(block)

        if not added:
            raise Exception("Error: Chain Dump Failure")

    return generated_blockchain


def consensus():
    '''If block is part of longest chain we add it to our chain'''
    global blockchain
    longest_chain = None
    current_len = len(blockchain)
    for node in peers:
        response = requests.get('http://{}/chain'.format(node))
        length = response.json()['length']
        chain = response.json()['chain']
        if length > current_len and blockchain.check_chain_validity(chain):
            current_len = length
            longest_chain = chain
    if longest_chain:
        blockchain = longest_chain
        return True
    return False

def announce_new_block(block):
    for peer in peers:
        url = "http://{}/add_block".format(peer)
        requests.post(url, data=json.dumps(block.__dict__, sort_keys=True))





if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000)

