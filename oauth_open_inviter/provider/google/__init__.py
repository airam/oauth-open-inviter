from oauth_open_inviter.oauth_access.access import OAuth2Access
from oauth_open_inviter.provider.base import BaseProvider
from oauth_open_inviter.provider.google.wrappers import GmailFeed, GmailContact

MAX_LIMIT = 25
START_INDEX = 1
MAX_RESULTS = 50

class GmailProvider(OAuth2Access, BaseProvider):
    """
    Class for getting contacts from gmail account
    (using OAuth2)
    """

    access_token_url = 'https://accounts.google.com/o/oauth2/token'
    authorize_url = 'https://accounts.google.com/o/oauth2/auth'

    scope_urls = ['https://www.google.com/m8/feeds/']

    def search(self, base_url, extra_params=None,
               url=None, start_index=START_INDEX, max_results=MAX_RESULTS, **kwargs):
        feed_url = url or base_url
        url_params = {'start-index': start_index,'max-results': max_results}
        if url:
            url_params = None
        else:
            if extra_params:
                url_params.update(extra_params)
        return self.make_api_call(url=feed_url, method="GET", params=url_params, **kwargs)

    def get_contacts(self, username='default', url=None, start_index=START_INDEX, max_results=MAX_RESULTS):
        base_url = 'https://www.google.com/m8/feeds/contacts/%s/full' % username
        extra_params = {'alt': 'json'}
        feed = self.search(base_url, url=url, extra_params=extra_params,
            start_index=start_index, max_results=max_results, kind='json')
        return GmailFeed(feed, GmailContact)

    def get_all_contacts(self, username='default'):
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

