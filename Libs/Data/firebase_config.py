import pyrebase

firebaseConfig = {
    'apiKey': "AIzaSyCLTao0HZg76fADjCsxYNRGK3EnyLWoPlU",
    'authDomain': "loki-78600.firebaseapp.com",
    'projectId': "loki-78600",
    'storageBucket': "loki-78600.appspot.com",
    'databaseURL': "https://loki-78600-default-rtdb.firebaseio.com/",
    'messagingSenderId': "231998097698",
    'appId': "1:231998097698:web:56d086015e63dc0b3f7d7b",
    'measurementId': "G-NNDKMJ0FN4"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

def initialize_firebase():
    global firebase, auth, db
    firebase = pyrebase.initialize_app(firebaseConfig)
    auth = firebase.auth()
    db = firebase.database()
