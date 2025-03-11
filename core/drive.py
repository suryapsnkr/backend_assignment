
import json
import requests
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect

# Replace with your actual credentials from Google Cloud Console
GOOGLE_CLIENT_ID = "808778216240-j1g5tes4ooj768v2o51lo7vl293398o3.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "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"
REDIRECT_URI = "http://localhost:8000/api/drive/callback/"

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
DRIVE_FILES_URL = "https://www.googleapis.com/drive/v3/files"
DRIVE_UPLOAD_URL = "https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart"


def connect_google_drive(request):
    auth_url = (
        f"{GOOGLE_AUTH_URL}?response_type=code"
        f"&client_id={GOOGLE_CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope=https://www.googleapis.com/auth/drive.file"
    )
    return HttpResponseRedirect(auth_url)


def drive_callback(request):
    code = request.GET.get('code')
    data = {
        'code': code,
        'client_id': GOOGLE_CLIENT_ID,
        'client_secret': GOOGLE_CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
        'grant_type': 'authorization_code',
    }
    response = requests.post(GOOGLE_TOKEN_URL, data=data)
    token_info = response.json()

    request.session['drive_access_token'] = token_info.get('access_token')
    return JsonResponse({"message": "Drive connected!", "token_info": token_info})


def list_drive_files(request):
    access_token = request.session.get('drive_access_token')
    if not access_token:
        return JsonResponse({"error": "No Drive connection found!"}, status=401)

    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(DRIVE_FILES_URL, headers=headers)
    return JsonResponse(response.json())


def upload_file_to_drive(request):
    access_token = request.session.get('drive_access_token')
    if not access_token:
        return JsonResponse({"error": "No Drive connection found!"}, status=401)

    file = request.FILES.get('file')
    if not file:
        return JsonResponse({"error": "No file provided!"}, status=400)

    headers = {'Authorization': f'Bearer {access_token}'}
    metadata = {
        "name": file.name
    }
    files = {
        'data': ('metadata', json.dumps(metadata), 'application/json'),
        'file': file
    }
    response = requests.post(DRIVE_UPLOAD_URL, headers=headers, files=files)
    return JsonResponse(response.json())


def download_file_from_drive(request, file_id):
    access_token = request.session.get('drive_access_token')
    if not access_token:
        return JsonResponse({"error": "No Drive connection found!"}, status=401)

    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(f"{DRIVE_FILES_URL}/{file_id}?alt=media", headers=headers)

    content_type = response.headers.get('Content-Type', 'application/octet-stream')
    response = HttpResponse(response.content, content_type=content_type)
    response['Content-Disposition'] = f'attachment; filename="{file_id}"'
    return response
