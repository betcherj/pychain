## Blockchain bets 
Jack Betcher and Peter Bromley 

### Proposal
In this project hope to implement a block chain based sports betting ledger in order to learn
associated new concepts and technologies. We plan to use a python implementation of the block chain 
as well as Flask with postman for our API interaction. The nodes of our block chain will contain signed bets allowing for a verifiable record without the need for a third party.  

To start the server 

```flask run -h "$HOST" -p "$PORT"```

View the full chain 

```curl http://$HOST:$PORT/chain```

Register with peers (Need to register all pairs of peers) 

```curl -X POST -H "Content-Type: application/json" -d "{\"node_address\" : \"http://$DESTHOST:$DESTPORT\"}" "http://$HOST:$PORT/register_with"```

Post Bets

```curl -X POST -H "Content-Type: application/json" -d "{\"team1\": \"cavaliers\", \"team2\": \"lakers\", \"date\": 20190102, \"winner\": \"cavaliers\", \"amount\": 10}" "http://$HOST:$PORT/bet/new"```
