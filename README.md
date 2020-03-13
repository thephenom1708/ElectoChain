# ElectoChain
A Decentralised digital Voting System based on Blockchain architecture.

## Research Paper
A research paper has also been written on this project
[click here](https://github.com/thephenom1708/ElectoChain/blob/master/ElectoChain_paper.pdf)

## Technology-Stack:
* Front-End Development: HTML,CSS,Bootstrap,Vanilla JS,Jquery
* Data-Processing and Blockchain Development: Python 3.6.5
* Back-End Development: Django-Python Framework
* Database management: DB SQLite


## Voter Authentication :
* The voter authentication is carried out in two steps and it is implemented using Aadhaar API services.
* A voter has to provide his Thumb impression ID and Aadhaar ID to the system which will serve as an input to Aadhaar API.
* Aadhaar API will provide the result as a basic detail of the voter if he/her has been successfully authenticated.

## Vote Casting and Blockchain REST API Development:
* Here system will create a unique voter ID for the voter.
* Again the voter will cast a vote for any one of the candidate.
* After vote casting there are six different steps are carried out for which we have designed a special REST API:
  1. Transaction Verification
  2. Proof of Work Algorithm
  3. Block creation and Serialization
  4. Block Broadcasting and validation
  5. Consensus Algorithm
  6. Byzantine Fault Tolerance

## Peer to Peer (Distributed) Network Design:
* A peer to peer distributed network on which the blockchain architecture works.
* A Web Socket request API for broadcasting the all the requests into P2P network.
* Handling concurrency by using a mutex lock mechanism.


## Database Management:
* A relational DB SQLite is used as a database for the project.
* Many cryptographic and encryption algorithms are used to store the data securely in the database (SHA-256, CSPRNG, salt-hashing, etc).
* Complete normalization is also achieved in different relations of the database. 

## Admin Section:
* This panel is only reserved for the governing body of an election.
* Every admin is assigned a unique Election Commission ID for authentication.
* Result analysis of election is carried out in this section.

## Architectural Control flow of the System
![](https://lh4.googleusercontent.com/HRenn7pB3c3DhMpAW6Fz4WjdRh_T6L48rhsRoOebMjcjTkfPwNIVY-8ZxMVNxcSKAxWWbnl0_YW6NIe9q4mjzWOyCZunxG0c0df-x1JSpnbWX__2c4bmT3TDBjRrE9VuDosv5f2e)

## The operational flow of the System
![](https://lh4.googleusercontent.com/H5WDCtX38yu7UU36uf4e0PKrNFxR8TuuHNLWkIvYsA7K_u-3siu5foq1QDJ77hYsaC6HDd5QgGW8y-3U8fw1rwoTNqsmRx_fC98zbPeKyWGi4y3awailbTvVF1eM67Oe4UsI0nox)


## Steps to run the application:
1. Clone this repository.
2. Change this to working directory.
3. Hit command: "docker-compose up --build"
4. Go to http://localhost:5000/auth/ in your browser.

