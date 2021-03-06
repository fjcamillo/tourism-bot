from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import generic
from django.http import HttpResponse
import requests
from pprint import pprint
import json
import datetime
# from . import replierfunc
# from .persistentmenus import persistentmenu
# from .generictemplates import generate
import mainmenu
import topdestinatons
import ceamore
import princessamore
import galeramore
import elnidomore
import boracaymore
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import numpy as np
import classifier
import storiesme
import bookreceipt
import flight

count_vec = CountVectorizer()
normalized_text = TfidfTransformer()

verify_token = '5244680129'
ngrokurl = 'https://3a5b64d1.ngrok.io'

page_access_token = 'EAAIwxSTcnu0BALz1yGvBSgnwXgwEQuv6IVoHmob6VYHni2EqCYSWYdZA3oM9e64tZBbeC5tn94mdvHZAoJzKhwzN9Thj8d3cYHzkSTgsbijEGhhZAh6msbG5i5y1eKX7xq6I3t0QPf8owXKhdbdJZAjLrhvZCoS7ZCHqBTgthRBlwZDZD'
post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token='+page_access_token

smess = [
"The College of Engineering, formerly known as the College of Engineering and Architecture celebrates its 25th year on the Centenary of PUP. The CEA was acknowledged by many as the University's flagship college. Here are the highlights of the growth of the College from the Faculty of Technology to what and where it is now.",

"PUERTO PRINCESA Paddling through the navigable portion of the 8.2 kilometer Underground River is a journey through time its karstic chambers serve as a natural canvas on which vignettes of the past are geologically preserved.",

"Our mission is to connect tourists and businesses to Boracay Island to share this unique world class fine white sand beach experience to the rest of the world.",

"El Nido is a Philippine municipality on Palawan island. Its known for its whitesand beaches, coral reefs and as the gateway to the Bacuit archipelago, a group of islands with steep karst cliffs.",

"Puerto Galera is a soothing vision of shimmering seas surrounded by lush mountains. It is considered one of the most beautiful and developed beach resort community in the country"

]

