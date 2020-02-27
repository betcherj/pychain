## Blockchain bets 
Jack Betcher and Peter Bromley 

### Proposal
In this project hope to implement a block chain based sports betting ledger in order to learn
associated new concepts and technologies. We plan to use a python implementation of the block chain 
as well as Flask with postman for our API interaction. The nodes of our block chain will contain signed bets allowing for a verifiable record without the need for a third party.  


post requests
```curl -X POST -H "Content-Type: application/json" -d '{"team1": "cavaliers", "team2": "lakers", "date": 20190102, "winner": "cavaliers", "amount": 10}' "http://localhost:5000/bet/new"```
