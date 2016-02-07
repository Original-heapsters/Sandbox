import os
import facebook
import urllib
import warnings
import webbrowser
#import dbmanager
import urlparse
#import settings



class FBOAuth(object):
    """
    Handles the OAuth phases of Facebook and returns an authenticated GrapApi object, to be used for
    using the Facebook API.
    """
    # the following values are taken from settings.py file but could be hardcoded here
    FACEBOOK_GRAPH_URL = 'http://localhost:8080/'
    CLIENT_ID     = '1689342161283671'
    CLIENT_SECRET = 'a57e46dd1a8e50677a036d0fc77e549b'
    REDIRECT_URI = 'http://localhost:8080/'

    SECRET_CODE = None
    ACCESS_TOKEN = None

    def __init__(self):
        #self.database = dbmanager.DBManager()
        FBOAuth.SECRET_CODE = self.get_secret_code()
        FBOAuth.ACCESS_TOKEN = self.get_access_token()

    def authorize(self):
        
        warnings.filterwarnings('ignore', category=DeprecationWarning)
        savout = os.dup(1)
        os.close(1)
        os.open(os.devnull, os.O_RDWR)
        try:
            webbrowser.open(FBOAuth.FACEBOOK_GRAPH_URL+'/oauth/authorize?'+urllib.urlencode(
                                {'client_id':FBOAuth.CLIENT_ID,
                                 'redirect_uri':FBOAuth.REDIRECT_URI,
                                 'scope':'read_stream'}))
        finally:
            os.dup2(savout, 1)

        FBOAuth.SECRET_CODE = raw_input("Secret Code: ")
        self.save_secret_code(FBOAuth.SECRET_CODE)

        return FBOAuth.SECRET_CODE

    def access_token(self):

        if not FBOAuth.SECRET_CODE:
            FBOAuth.SECRET_CODE = self.authorize()

        args = {'redirect_uri': FBOAuth.REDIRECT_URI,
                'client_id' : FBOAuth.CLIENT_ID,
                'client_secret':FBOAuth.CLIENT_SECRET,
                'code':FBOAuth.SECRET_CODE,}
        
        access_token = urllib.urlopen(FBOAuth.FACEBOOK_GRAPH_URL + "/oauth/access_token?" + urllib.urlencode(args)).read()
        access_token = urlparse.parse_qs(access_token)
        FBOAuth.ACCESS_TOKEN = access_token['access_token'][0]
        self.save_access_token(FBOAuth.ACCESS_TOKEN)
        return FBOAuth.ACCESS_TOKEN

    def get_graph_api(self):

        if not FBOAuth.ACCESS_TOKEN:
            self.access_token()

        return facebook.GraphAPI(FBOAuth.ACCESS_TOKEN)

    def invalidate_login(self):
        self.save_access_token(None)
        self.save_secret_code(None)
        exit(0)
    
    # The following four methods are using database.py for making SECRET_CODE and ACCESS_TOKEN persistent
    #----------------------------------------------------------------------------------------------------
    def get_secret_code(self):
        return None#self.database.get('SECRET_CODE') or None

    def save_secret_code(self, secret_code):
        self.database.save('SECRET_CODE', secret_code)

    def get_access_token(self):
        return None#self.database.get('ACCESS_TOKEN') or None

    def save_access_token(self, access_token):
        self.database.save('ACCESS_TOKEN', access_token)
    #-----------------------------------------------------------------------------------------------------
    
auth = FBOAuth()
auth.authorize()