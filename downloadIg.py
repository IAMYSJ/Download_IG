#! python3
# downloadIg.py

import sys
import requests
import json
import os
from bs4 import BeautifulSoup

# Make folder
os.makedirs('image', exist_ok=True)

start = True

while start:
	url = input('Please enter IG url(Enter q to leave): ')
	if url == 'q' or url == 'Q':
		start = False
		print('Goodbye...')
		sys.exit()
	try:
		# Build BeautifulSoup
		res = requests.get(url)
		res.raise_for_status()
		soup = BeautifulSoup(res.text, 'html.parser')
		
		# Resolve BeautifulSoup
		jsText = soup.findAll("script", {"type": "text/javascript"})
		result = jsText[2].string
		resultSize = len(result)
		result = result[21:resultSize-1]
		jsonResult = json.loads(result)
		data = jsonResult['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges']
	except:
		print('This is not IG url!')
	else:
		if data == []:
			print('The account is private!')
		else:
			for i in range(len(data)):
				# Image url
				url = jsonResult['entry_data']['ProfilePage'][0]['graphql']['user']['edge_owner_to_timeline_media']['edges'][i]['node']['display_url']
				print('Downlaoding image %s...' % (url))
				try:
					# Get image
					res = requests.get(url)
					res.raise_for_status()
				except requests.exceptions.MissingSchema:
					print('Some error...')
					break
				# Download
				imageFile = open(os.path.join('image', os.path.basename(url)), 'wb')
				for chunk in res.iter_content(100000):
					imageFile.write(chunk)

			imageFile.close()
			print('Done...')
