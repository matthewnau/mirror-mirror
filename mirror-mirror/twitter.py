import requests

def scrape_twitter(username):
    #start a new web-browsing session
    s = requests.session()

    #make containers for all the links to be collected
    messy_links, clean_links = [],[]

    #using the user's username, download the file containing the links to the last 3200 pictures ever posted
    user_links_page = s.get('https://twitter.com/i/profiles/show/'+username+'/media_timeline.json?count=3200')
    user_links_page = user_links_page.text.split('"')

    #collect the url of every possible jpg picture, find the uncompressed url
    for link in user_links_page:
        link = ''.join(link.split('\\'))
        if link.endswith('.jpg'):
            if link.startswith('https://pbs.twimg.com/media/') or \
               link.startswith('https://pbs.twimg.com/tweet_video_thumb/') or \
               link.startswith('https://pbs.twimg.com/ext_tw_video_thumb/'):
                messy_links.append(link + ':orig')

    #make sure there are no duplicate links
    for link in messy_links:
        if link not in clean_links:
            clean_links.append(link)

    #check if the account has any pictures associated with it
    if len(clean_links) > 0:

        #profile picture is compressed regardless, remove it
        if 'profile_images' in clean_links[0]:
            clean_links.pop(0)

    #terminate the browsing session
    s.close()

    #return all the decompressed image links
    return clean_links
