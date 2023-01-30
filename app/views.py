import os

from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response

import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery



os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
REDIRECT_URL = f"http://{os.getenv('HOST')}:{os.getenv('PORT')}/rest/v1/calendar/redirect/"
CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = [
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile',
    'openid'
    ]
def credentials_to_dict(credentials):
    credentials_dict = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
    return credentials_dict


class GoogleCalendarInitView(APIView):
    permission_classes = (AllowAny,)
    queryset = None

    def get(self, request):

        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES)
        flow.redirect_uri = REDIRECT_URL
        authorization_url, state = flow.authorization_url(access_type='offline',include_granted_scopes='true')
        request.session['state'] = state
        return redirect(authorization_url)


class GoogleCalendarRedirectView(APIView):
    permission_classes = (AllowAny,)
    queryset = None

    def get(self, request):

        state = request.session['state']
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
        flow.redirect_uri = REDIRECT_URL
        authorization_response = request.get_full_path()
        flow.fetch_token(authorization_response=authorization_response)
        credentials = flow.credentials
        request.session['credentials'] = credentials_to_dict(credentials)
        if 'credentials' not in request.session:
            return redirect('v1/calendar/init')
        credentials = google.oauth2.credentials.Credentials(**request.session['credentials'])
        service = googleapiclient.discovery.build('calendar', 'v3', credentials=credentials)
        calendar_list = service.calendarList().list().execute()
        calendar_id = calendar_list['items'][0]['id']
        events  = service.events().list(calendarId=calendar_id).execute()
        events_lists = []
        data = {}
        if not events['items']:
            print('No data found.')
            data["message"] = "No data found or user credentials invalid."
        else:
            for events_list in events['items']:
                events_lists.append(events_list)
            data["events"] = events_lists
        return Response(data, status=status.HTTP_200_OK)
