# get product urls from json

import requests, pprint, time
from pymongo import MongoClient

# initialize db connection
client = MongoClient('mongodb+srv://')
db=client.drivetrain

# product category ids
categories = [('cassette','cg3SHICCassetteSprocket'),
			('crankset', 'cg3SHICCrankset'),
			('shift_lever', 'cg3SHICShiftLever'),
			('front_derailleur', 'cg3SHICFrontDerailleur'),
			('chain', 'cg3SHICChain'),
			('brifter', 'cg3SHICShiftBrakeLever'),
			('rear_derailleur', 'cg3SHICRearDerailleur')]

url = 'https://brandurl.com'

riding_style = ['bc2017Road', 'bc2017MTB']

# write product to db
def write_products(product_list, category, style):
	for product in product_list:
		product['style'] = style
		product['category'] = category
		result=db.brand.insert_one(product)
		print(product['name'])

# get all products from multi-page listing
def get_products(style, category):
	print(style)
	pages = 1

	while pages > 0:
		r = requests.get(url.format(category[1], style, pages))
		if(r.json()['status']):
			pages += 1
			write_products(r.json()['products'], category[0], style)
		else:
			pages = 0
		# rate limiter
		time.sleep(3)

# get all categories for each riding style
def get_categories(category):
	print(category[0])
	[get_products(x, category) for x in riding_style]


[get_categories(x) for x in categories]