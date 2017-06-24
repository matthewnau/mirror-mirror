import requests

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