class index(generic.View):

    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == verify_token:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error', 'Invalid Token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        pprint("\n=============INITIAL JSON RETURN================")
        pprint(incoming_message)
        pprint("\n=============INITIAL JSON RETURN================")
        if 'entry' in incoming_message:
            for entry in incoming_message['entry']:
                if 'messaging' in entry:
                    for message in entry['messaging']:
                        if 'postback' in message:
                            if message['postback']['payload']=='MAIN_MENU':
                                mainmenu.mainmenu(message['sender']['id'],ngrokurl, page_access_token)
                            elif message['postback']['payload']=="GET_LOCATION":
                                location_button(message['sender']['id'])
                            elif message['postback']['payload'] == "TOP_DESTINATION":
                                topdestinatons.topdestinations(message['sender']['id'], ngrokurl, page_access_token)
                            elif message['postback']['payload'] == "STORIES":
                                storiesme.storiesme(message['sender']['id'], ngrokurl, page_access_token)
                            elif message['postback']['payload'] == "SUBSCRIPTIONS":
                                pass
                            elif message['postback']['payload'] == "ABOUT_US":
                                pass
                            elif message['postback']['payload'] == "SHOW_BEST":
                                topdestinatons.topdestinations(message['sender']['id'], ngrokurl, page_access_token)
                            elif message['postback']['payload'] == "SUBSCRIBE":
                                pass
                            elif message['postback']['payload'] == "SHOW_HEADLINES":
                                storiesme.storiesme(message['sender']['id'], ngrokurl, page_access_token)
                            elif message['postback']['payload'] == "BLOG":
                                storiesme.storiesme(message['sender']['id'], ngrokurl, page_access_token)
                            elif message['postback']['payload'] == "ABOUT_CEA":
                                ceamore.ceamore(message['sender']['id'], ngrokurl, page_access_token)
                                mess = smess[0]
                                post_facebook_messages(message['sender']['id'], mess)
                            elif message['postback']['payload'] == "BOOK_CEA":
                                flight.flight(message['sender']['id'], ngrokurl, page_access_token)
                                bookreceipt.bookreceipt(message['sender']['id'], ngrokurl, page_access_token)
                            elif message['postback']['payload'] == "ABOUT_PRINCESSA":
                                princessamore.princessamore(message['sender']['id'], ngrokurl, page_access_token)
                                mess = smess[1]
                                post_facebook_messages(message['sender']['id'], mess)
                            elif message['postback']['payload'] == "BOOK_PRINCESSA":
                                bookreceipt.bookreceipt(message['sender']['id'], ngrokurl, page_access_token)
                            elif message['postback']['payload'] == "ABOUT_BORACAY":
                                boracaymore.boracaymore(message['sender']['id'], ngrokurl, page_access_token)
                                mess = smess[2]
                                post_facebook_messages(message['sender']['id'], mess)
                            elif message['postback']['payload'] == "BOOK_BORACAY":
                                bookreceipt.bookreceipt(message['sender']['id'], ngrokurl, page_access_token)
                            elif message['postback']['payload'] == "ABOUT_NIDO":
                                elnidomore.elnidomore(message['sender']['id'], ngrokurl, page_access_token)
                                mess = smess[3]
                                post_facebook_messages(message['sender']['id'], mess)
                            elif message['postback']['payload'] == "BOOK_NIDO":
                                bookreceipt.bookreceipt(message['sender']['id'], ngrokurl, page_access_token)
                            elif message['postback']['payload'] == "ABOUT_GALERA":
                                galeramore.galeramore(message['sender']['id'], ngrokurl, page_access_token)
                                mess = smess[4]
                                post_facebook_messages(message['sender']['id'], mess)
                            elif message['postback']['payload'] == "BOOK_GALERA":
                                bookreceipt.bookreceipt(message['sender']['id'], ngrokurl, page_access_token)
                        if 'message' in message:
                            if 'attachments' in message['message']:
                                for attach in message['message']['attachments']:
                                    lat = attach['payload']['coordinates']['lat']
                                    long = attach['payload']['coordinates']['long']
                                    reply = 'lat: {}, long: {}'.format(lat, long)
                                    post_facebook_messages(message['sender']['id'], reply)
                            if 'text' in message['message']:
                                # for tex in m
                                chatbot(message['message']['text'], message['sender']['id'], classifier.getTrainSet(), classifier.getLabels(), False)
                                pass

                        # gen = generate(fbid=message['sender']['id'], page_access_token=page_access_token)
                        # gen.generichorizontaltemplate(gen.fbid, gen.page_access_token)
                        # whitelistdomain(message['sender']['id'], page_access_token)
                        # generichorizontaltemplate(message['sender']['id'], page_access_token)
                        #
                        # firstname = getName(message['sender']['id'], page_access_token)['first_name']

                        # mainmenu = persistentmenu(message['sender']['id'], page_access_token)
                        # mainmenu.persistent_mainmenu(mainmenu.fbid, mainmenu.page_access_token)

                        # send_message = "Hi {}, Thank You, for trying out TaraliBot. I will now echo your message: {}".format(
                        #     firstname, message['message']['text'])
                        # post_facebook_messages(message['sender']['id'], send_message)
                        # location_reply(message['sender']['id'], message)
                # elif ''
        else: pass
        return HttpResponse()

def location_button(fbid):
    """
    :param fbid: Facebook User ID
    :param received_messages: Message Received Sent by Facebook User ID
    :return:
    """
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token='+page_access_token
    response_msg = json.dumps(
        {"recipient": {"id": fbid},
        "message": {
            "text": "Please share the location you want to search:",
            "quick_replies": [
                {
                    "content_type": "location",
                }
                ]
            }
        })

    print('-----')
    print(response_msg)
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)
    pprint(status.json())
    return

