import json
import urllib

from django.http import JsonResponse

import face_recognition
import urllib.request
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def home(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        if data['linkFile1'] is not None or data['linkFile2'] is not None:
            first_image_url = data['linkFile1']
            second_image_url = data['linkFile2']
            try:
                first_image = urllib.request.urlopen(first_image_url)
                second_image = urllib.request.urlopen(second_image_url)

                result = compare_faces(first_image, second_image)

                if result[0] < 0.6:
                    message = "The two faces belong to the same person. "
                else:
                    message = "The two faces don't belong to the same person. "

                response_data = {
                    "statusCode": 200,
                    "statusMessage": "OK",
                    "hasError": False,
                    "data": {
                        "resultIndex": 0,
                        "resultMessage": message,
                        "similarPercent": 1 - result[0]
                    }
                }
            except:
                response_data = {
                    "statusCode": 500,
                    "statusMessage": "Oops! Something went wrong, please, try again!",
                    "hasError": True,
                    "data": {}
                }
        else:
            response_data = {
                "statusCode": 422,
                "statusMessage": "Validation error",
                "hasError": True
            }

    else:
        response_data = {
            "statusCode": 403,
            "statusMessage": "This url is supported only POST requests",
            "hasError": True
        }

    return JsonResponse(response_data)


def compare_faces(first_face, second_face):
    first_image = face_recognition.load_image_file(first_face)
    second_image = face_recognition.load_image_file(second_face)

    first_encoding = face_recognition.face_encodings(first_image)[0]
    second_encoding = face_recognition.face_encodings(second_image)[0]

    return face_recognition.face_distance([first_encoding], second_encoding)
