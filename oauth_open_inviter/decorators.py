###-*- coding: utf-8 -*-#################################
"""
Django integration module
"""
import json

from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponseBadRequest

from oauth_open_inviter.provider.google import GmailProvider
from oauth_open_inviter.provider.hotmail import HotmailProvider, HotmailOauthProvider
from oauth_open_inviter.provider.yahoo import YahooProvider


providers = {
    'google': GmailProvider,
    'hotmail': HotmailProvider,
    'hotmail2': HotmailOauthProvider,
    'yahoo': YahooProvider
}

providers.update(getattr(settings, 'OAUTH_OPEN_INVITER_PROVIDER', {}))

PROVIDER_CREDENTIALS = settings.OAUTH_OPEN_INVITER_SETTINGS

if type(PROVIDER_CREDENTIALS) != dict:
    raise AttributeError('OAUTH_OPEN_INVITER_SETTINGS is not dictionary')


def get_contacts(view):

    def wrapped_func(request, **kwargs):
        service_name = request.GET.get('service') or request.session.get('open_inviter_service')
        if not service_name:
            raise AttributeError('Service name is not defined')

        if service_name not in providers:
            raise AttributeError('Unknown service name: %s' % service_name)

        if type(PROVIDER_CREDENTIALS.get(service_name)) != dict:
            raise AttributeError('Settings for "%s" provider is not defined' % service_name)

        provider_class = providers.get(service_name)

        if request.GET.get('service'):
            data = PROVIDER_CREDENTIALS.get(service_name)
            data['callback_url'] = request.build_absolute_uri(request.path)
            provider = provider_class(**data)
            request.session['open_inviter_service'] = service_name
            token = provider.get_tokens()
            if token:
                request.session['open_inviter_data'] = json.dumps(token)
            return redirect(provider.get_auth_url())
        elif 'open_inviter_service' in request.session:
            params = dict(PROVIDER_CREDENTIALS.get(service_name))
            params['callback_url'] = request.build_absolute_uri(request.path)
            params.update(json.loads(request.session.get('open_inviter_data', '[]')))
            params.update(dict([(k, v) for k, v in request.GET.items()]))
            if request.method == 'POST':
                params['post_params'] = request.POST
            provider = provider_class(**params)
            del request.session['open_inviter_service']
            if 'open_inviter_data' in request.session:
                del request.session['open_inviter_data']
            return view(request, contact_provider=provider, **kwargs)
        else:
            return HttpResponseBadRequest('')

    return wrapped_func
