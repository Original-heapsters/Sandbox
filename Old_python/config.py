# config.py

from authomatic.providers import oauth2

CONFIG = {
    
    'fb': {
           
        'class_': oauth2.Facebook,
        
        # Facebook is an AuthorizationProvider too.
        'consumer_key': '1689342161283671',
        'consumer_secret': 'a57e46dd1a8e50677a036d0fc77e549b',
        
        # But it is also an OAuth 2.0 provider and it needs scope.
        'scope': ['user_about_me', 'email', 'user_actions.music','user_events','user_likes','user_photos','user_tagged_places','user_hometown','user_location','user_posts'],
    }
}