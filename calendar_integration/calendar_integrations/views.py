from django.shortcuts import redirect
from django.views import View
from google.oauth2 import credentials
from google_auth_oauthlib.flow import Flow

# Set up the Google API credentials
CLIENT_SECRETS_FILE = 'client_secret.json'  # Replace with your own client secrets file

class GoogleCalendarInitView(View):
    def get(self, request):
        flow = Flow.from_client_secrets_file(
            CLIENT_SECRETS_FILE,
            scopes=['https://www.googleapis.com/auth/calendar'],
            redirect_uri=request.build_absolute_uri('/calendar/redirect/')
        )
        authorization_url, state = flow.authorization_url(access_type='offline', prompt='consent')
        request.session['oauth2_state'] = state
        return redirect(authorization_url)


class GoogleCalendarRedirectView(View):
    def get(self, request):
        state = request.session['oauth2_state']
        flow = Flow.from_client_secrets_file(
            CLIENT_SECRETS_FILE,
            scopes=['https://www.googleapis.com/auth/calendar'],
            redirect_uri=request.build_absolute_uri('/calendar/redirect/')
        )
        flow.fetch_token(authorization_response=request.build_absolute_uri(), state=state)
        credentials = flow.credentials
        # Store the credentials in your database or use them to interact with the Google Calendar API
        return redirect('/')  # Redirect to a success page
