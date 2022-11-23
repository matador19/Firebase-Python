from flask import Flask
from flask import request
from flask import jsonify
import json
import requests
import os
import numpy as np
from keras.models import load_model
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Fetch the service account key JSON file contents
cred = credentials.Certificate('secret key.json')
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://blooddonationapp-ba6fb-default-rtdb.firebaseio.com/"
})
app = Flask(__name__)
model = load_model('model.h5')


@app.route('/run', methods=['GET', 'POST'])
def root():
    ref = db.reference('/risk')
    #users = ref.order_by_key().get()
    personone=ref.child("3").get() #change the value here
   
    inputs_test=[]
    for key in personone:
        if personone[key]== 'yes':
            personone[key]=1
        else:
            personone[key]=0
        inputs_test.append(personone[key])
        # print(personone[key])
    prediction=np.around(model.predict(np.reshape(inputs_test,(1,8)))).astype(np.int64)
    text_prediction=""
    if prediction[0][0]==1 and  prediction[0][1]==0 and  prediction[0][2]==0:
        text_prediction="high"
    if prediction[0][0]==0 and  prediction[0][1]==1 and  prediction[0][2]==0:
        text_prediction="low"
    if prediction[0][0]==0 and  prediction[0][1]==0 and  prediction[0][2]==1:
        text_prediction="medium"
    ref.child("3").update({'prediction':text_prediction}) #change the value here
    print(text_prediction)
    return jsonify({"method":"GET","pred":"predicted"})
