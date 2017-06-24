import requests

def scrape_vsco(username):
	#start a new web-browsing session
	s = requests.session()

	#make containers for all the links to be collected
	messy_links, clean_links = [],[]

	#download the user's profile page
	profile_page = s.get('http://vsco.co/'+username)

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
