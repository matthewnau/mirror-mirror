import requests

def scrape_instagram(username):
	#start a new web-browsing session
	s = requests.session()

	#make containers for all the links to be collected
	messy_links, clean_links = [],[]

	#download the user's profile page
	profile_page = s.get('http://instagram.com/'+username).text

	#test if the user's account is private
	if '"is_private": true' in profile_page:
		user_links_page = profile_page.split('"')

	#otherwise, get all the other images
	else:
		profile_page = profile_page.split('"owner": {"id": "')

		#get the user's unique user id from the profile page
		unique_user_id = profile_page[1][0:profile_page[1].index('"')]

		#get the dynamically created javascript file's temporary unique pathway
		unique_commons_js = profile_page[12].split("en_US_Commons.js/")[1]
		unique_commons_js = unique_commons_js[0:unique_commons_js.index('.js')]

		#download the dynamically generated javascript page to get the unique session id
		javascript_page = s.get('https://www.instagram.com/static/bundles/en_US_Commons.js/'+unique_commons_js+'.js')
		javascript_page = javascript_page.text.split('return e.profilePosts.byUserId.get(t).pagination},queryId:"')[1]

		#get the unique session id from the javascript page
		unique_session_id = javascript_page[0:javascript_page.index('"')]

		#using the session and user id's, download the file containing the links to all pictures ever posted
		user_links_page = s.get("https://www.instagram.com/graphql/query/?query_id="+unique_session_id+"&id="+unique_user_id+"&first=1000000")
		user_links_page = user_links_page.text.split('"')

	#append every jpg picture url to the "messy links"
	for link in user_links_page:
		if ".jpg" in link:
			messy_links.append(link)

	#find the uncompressed links to the images provided
	for link in messy_links:
		segmented_link = link.split("/")
		unique_post_id = link[::-1][:link[::-1].index("/")][::-1]
		clean_link = "https://"+segmented_link[2]+"/"+segmented_link[3]+"/"+unique_post_id
		if clean_link not in clean_links:
			clean_links.append(clean_link)

	#terminate the browsing session
	s.close()

	#return all the decompressed image links
	return clean_links
