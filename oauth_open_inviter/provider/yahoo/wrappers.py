import urllib


class YahooFeed(object):
    def __init__(self, feed, converter, entries_key=''):
        self.feed = feed
        self.converter = converter
        self.entries_key = entries_key

    @property
    def entries(self):
        if self.feed:
            return [self.converter(entry) for entry in self.feed.get(self.entries_key, [])]
        return []

    @property
    def next_link(self):
        uri = self.feed['base_url']
        start = self.feed.get('start', 0)
        total = self.feed.get('total', 0)
        count = self.feed.get('count', 50)
        if self.feed.get(self.entries_key) and start + 1 < total:
            params = urllib.urlencode({'format': self.feed.get('format', 'json'), 'start': start + count,
                                       'count': count})
            return '%s?%s' % (uri, params)

    @property
    def prev_link(self):
        uri = self.feed['base_url']
        start = self.feed.get('start')
        count = self.feed.get('count', 50)
        if start and start > 0:
            start = start - count
            params = urllib.urlencode({'format': self.feed.get('format', 'json'), 'start': start, 'count': count})
            return '%s?%s' % (uri, params)


class YahooContact(object):
    def __init__(self, entry):
        self.entry = entry
        self.fields = {}
        for field in self.entry.get('fields'):
            self.fields[field.get('type')] = field.get('value')

    @property
    def id(self):
        return self.entry['id']

    @property
    def updated(self):
        return self.entry['updated']

    @property
    def created(self):
        return self.entry['created']

    @property
    def first_name(self):
        name = self.fields.get('name', {})
        name = '%s %s' % (name.get('givenName', ''), name.get('middleName', ''))
        return name.strip()

    @property
    def last_name(self):
        return self.fields.get('familyName', '')

    @property
    def name(self):
        name = '%s %s' % (self.first_name, self.last_name)
        return name.strip()

    @property
    def emails(self):
        return [email for email in [self.fields.get('email', '').strip()] if email]

    @property
    def nickname(self):
        return self.fields.get('nickname')
