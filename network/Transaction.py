import hashlib
import random
import secrets
import time
import json


class Transaction:
	def __init__(self,voterId,candidateId):
		self.voterId=voterId
		self.salt=secrets.token_hex(5)
		self.candidateHash=hashlib.sha256((str(candidateId)+str(self.salt)).encode()).hexdigest()

	def displayEmployee(self):
		print("VoterId %d candidateHash %s Salt %s" %(self.voterId,self.candidateHash,self.salt))



class Block:
	blockcount=0
	def __init__(self,Transaction,previousHash):
		self.timeStamp=str(time.time())
		self.previousHash=str(previousHash)
		self.transaction=str(Transaction.voterId)+str(Transaction.salt)+str(Transaction.candidateHash)
		self.nonce=0;
		self.difficulty=5;
		#self.hash=hashlib.sha256((str(self.timeStamp)+str(previousHash)+str(self.transaction)).encode()).hexdigest()
		self.hash=self.calculatehash()
		Block.blockcount=Block.blockcount+1

	def displayBlock(self):
		print("TimeStamp %s  previousHash %s  hash %s blockcount %d" %(self.timeStamp,self.previousHash,self.hash,Block.blockcount))



	def calculatehash(self):
		return hashlib.sha256((str(self.timeStamp)+str(self.previousHash)+str(self.transaction)+str(self.nonce)).encode()).hexdigest()


	def mineBlock(self):
		target=str('0'*self.difficulty)
		while str(self.hash[:self.difficulty])!=target:
			self.nonce=self.nonce+1
			self.hash=self.calculatehash()

		print("Block Mined: %s"%(self.hash))



def is_Valid(my_objects):
	for i in range(1,len(my_objects)):
		first=my_objects[i-1]
		second=my_objects[i]
		# print("FirstHash: "+first.hash+"Second Hash: "+second.previousHash+"\n")
		# print("Hash: "+second.hash+"Prev: "+Block.calculatehash(second))

		if first.hash!=second.previousHash or second.hash!=Block.calculatehash(second):
			return False

		return True

def save_data(blockchain):
	with open('blockchain.txt',mode='w')as f:
		f.write(str(blockchain))






if __name__ == '__main__':
	
	my_objects=[]

	tr = Transaction(1,6)
	#tr.displayEmployee()
	#print(tr.__dict__)
	tr2 = Transaction(1,6)
	#tr2.displayEmployee()

	tr3=Transaction(2,7)
	#tr3.displayEmployee()

	if Block.blockcount==0:
		bl=Block(tr,0)

	my_objects.append(bl)
	#my_objects[0].displayBlock()
	my_objects[0].mineBlock()
	#save_data(k=json.dumps(my_objects[0].__dict__))
	my_objects[0].displayBlock()
	bl2=Block(tr2,my_objects[-1].hash)
	#print(json.dumps(bl2.__dict__))
	#bl2.displayBlock()
	my_objects.append(bl2)
	my_objects[1].mineBlock()
	#save_data(my_objects)
	my_objects[1].displayBlock()
	bl2.timeStamp=4245
	# bl2.displayBlock()
	bl3=Block(tr3,my_objects[-1].hash)
	#bl3.displayBlock()
	my_objects.append(bl3)
	my_objects[2].mineBlock()
	#save_data(my_objects)
	my_objects[2].displayBlock()

	v=is_Valid(my_objects)
	if v:
		print("BlockChain is valid")
	else:
		print("BlockChain is Invalid")

	# target=str('0'*5)
	# print(target)
