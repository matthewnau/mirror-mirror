import requests

def scrape_okcupid(username):
	#start a new web-browsing session
	s = requests.session()

	#make containers for all the links to be collected
	messy_links, clean_links = [],[]

	#download the user's profile page
	profile_page = s.get('https://www.okcupid.com/profile/'+username).text.encode('utf-8')
	profile_page = str(str(profile_page).split("'")).split('"')

	#check if account exists
	if '<title>Account not found | OkCupid</title>' not in str(profile_page):
		
		#collect the url of every possible jpg picture
		for link in profile_page:
			if ('.jpeg' in link) and ('/images/' in link):
				messy_links.append(link)

		#choose the first cdn server available to prevent duplicate images
		chosen_cdn_server = messy_links[0][:messy_links[0].index('/images')]

		#find the uncompressed links to the images provided, and clean them up
		for link in messy_links:
			clean_link = chosen_cdn_server+'/images/'+link[::-1][:link[::-1].index('/')][::-1]
			clean_link = clean_link[::-1][clean_link[::-1].index('.')+1:][::-1]+'.jpeg'
			if clean_link not in clean_links:
				clean_links.append(clean_link)

	#terminate the browsing session
	s.close()

	#return all the decompressed image links
	return clean_links
