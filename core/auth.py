
import requests
from django.http import JsonResponse, HttpResponseRedirect

# Replace with your actual credentials from Google Cloud Console
GOOGLE_CLIENT_ID = "808778216240-j1g5tes4ooj768v2o51lo7vl293398o3.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "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"
REDIRECT_URI = "http://localhost:8000/api/auth/callback/"

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"


def start_google_auth(request):
    auth_url = (
        f"{GOOGLE_AUTH_URL}?response_type=code"
        f"&client_id={GOOGLE_CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope=email%20profile"
    )
    return HttpResponseRedirect(auth_url)


def google_auth_callback(request):
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

    access_token = token_info.get('access_token')
    headers = {'Authorization': f'Bearer {access_token}'}
    user_info_response = requests.get(GOOGLE_USERINFO_URL, headers=headers)
    user_info = user_info_response.json()

    return JsonResponse(user_info)