def generichorizontaltemplate(fbid, page_access_token):
    pprint('---Starting generichorizontaltemplate----')
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + page_access_token
    # response = {
    #     'recipient': {'id': self.fbid},
    #     'message':{
    #         'attachment':{
    #             'type':'template',
    #             'payload':
    #         }
    #     }
    # }

    response_msg = json.dumps({
            "recipient": {"id": fbid},
            "message":{
                "attachment":{
                  "type":"template",
                  "payload":{
                    "template_type":"generic",
                    "elements":[
                       {
                        "title":"Welcome to Peter\'s Hats",
                        "image_url":ngrokurl+"/media/1.jpg",
                        "subtitle":"We\'ve got the right hat for everyone.",
                        "default_action": {
                          "type": "web_url",
                          "url": ngrokurl,
                          "messenger_extensions": True,
                          "webview_height_ratio": "tall",
                          "fallback_url": ngrokurl
                        },
                        "buttons":[
                          {
                            "type":"web_url",
                            "url":ngrokurl,
                            "title":"View Website"
                          },{
                            "type":"postback",
                            "title":"Start Chatting",
                            "payload":"DEVELOPER_DEFINED_PAYLOAD"
                          },

                        ]
                      },
                        {
                            "title": "Welcome to Peter\'s Hats",
                            "image_url": ngrokurl + "/media/1.jpg",
                            "subtitle": "We\'ve got the right hat for everyone.",
                            "default_action": {
                                "type": "web_url",
                                "url": ngrokurl,
                                "messenger_extensions": True,
                                "webview_height_ratio": "tall",
                                "fallback_url": ngrokurl
                            },
                            "buttons": [
                                {
                                    "type": "web_url",
                                    "url": ngrokurl,
                                    "title": "View Website"
                                }, {
                                    "type": "postback",
                                    "title": "Start Chatting",
                                    "payload": "DEVELOPER_DEFINED_PAYLOAD"
                                },

                            ]
                        },
                        {
                            "title": "Welcome to Peter\'s Hats",
                            "image_url": ngrokurl + "/media/1.jpg",
                            "subtitle": "We\'ve got the right hat for everyone.",
                            "default_action": {
                                "type": "web_url",
                                "url": ngrokurl,
                                "messenger_extensions": True,
                                "webview_height_ratio": "tall",
                                "fallback_url": ngrokurl
                            },
                            "buttons": [
                                {
                                    "type": "web_url",
                                    "url": ngrokurl,
                                    "title": "View Website"
                                }, {
                                    "type": "postback",
                                    "title": "Start Chatting",
                                    "payload": "DEVELOPER_DEFINED_PAYLOAD"
                                },

                            ]
                        }
                    ]
                  }
                }
              }
            })
    pprint(response_msg)
    status = requests.post(post_message_url, headers={"Content-Type" : "application/json"}, data = response_msg)
    pprint(status.json())
    return


def getName(fbid, page_access_token):
    """
    Sample Get API Access
    https://graph.facebook.com/v2.6/<USER_ID>?fields=first_name,last_name,profile_pic,locale,timezone,gender&access_token=PAGE_ACCESS_TOKEN
    :param fbid:
    :param page_access_token:
    :return:
    """
    post_message_url = 'https://graph.facebook.com/v2.6/'+fbid+'?fields=first_name,last_name&access_token='+page_access_token
    status = requests.get(post_message_url)
    pprint(status.json())
    return status.json()

def post_facebook_messages(fbid, received_messages):
    """
    :param fbid: Facebook User ID
    :param received_messages: Message Received Sent by Facebook User ID
    :return:
    """
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token='+page_access_token

    response_msg = json.dumps(
        {"recipient":
             {"id": fbid},
         "message":
             {"text": received_messages}
         })

    print('-----')
    print(response_msg)
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)
    pprint(status.json())
    return

def receive_postback(fbid):
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token='+page_access_token
    return

def location_reply(fbid, received_messages):
    """
    :param fbid: Facebook User ID
    :param received_messages: Message Received Sent by Facebook User ID
    :return:
    """
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token='+page_access_token
    latitude = []
    longitude = []
    msg = received_messages['message']
    for attach in msg['attachments']:
        latitude.append(attach['payload']['coordinates']['lat'])
        longitude.append(attach['payload']['coordinates']['long'])

    response_msg = json.dumps(
        {'recipient':
             {'id':fbid},
         'message':
             {'text':
                  "Coordinates: "+str(latitude[0])+","+str(longitude[0])}})

    status = requests.post(post_message_url, headers={"Content-Type": "application/json"}, data=response_msg)
    pprint(status.json())
    return

def chatbot(predict_message, sender_id, training_Set, labels, verbose):
    if verbose==True:
        print("\n----Entered Chatbot-----\n")

    #Created a model to fit the training_set
    trained = count_vec.fit_transform(training_Set)

    #Normalizing the trained model
    normal = normalized_text.fit_transform(trained)

    #Created a Random Forest Classifer and fitted the normal and labels dataset
    clf = RandomForestClassifier().fit(normal, labels)
    docs_new = [predict_message]
    X_new_counts = count_vec.transform(docs_new)
    X_new_tfidf = normalized_text.transform(X_new_counts)
    x = clf.predict(X_new_tfidf)
    post_facebook_messages(sender_id,str(x[0]))
    return