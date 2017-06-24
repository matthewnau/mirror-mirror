import requests

def scrape_twitter(username):
	#start a new web-browsing session
	s = requests.session()

	#make containers for all the links to be collected
	messy_links, clean_links = [],[]

	#using the user's username, download the file containing the links to the last 3200 pictures ever posted
	user_links_page = s.get('https://twitter.com/i/profiles/show/'+username+'/media_timeline.json?count=3200')
	user_links_page = user_links_page.text.split('"')

	#collect the url of every possible jpg picture
	for link in user_links_page:
		if '.jpg' in link:
			messy_links.append(link)

	#find the uncompressed links to the images provided, and clean them up
	for link in messy_links:
		clean_link = ''.join(link.split('\\'))
		if clean_link not in clean_links:
			clean_links.append(clean_link)

	#check if the account has any pictures associated with it
	if len(clean_links) > 0:

		#profile picture is compressed regardless, remove it
		if 'profile_images' in clean_links[0]:
			clean_links.pop(0)

	#if the user has no pictures, add the default picture
	else:
		clean_links.append('https://abs.twimg.com/sticky/default_profile_images/default_profile.png')

	#terminate the browsing session
	s.close()

	#return all the decompressed image links
	return clean_links
