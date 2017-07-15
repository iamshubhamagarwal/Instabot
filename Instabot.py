#Import required libraries
import requests,urllib
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer

#Access_Token And Base_Url
APP_ACCESS_TOKEN='2118448589.f3bbef4.dea6f123620e4b1b8228b6963d848e19'
BASE_URL = 'https://api.instagram.com/v1/'

#Method to print own info
def self_info():
 try:
    request_url=BASE_URL+'users/self/?access_token='+APP_ACCESS_TOKEN
    print "GET request url: %s" %(request_url)                               #Prints get requests url
    user_info=requests.get(request_url).json()                    #Stores json objects
 except:
   print "Request url is not working proper. Please Try again."
   if user_info['meta']['code'] == 200:                                            #Checks if meta code is 200
         if len(user_info['data']):              #Check the user info is valid or not
                print ('Username: %s') % (user_info['data']['username'])
                print ('No. of followers: %s',) % (user_info['data']['counts']['followed_by'])
                print ('No. of people you are following: %s') % (user_info['data']['counts']['follows'])
                print ('No. of posts: %s')% (user_info['data']['counts']['media'])
                print ('Short Bio: %s') %(user_info['data']['bio'])
         else:
                print 'User does not exist!'
 else:
         print 'Status code other than 200 received!'               #It means eveything is ok


#Function declaration to get the ID of a user by username
def get_user_id(insta_username):
        request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, APP_ACCESS_TOKEN)
        print 'GET request url : %s' % (request_url)
        user_info = requests.get(request_url).json()
        try:
            if user_info['meta']['code'] == 200:
                if len(user_info['data']):
                    return user_info['data'][0]['id']   #Returns id to the uesrs
                else:
                    return None                    #Returns none if the info is not found
            else:
                print 'Status code other than 200 received!'
                exit()                                  #exits if status other than 200
        except KeyError:
            print "Unable to process your request. Please try again!!"


#Function to get user info by username
def get_user_info(insta_username):
        user_id = get_user_id(insta_username)
        if user_id == None:                                 #Checks if username is valid or not
            print 'User does not exist!'
            exit()
        request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
        print 'GET request url : %s' % (request_url)            #Prints get requests url
        user_info = requests.get(request_url).json()

        if user_info['meta']['code'] == 200:
            try:
                if len(user_info['data']):
                    print ('Username: %s') % (user_info['data']['username'])
                    print ('No. of followers: %s') % (user_info['data']['counts']['followed_by'])
                    print ('No. of people %s are following: %s') % (user_info['data']['username'],user_info['data']['counts']['follows'])
                    print ('No. of posts: %s') % (user_info['data']['counts']['media'])
                else:
                    print 'There is no data for this user!'
            except KeyError:
                print "Unable to process your request. Please try again!!"
        else:
            print 'Status code other than 200 received!'        #Check Status of code is 200


#Function to get own recent post and downld the images
def get_own_post():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    own_media = requests.get(request_url).json()
    if own_media['meta']['code'] == 200:
        try:
            if len(own_media['data']):
                image_name = own_media['data'][0]['id'] + '.jpg'       #Name of the images
                image_url = own_media['data'][0]['images']['standard_resolution']['url']              #url of the images
                urllib.urlretrieve(image_url, image_name)
                print 'Your image has been downloaded!'
            else:
                print 'Post does not exist!'
        except KeyError:                                                     #Give the error if put wrong details
            print "Unable to process your request. Please try again!!"
    else:
        print 'Status code other than 200 received!'


#Function to get users post
def get_user_post(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)              #Get request the info from the url
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)                         #It take the image from the user url and download it
            print 'Your image has been downloaded!'
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'


