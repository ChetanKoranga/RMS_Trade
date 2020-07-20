import pymongo
from pymongo import MongoClient


client=MongoClient()

db=client['cum_ideas_ch']


collection=db['cols']


post={
		"symbol":"tcse",
		"algo_name":"algo1",
		"quantity":20


}
print("bye")


if not db['cols'].find_one({}):
	print("hello")

	db['cols'].insert(post)
else:
	print("hellos")
	for i in db['cols'].find({}):
		print(i)
		
		conc=i['symbol']+i['algo_name']
		# print(conc)
		conc_2=post['symbol']+post['algo_name']
		# print(conc_2)
		if conc==conc_2:
			# print("hello")
			i['quantity']+=post['quantity']
		else:
			db['cols'].insert(post)