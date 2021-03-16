from configure_clients import azure_detect
from configure_clients import azure_identify


def azure_recognisation(image):
    face_recognition_successful = False
    azure_face_id = ""
    try:
        detected_id = azure_detect(image)
        azure_face_id = azure_identify(detected_id)
        face_recognition_successful = True
    except Exception as e:
        print("error in face recognition "+str(e))

    finally:
        if face_recognition_successful:
            return azure_face_id
        else:
            return "-1"
