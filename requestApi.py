import os, requests
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials


headers = {
    'Ocp-Apim-Subscription-Key': '16287767a9cc49e2a3367b0225e2d2bd',
}

KEY = '16287767a9cc49e2a3367b0225e2d2bd'

ENDPOINT = 'https://testproj.cognitiveservices.azure.com/'


def detectedFace(image):
    face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))

    faces_on_image = []

    single_face_image_url = image
    single_image_name = os.path.basename(single_face_image_url)
    detected_faces = face_client.face.detect_with_url(url=single_face_image_url)
    if not detected_faces:
        raise Exception('No face detected from image {}'.format(single_image_name))
    
    for face in detected_faces:
        faces_on_image.append(face.face_id)

    return faces_on_image


def createPersonGroup(name, userData, personGroupId):
    body = dict()
    body["name"] = name
    body["userData"] = userData
    body = str(body)
    print(body)
    #Request URL 

    FaceApiCreateLargePersonGroup = 'https://testproj.cognitiveservices.azure.com/face/v1.0/persongroups/'+personGroupId 
    try:
        response = requests.put(FaceApiCreateLargePersonGroup, data=body, headers=headers) 
        return response.status_code


    except Exception as e:
        return e


def createPerson(name, userData, personGroupId):
    body = dict()
    body["name"] = name
    body["userData"] = userData
    body = str(body)

    #Request URL 
    FaceApiCreatePerson = ENDPOINT+'face/v1.0/persongroups/'+personGroupId+'/persons'

    try:
        # REST Call 
        response = requests.post(FaceApiCreatePerson, data=body, headers=headers) 
        responseJson = response.json()
        personId = responseJson
        return personId
        
    except Exception as e:
        return e


def addImageForPerson(personId, personGroupId, imgURL):
    FaceApiAddFace = ENDPOINT+'face/v1.0/persongroups/'+personGroupId+'/persons/'+personId+'/persistedFaces'

    body = dict()
    body["url"] = imgURL
    body = str(body)

    try:
        # REST Call 
        response = requests.post(FaceApiAddFace, data=body, headers=headers) 
        responseJson = response.json()
        persistedFaceId = responseJson["persistedFaceId"]
        print("PERSISTED FACE ID: "+str(persistedFaceId))
        return persistedFaceId
    
    except Exception as e:
        return e


def identifyPerson(image, groupId):
    faceIdsList = detectedFace(image)
    FaceApiIdentify = ENDPOINT+'face/v1.0/identify'

    body = dict()
    body["personGroupId"] = groupId
    body["faceIds"] = faceIdsList
    body = str(body)

    try:
        # REST Call
        response = requests.post(FaceApiIdentify, data=body, headers=headers) 
        responseJson = response.json()
        print(responseJson)
        personId = responseJson[0]["candidates"][0]["personId"]
        confidence = responseJson[0]["candidates"][0]["confidence"]
        
        person = getPerson(personId, groupId)
        return person

    except Exception:
        return 'Could not detect'


def trainPersonGroup(groupId):
    body = dict()

    #Request URL 
    FaceApiTrain = ENDPOINT+'face/v1.0/persongroups/'+groupId+'/train'

    try:
        # REST Call 
        response = requests.post(FaceApiTrain, data=body, headers=headers) 
        return response.status_code

    except Exception as e:
        return e


def getPerson(personId, personGroupId):
    getPersonApi = 'https://testproj.cognitiveservices.azure.com/face/v1.0/persongroups/'+personGroupId+'/persons/'+personId

    try:
        response = requests.get(getPersonApi, headers=headers)
        responseJson = response.json()
        print(responseJson)
        return responseJson
    except Exception as e:
        return e


def getGroups():
    getGroupsApi = ENDPOINT+'face/v1.0/persongroups/'

    try:
        response = requests.get(getGroupsApi, headers=headers)
        return response.json()

    except Exception as e:
        return e