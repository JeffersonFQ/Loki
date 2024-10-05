import pyrebase

firebaseConfig = {
    'apiKey': "AIzaSyDjYwLhHAB8ZJSuFw4mmh58RKzp9tx3nVA",
    'authDomain': "loki-95d45.firebaseapp.com",
    'projectId': "loki-95d45",
    'storageBucket': "loki-95d45.appspot.com",
    'databaseURL': "https://loki-95d45-default-rtdb.firebaseio.com/",
    'messagingSenderId': "784689390439",
    'appId': "1:784689390439:web:c41456f433c5f86b9285c2",
    'measurementId': "G-18J63K96HG"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

def initialize_firebase():
    global firebase, auth, db
    firebase = pyrebase.initialize_app(firebaseConfig)
    auth = firebase.auth()
    db = firebase.database()
