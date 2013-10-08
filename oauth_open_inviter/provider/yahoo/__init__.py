from oauth_open_inviter.oauth_access.access import OAuthAccess
from oauth_open_inviter.provider.base import BaseProvider
from oauth_open_inviter.provider.yahoo.wrappers import YahooFeed, YahooContact

MAX_LIMIT = 25
START_INDEX = 0
MAX_RESULTS = 50

SOCIAL_API_URL = 'http://social.yahooapis.com/v1'


class YahooProvider(OAuthAccess, BaseProvider):
    """
    Class for getting contacts from yahoo account
    (using OAuth)
    """

    request_token_url = 'https://api.login.yahoo.com/oauth/v2/get_request_token'
    access_token_url = 'https://api.login.yahoo.com/oauth/v2/get_token'
    authorize_url = 'https://api.login.yahoo.com/oauth/v2/request_auth'

    def search(self, base_url, extra_params=None,
               url=None, start_index=START_INDEX, max_results=MAX_RESULTS, **kwargs):
        feed_url = url or base_url
        url_params = {'start': start_index, 'count': max_results}
        if url:
            url_params = None
        else:
            if extra_params:
                url_params.update(extra_params)
        return self.make_api_call(url=feed_url, method="GET", params=url_params, **kwargs)

    def get_contacts(self, username='me', url=None, start_index=START_INDEX, max_results=MAX_RESULTS):
        base_url = '%s/user/%s/contacts' % (SOCIAL_API_URL, username)
        extra_params = {'format': 'json'}
        feed = self.search(base_url, url=url, extra_params=extra_params, start_index=start_index,
                           max_results=max_results, kind='json')
        contacts = feed.get('contacts', {})
        contacts.update(extra_params)
        contacts.update({'base_url': base_url})
        return YahooFeed(contacts, YahooContact, entries_key='contact')

    def get_all_contacts(self, username='me'):
        next_link = None
        try:
            while True:
                feed = self.get_contacts(username=username, url=next_link)
                if feed:
                    accounts = feed.entries
                    next_link = feed.next_link
                    for accounts in accounts:
                        yield accounts
                if not next_link:
                    break
        except Exception, ex:
            pass