#Function to get post id
def get_post_id(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()
    if user_media['meta']['code'] == 200:
        try:
            if len(user_media['data']):
                return user_media['data'][0]['id']
            else:
                print 'There is no recent post of the user!'                 #Check the recent post of the user
                exit()
        except KeyError:
            print "Unable to process your request. Please try again!!"
    else:
        print 'Status code other than 200 received!'
        exit()


#Function to get the list of users
def get_like_list(insta_username):
    post_id = get_post_id(insta_username)
    if post_id == None:
        print 'User does not exist!'
        exit()
    try:
        request_url=(BASE_URL+'media/%s/likes?access_token=%s') %(post_id,APP_ACCESS_TOKEN)
        print 'GET request url : %s' % (request_url)
        like_list = requests.get(request_url).json()                    #Check the like list of the recent post
        if len(like_list['data']):
            print 'These are the usernames that have liked your recent post:'
            for i in range(len(like_list['data'])):
                    print ('username: %s') %(like_list['data'][i]['username'])
        else:
            print 'User\'s recent post has no likes yet!'
    except KeyError:
            print "Unable to process your request. Please try again!!"



#Function to like a post
def like_a_post(insta_username):
    media_id=get_post_id(insta_username)
    request_url=(BASE_URL+"media/%s/likes") %(media_id)
    payload={"access_token":APP_ACCESS_TOKEN}
    print 'POST request url : %s' % (request_url)
    try:
        post_a_like = requests.post(request_url, payload).json()
        if post_a_like['meta']['code'] == 200:                          #it help to like a post through the user
            print 'Like was successful!'
        else:
            print 'Your like was unsuccessful. Try again!'
    except KeyError:
            print "Unable to process your request. Please try again!!"

#Function to unlike a post
def unlike_a_post(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + "media/%s/likes?access_token=%s") % (media_id,APP_ACCESS_TOKEN)
    print 'DELETE request url: %s'%(request_url)
    unlike_post=requests.delete(request_url).json()
    if unlike_post['meta']['code'] == 200:
        print 'Unlike was successful!'
    else:
        print 'Your Unlike was unsuccessful. Try again!'

#Function to get a comment list on the post
def get_comment_list(insta_username):
    post_id = get_post_id(insta_username)
    if post_id == None:
        print 'User does not exist!'
        exit()
    try:
        request_url = (BASE_URL + 'media/%s/comments?access_token=%s') % (post_id, APP_ACCESS_TOKEN)
        print 'GET request url : %s' % (request_url)
        comment_list=requests.get(request_url).json()
        if len(comment_list['data']):
            print 'These are the usernames that have commented on your recent post:'
            for i in range(len(comment_list['data'])):
                    print ('username: %s') %(comment_list['data'][i]['from']['username'])
                    print ('comment: %s') %(comment_list['data'][i]['text'])
        else:
            print 'User\'s recent post has no comments yet!'
    except KeyError:
            print "Unable to process your request. Please try again!!"


#Function to make a comment on a recet post
def post_a_comment(insta_username):
    media_id = get_post_id(insta_username)
    comment_text = raw_input("Your comment: ")
    try:
        payload = {"access_token": APP_ACCESS_TOKEN, "text" : comment_text}
        request_url = (BASE_URL + 'media/%s/comments') % (media_id)
        print ('POST request url : %s') % (request_url)
        make_comment = requests.post(request_url, payload).json()
        if make_comment['meta']['code'] == 200:
            print "Successfully added a new comment!"
        else:
            print "Unable to add comment. Try again!"
    except :
        print "Unable to process your request. Please try again!!"


#Function to get a recent like by self
def recent_liked():
        request_url=(BASE_URL+'users/self/media/liked?access_token=%s') %(APP_ACCESS_TOKEN)
        print 'GET request url: %s' %(request_url)
        recent_liked_media=requests.get(request_url).json()
        try:
            if recent_liked_media['meta']['code']==200:
                if len(recent_liked_media['data']):
                    image_name = 'recent_liked' + '.jpg'
                    image_url = recent_liked_media['data'][0]['images']['standard_resolution']['url']
                    urllib.urlretrieve(image_url, image_name)
                    print 'Your image has been downloaded!'
                else:
                    print 'Post does not exist!'
            else:print 'Status code other than 200 received!'
        except KeyError:
            print "Unable to process your request. Please try again!!"




#Function to delete a negative comments
def delete_negative_comment(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()
    try:
        if comment_info['meta']['code'] == 200:
            if len(comment_info['data']):
                # Here's a naive implementation of how to delete the negative comments
                for x in range(0, len(comment_info['data'])):
                    comment_id = comment_info['data'][x]['id']                                  #storing comment id
                    comment_text = comment_info['data'][x]['text']
                    blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())                #Textblob() takes comment text
                    if (blob.sentiment.p_neg > blob.sentiment.p_pos):
                        print ('Negative comment : %s') % (comment_text)
                        delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (media_id, comment_id, APP_ACCESS_TOKEN)
                        print 'DELETE request url : %s' % (delete_url)
                        delete_info = requests.delete(delete_url).json()

                        if delete_info['meta']['code'] == 200:
                            print 'Comment successfully deleted!\n'
                        else:
                            print 'Unable to delete comment!'
                    else:
                        print ('Positive comment : %s\n') % (comment_text)
            else:
                print 'There are no existing comments on the post!'
        else:
            print 'Status code other than 200 received!'
    except KeyError:
            print "Unable to process your request. Please try again!!"

def choose_post():
    print "Choose post one of following options:"
    print "a.Choose post with minimum likes"
    print "b.Choose post with maximum likes"
    print "c.Choose post which has text in caption"
    print "d.Choose post of recent images liked ny user"
    choice = raw_input("Enter your choice: ")
    try:
        if choice == 'a':
            user_name = raw_input("Enter username: ")
            user_id = get_user_id(user_name)
            if user_id == None:
                print "Username not valid!"
            else:
                request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
                print 'GET request url : %s' % (request_url)
                user_media = requests.get(request_url).json()
                if user_media['meta']['code'] == 200:
                    if len(user_media['data']):
                        like_count_list = []
                        for i in range(len(user_media['data'])):
                            likes = user_media['data'][i]['likes']['count']
                            like_count_list.append(likes)
                        min_count = min(like_count_list)
                        for i in range(len(user_media['data'])):
                            if user_media['data'][i]['likes']['count'] == min_count:
                                get_id = user_media['data'][i]['id']
                                image_name = get_id + '.jpeg'
                                image_url = user_media['data'][i]['images']['standard_resolution']['url']
                        urllib.urlretrieve(image_url, image_name)
                        print 'Your image has been download!'
        elif choice == 'b':
            user_name = raw_input("Enter username: ")
            user_id = get_user_id(user_name)
            if user_id == None:
                print "Username not valid!"
            else:
                request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
                print 'GET request url : %s' % (request_url)
                user_media = requests.get(request_url).json()

                if user_media['meta']['code'] == 200:
                    if len(user_media['data']):
                        like_count_list = []
                        for i in range(len(user_media['data'])):
                            likes = user_media['data'][i]['likes']['count']
                            like_count_list.append(likes)
                        min_count = max(like_count_list)
                        for i in range(len(user_media['data'])):

                            if user_media['data'][i]['likes']['count'] == min_count:
                                get_id = user_media['data'][i]['id']
                                image_name = get_id + '.jpeg'
                                image_url = user_media['data'][i]['images']['standard_resolution']['url']
                        urllib.urlretrieve(image_url, image_name)
                        print 'Your image has been download!'


        elif choice == 'c':
            user_name = raw_input("Enter username: ")
            user_id = get_user_id(user_name)
            if user_id == None:
                print "Username not valid!"
            else:
                request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
                print 'GET request url : %s' % (request_url)
                user_media = requests.get(request_url).json()

                if user_media['meta']['code'] == 200:
                    if len(user_media['data']):
                        word = raw_input("Enter word you want to search in caption of a post: ")
                        if word.isspace() == True or len(word) == 0:
                            print "Word cannot be empty!"
                        else:
                            count = 0
                            for i in range(len(user_media['data'])):
                                caption = user_media['data'][i]['caption']['text']
                                if word in caption:
                                    print "Post id is: %s" % (user_media['data'][i]['id'])
                                    print "Caption: %s\n" % (caption)
                                    get_id = user_media['data'][i]['id']
                                    image_name = get_id + '.jpg'
                                    image_url = user_media['data'][i]['images']['standard_resolution']['url']
                                    urllib.urlretrieve(image_url, image_name)
                                    print 'Your image has been download!'
                                    count += 1
                            if count == 0:
                                print "Entered word is not in caption!"
                    else:
                        print "This user has no media. Try again!"
                else:
                    print "Status code other than 200 recieved"

        else:
            print "Wrong choice!! Try again."
    except:
       print "Unable to process your request. Please try again!!"



#Function for recent like
def recent_media_liked():
           request_url = (BASE_URL + 'users/self/media/liked?access_token=%s') % (APP_ACCESS_TOKEN)
           print 'GET request url: %s' % (request_url)
           recent_liked_media = requests.get(request_url).json()
           try:
               if recent_liked_media['meta']['code'] == 200:
                   if len(recent_liked_media['data']):
                       image_name = 'recent_liked' + '.jpg'
                       image_url = recent_liked_media['data'][0]['images']['standard_resolution']['url']
                       urllib.urlretrieve(image_url, image_name)
                       print 'Your image has been downloaded!'
                   else:
                       print 'Post does not exist!'
               else:
                   print 'Status code other than 200 received!'
           except KeyError:
               print "Unable to process your request. Please try again!!"


def location_info():
    user_name = raw_input("Enter username: ")
    user_id = get_user_id(user_name)
    if user_id == None:
        print "Username not valid!"
    else:
        request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
        print 'GET request url : %s' % (request_url)
        user_media = requests.get(request_url).json()  # STORES JSON OBJECT RESPONSE IN A VARIABLE

        if user_media['meta']['code'] == 200:  # CHECKS IF RECIEVED META CODE IS 200
            if len(user_media['data']):
                word = raw_input("Enter the location you want to search): ")  # ASKING FOR TEXT USER WANT TO SEARCH FOR IN CAPTION
                if word.isspace() == True or len(word) == 0:
                    print "id cannot be empty!"
                else:
                    for i in range(len(user_media['data'])):
                        location = user_media['data'][i]['location']['id']
                        if word in location:  # GETS THE POST IF WORD IS FOUND IN CAPTION OF POST
                            print "Post id is: %s" % (user_media['data'][i]['id'])
                            print "image: %s\n" % (location)
                            get_id = user_media['data'][i]['id']
                            image_name = get_id + '.jpeg'
                            image_url = user_media['data'][i]['images']['standard_resolution']['url']
                            urllib.urlretrieve(image_url, image_name)
                            print 'Your image has been downloaded!'
            else:
                print "This user has no media. Try again!"
        else:
            print "Status code other than 200 recieved"



#function to ask users user for task they want to perform
def start_bot():
        while True:
            print '\n'
            print 'Hey! Welcome to instaBot!'
            print 'Here are your menu options:'
            print "a.Get your own details\n"
            print "b.Get details of a user by username\n"
            print "c.Get your own recent post\n"
            print "d.Get the recent post of a user by username\n"
            print "e.Get a list of people who have liked the recent post of a user\n"
            print "f.Like the recent post of a user\n"
            print "g.Unlike the recent post of a user\n"
            print "h.Get a list of comments on the recent post of a user\n"
            print "i.Make a comment on the recent post of a user\n"
            print "j.Delete negative comments from the recent post of a user\n"
            print "k.To choose Min and Max likes and choose a caption\n "
            print "l.Exit"
            #Getting menu choice for user
            choice = raw_input("Enter you choice: ")
            if choice == "a":
                self_info()
            elif choice == "b":
                insta_username = raw_input("Enter the username of the user: ")
                get_user_info(insta_username)
            elif choice=="c":
                get_own_post()
            elif choice=="d":
                insta_username = raw_input("Enter the username of the user: ")
                get_user_post(insta_username)
            elif choice=="e":
                insta_username = raw_input("Enter the username of the user: ")
                get_like_list(insta_username)
            elif choice=="f":
                insta_username = raw_input("Enter the username of the user: ")
                like_a_post(insta_username)
            elif choice=="g":
                insta_username = raw_input("Enter the username of the user: ")
                unlike_a_post(insta_username)
            elif choice=="h":
                insta_username = raw_input("Enter the username of the user: ")
                get_comment_list(insta_username)
            elif choice=="i":
                insta_username = raw_input("Enter the username of the user: ")
                post_a_comment(insta_username)
            elif choice=="j":
                insta_username = raw_input("Enter the username of the user: ")
                delete_negative_comment(insta_username)
            elif choice=='k':
                choose_post()
            elif choice=='l':
                recent_media_liked()
            elif choice=='m':
                location_info()
            elif choice=='n':
                exit()
            else:
                print "wrong choice"

start_bot()              #Recall the startbot