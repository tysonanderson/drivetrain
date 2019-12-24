import requests, pprint, time, json
from bs4 import BeautifulSoup
from pymongo import MongoClient

# start db connection
client = MongoClient('mongodb+srv://')
db=client.drivetrain

cursor = db.brand.find()

def get_details(url):

	# get product detail page; parse table
	full_url = 'https://brandurl.com{}'.format(url)
	r = requests.get(full_url)
	soup = BeautifulSoup(r.text)

	th = [x.text for x in soup.find_all('th')]
	td = [x.text for x in soup.find_all('td')]

	# combine elements to dict
	if len(th) == len(td):
		dictionary = dict(zip(th,td))
		return dictionary
	else:
		# data integrity check
		raise Exception('Data elements do not match')

# write details to db
def write_details(element):
	db.brand.update_one({'_id': element['_id']}, {'$set': {'details': get_details(element['url'])}})
	print(element['name'])

	# rate limiter
	time.sleep(3)

[write_details(x) for x in cursor]