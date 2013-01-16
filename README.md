OAuth Open Inviter
------------------
Allows to export user contacts from Google, Yahoo! and Hotmail using oauth(2).
Based in django-oauth-access(https://github.com/eldarion/django-oauth-access/)
and Python-contact-importer(https://github.com/millioner/Python-contact-importer)

SETTINGS
--------
The basic configuration is in https://github.com/mpcabd/Python-contact-importer#readme, however we use the google oauth2
api and you need the consumer token and consumer token secret generated when you registre your application in
https://code.google.com/apis/console/#access (don't forget to put you absolute authorized redirect uris); we also
changed the setting variable CONTACT_IMPORT_SETTINGS name to with OAUTH_OPEN_INVITER_SETTINGS.

USAGE
-----
Also with changed little things in the usage. Every Provider has tree basic methods:
-receive_access_tokens: It exchange the oauth token(oauth) or code(oauth2) with the access token.
-get_contacts: Return the paginate list of contacts of the user specified by username. A class with entries, next_link
               and prev_link properties. Entries return a list of Contacts(Yahoo Contact, Hotmail Contact,
               Gmail Contact) that correspond to the current page, next_link return a url to the next page, and
               prev_link return a url to the previous page.
-get_all_contacts: Return all contacts of the user specified by username. A list of Contacts(YahooContact,
                HotmailContact, GmailContact)

With that changed a example of view usage:

views.py

from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from oauth_open_inviter.decorators import get_contacts

@csrf_exempt # Windows Live returns POST request
@login_required
@get_contacts
def import_contacts(request, contact_provider):
    access_token = contact_provider.receive_access_tokens() #you have to get the access token to do a api call.
    contacts = []
    for contact in contact_provider.get_all_contacts():
        contacts.append({'name': contact.name, 'emails': contact.emails})
    return render_to_response('contact_list.html', {
        'contacts': contacts,
        }, context_instance=RequestContext(request))

PROVIDER
--------
We provide the next Contacts Provider that get_contacts decorator used:

providers = {
    'google': GmailProvider, #using oauth v2 api
    'hotmail': HotmailProvider, #using WindowsLiveLogin api
    'hotmail2': HotmailOauthProvider, #using oauth v2 api, but for now the api don't provider email, only emails_hashes
    'yahoo': YahooProvider #using oauth v1
}

You can added(or modify) providers to this dictionary using the setting variable OAUTH_OPEN_INVITER_PROVIDER, given a
dictionary when each key is a service name and each value is a BaseProvider and BasicAccess, OAuthAccess or
OAuth2Access child class.
