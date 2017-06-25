#!/usr/bin/env python3

import requests
import json
import html
import re

URL = r'https?://[-\._:a-z0-9]+/[-\._:%\?=&/\\,;\+~#a-z0-9]+'
ALL_URL = re.compile('^'+URL+'$', re.I)
URLS = re.compile(URL, re.I)
TWITER_SIZE = re.compile(r':[a-z]+$')


def scrape_instagram(username):
	#start a new web-browsing session
	s = requests.session()

	#make containers for all the links to be collected
	messy_links, clean_links = [],[]

	#download the user's profile page
	profile_page = s.get('http://instagram.com/'+username).text

	#check if account exists
	if '<body class=" p-error dialog-404">' not in profile_page:

		#test if the user's account is private
		if '"is_private": true' in profile_page:
			user_links_page = profile_page.split('"')

		#otherwise, get all the other images
		else:
			profile_page = profile_page.split('"owner": {"id": "')

			#get the user's unique user id from the profile page
			unique_user_id = profile_page[1][:profile_page[1].index('"')]

			#get the dynamically created javascript file's temporary unique pathway
			unique_commons_js = profile_page[len(profile_page)-1].split('en_US_Commons.js/')[1]
			unique_commons_js = unique_commons_js[:unique_commons_js.index('.js')]

			#download the dynamically generated javascript page to get the unique session id
			javascript_page = s.get('https://www.instagram.com/static/bundles/en_US_Commons.js/'+unique_commons_js+'.js')
			javascript_page = javascript_page.text.split('return e.profilePosts.byUserId.get(t).pagination},queryId:"')[1]

			#get the unique session id from the javascript page
			unique_session_id = javascript_page[:javascript_page.index('"')]

			#using the session and user id's, download the file containing the links to all pictures ever posted
			user_links_page = s.get('https://www.instagram.com/graphql/query/?query_id='+unique_session_id+'&id='+unique_user_id+'&first=1000000')
			user_links_page = user_links_page.text.split('"')

		#collect the url of every possible jpg picture
		for link in user_links_page:
			if '.jpg' in link:
				messy_links.append(link)

		#find the uncompressed links to the images provided, and clean them up
		for link in messy_links:
			segmented_link = link.split('/')
			unique_post_id = link[::-1][:link[::-1].index('/')][::-1]
			clean_link = 'https://'+segmented_link[2]+'/'+segmented_link[3]+'/'+unique_post_id
			if clean_link not in clean_links:
				clean_links.append(clean_link)

	#terminate the browsing session
	s.close()

	#return all the decompressed image links
	return clean_links

def links_from_json(json):
	tp = type(json)
	if tp == str:
		if ALL_URL.match(json):
			yield json
		else:
			for url in URLS.findall(json):
				yield html.unescape(url)

	elif tp == list:
		for item in json:
			yield from links_from_json(item)

	elif tp == dict:
		for item in json.values():
			yield from links_from_json(item)

def scrape_twitter(username):
	#start a new web-browsing session
	s = requests.session()

	try:
		#make containers for all the links to be collected
		seen_links = set()
		links = []

		#using the user's username, download the file containing the links to the last 3200 pictures ever posted
		user_links_page = s.get('https://twitter.com/i/profiles/show/'+username+'/media_timeline.json?count=3200')
		user_links_page = json.loads(user_links_page.text)

		#collect the url of every possible jpg picture
		for link in links_from_json(user_links_page):
			link = TWITER_SIZE.sub('', link)
			if link.endswith('.jpg'):
				if link.startswith('https://pbs.twimg.com/media/') or \
				   link.startswith('https://pbs.twimg.com/tweet_video_thumb/') or \
				   link.startswith('https://pbs.twimg.com/ext_tw_video_thumb/'):
					link = link + ':orig'

				if link not in seen_links:
					links.append(link)
					seen_links.add(link)

		#check if the account has any pictures associated with it
		if links:

			#profile picture is compressed regardless, remove it
			if 'profile_images' in links[0]:
				links.pop(0)


		#return all the decompressed image links
		return links

	finally:
		#terminate the browsing session
		s.close()

def scrape_vsco(username):
	#start a new web-browsing session
	s = requests.session()

	#make containers for all the links to be collected
	messy_links, clean_links = [],[]

	#download the user's profile page
	profile_page = s.get('http://vsco.co/'+username)

	#check if account exists
	if '<p class="page-error-heading mt40">This page does not exist</p>' not in profile_page.text:

		#get the unique session id from the site's cookies
		unique_session_id = str(profile_page.cookies).split('vs=')[1]
		unique_session_id = unique_session_id[:unique_session_id.index(' ')]

		#convert the profile page to a string
		profile_page = profile_page.text

		#get the user's unique user id from the profile page
		unique_user_id = profile_page.split('"id":')[1]
		unique_user_id = unique_user_id[:unique_user_id.index(',')]

		#find the user's profile picture link
		profile_picture_link = profile_page.split('responsive_url":"')[1]
		profile_picture_link = profile_picture_link[:profile_picture_link.index('"')]
		
		#add the profile picture link to the list
		messy_links.append('http://'+profile_picture_link)

		#using the session and user id's, download the file containing the links to all pictures ever posted
		user_links_page = s.get('http://vsco.co/ajxp/'+unique_session_id+'/2.0/medias?site_id='+unique_user_id+'&page=1&size=10000').text.split('"')

		#collect the url of every possible jpg picture
		for link in user_links_page:
			if ((('im.vsco.co' in link) and ('.jpg' in link))):
				messy_links.append('http://'+link)

		#find the uncompressed links to the images provided, and clean them up
		for link in messy_links:
			clean_links.append(link.replace('\\',''))

	#terminate the browsing session
	s.close()

	#return all the decompressed image links
	return clean_links

def scrape_tinder(username):
	#start a new web-browsing session
	s = requests.session()

	#make containers for all the links to be collected
	messy_links, clean_links = [],[]

	#download the user's profile page
	profile_page = s.get('https://www.gotinder.com/@'+username)

	#check if account exists
	if "<h1 id='title'>Looking for Someone?</h1>" not in profile_page:

		#convert the profile page to a list
		profile_page = profile_page.text.split('"')

		#collect the url of every possible jpg picture
		for link in profile_page:
			if '.jpg' in link:
				messy_links.append(link)

		#find the uncompressed links to the images provided, and clean them up
		for link in messy_links:
			clean_link = '/'.join(link.split('&#x2F;'))
			if clean_link not in clean_links:
				clean_links.append(clean_link)

		#check if the account has any pictures associated with it
		if len(clean_links) > 0:

			#remove the picture that's not user related
			clean_links.pop(1)

	#terminate the browsing session
	s.close()

	#return all the decompressed image links
	return clean_links

if __name__ == '__main__':
	import sys
	if len(sys.argv) < 3:
		sys.stderr.write('usage: mirror-mirror.py <service> <username...>\n')
		sys.exit(1)
	else:
		service = sys.argv[1].lower()

		if service == 'instagram':
			scrape = scrape_instagram

		elif service == 'twitter':
			scrape = scrape_twitter

		elif service == 'vsco':
			scrape = scrape_vsco

		elif service == 'tinder':
			scrape = scrape_tinder

		else:
			sys.stderr.write('unknown service: %s\n' % service)
			sys.exit(1)

		for username in sys.argv[2:]:
			for link in scrape(username):
				print(link)
