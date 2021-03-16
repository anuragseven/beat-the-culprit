import requests
import json


def send_text_to_authority(name):
    myobj = {
        'Body': "CRIMINAL DETECTED : {} ".format(name),
        'From': '+18155818608',
        'To': '+91 9340000871',

    }
    requests.post('https://api.twilio.com/2010-04-01/Accounts/AC7d1485213feabb7e5aeba64a5ae15ac6/Messages'
                  '.json',
                  auth=('AC7d1485213feabb7e5aeba64a5ae15ac6', 'b94fa2c63bb040b75f1c42b3a8bc2709'),
                  data=myobj)


def azure_detect(image):
    url = 'https://westus.api.cognitive.microsoft.com/face/v1.0/detect?returnFaceId=true'
    headers = {"Content-Type": "application/octet-stream",
               "Ocp-Apim-Subscription-Key": '8e7f8b81cb1c44fdba666fae65525a46'}

    response = requests.post(url=url, headers=headers, data=image)
    dict_obj = json.loads(response.text)
    detected_face_id = dict_obj[0]['faceId']
    print('azure detected a face , temproary id provided to it :' + detected_face_id)
    return dict_obj[0]['faceId']


def azure_identify(detected_face_id):
    url = 'https://westus.api.cognitive.microsoft.com/face/v1.0/identify'
    headers = {'Content-Type': 'application/json', 'Ocp-Apim-Subscription-Key': '8e7f8b81cb1c44fdba666fae65525a46'}
    request_body = {"faceIds": [
        detected_face_id
    ],
        "personGroupId": "criminal_group",

        "maxNumOfCandidatesReturned": 1,
        "confidenceThreshold": 0.45}

    response = requests.post(url=url, headers=headers, data=json.dumps(request_body))
    dict_obj = json.loads(response.text)
    azure_face_id = dict_obj[0]['candidates'][0]['personId']
    confidence = dict_obj[0]['candidates'][0]['confidence']
    print("criminal has been identified  with face id: " + azure_face_id)
    print("and confidence : " + str(confidence))
    return azure_face_id


def firebase_user_sign_in():
    url = 'https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=AIzaSyCe' \
          '-vZ2pPxg5h4y1LUTD76Wi9ZGktAoAF8'

    data = {'email': 'facerecognitionproject1@gmail.com', 'password': 'BeatTheCulprits', 'returnSecureToken': 'true'}
    response = requests.post(url=url, data=data)
    dict_obj = json.loads(response.text)
    id_token = dict_obj['idToken']
    return id_token


def get_name_from_id(azure_face_id, id_token):
    url = 'https://firestore.googleapis.com/v1/projects/beattheculprit/databases/(default)/documents/criminals/' + \
          azure_face_id
    headers = {'Authorization': 'Bearer ' + id_token}
    response = requests.get(url=url, headers=headers)
    dict_obj = json.loads(response.text)
    name = dict_obj['fields']['name']['stringValue']
    return name
