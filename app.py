from flask import Flask, jsonify, request
from uuid import uuid4
from blockChain import *
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
        return 'bet matched, announcing to chain'
    return 'posting new NBA bet'


@app.route('/chain', methods=['GET'])
def full_chain():
    chain_info = []
    for block in blockchain.chain:
        chain_info.append(block.toJSON())
    response = {
        'chain': chain_info,
        'length': len(blockchain.chain),
        'peers': list(peers)
    }
    return jsonify(response), 200


@app.route('/register_node', methods=['POST'])
def register_new_peers():
    node_address = request.get_json()['node_address']
    if not node_address:
        return "Invalid Data", 404
    peers.add(node_address)
    return full_chain()


@app.route('/register_with', methods=['POST'])
def register_with_existing_node():
    node_address = request.get_json()["node_address"]

    if not node_address:
        return "Invalid data", 400
    data = {"node_address": request.host_url}
    headers = {"Content-Type": "application/json"}

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


@app.route('/add_block', methods=['POST'])
def verify_and_add_block():
    block_data = request.get_json()
    block = Block(block_data["index"],
                  block_data["timestamp"],
                  block_data["wagers"],
                  block_data["previous_hash"],)
    added = blockchain.add_block(block)
    if not added:
        return "The block was discarded by the node", 400

    return "Block added to the chain", 201

def announce_new_block(block):
    for peer in peers:
        url = "{}add_block".format(peer)
        headers = {"Content-Type": "application/json"}
        requests.post(url, data=block.toJSON(), headers=headers)


if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000)

