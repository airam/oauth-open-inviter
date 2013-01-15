class GmailFeed(object):

    def __init__(self, feed, converter):
        self.feed = feed
        if self.feed and self.feed.has_key('feed'):
            self.feed = self.feed['feed']
        self.converter = converter
        self.load_link()

    def load_link(self):
        self.links = {}
        for link in self.feed['link']:
            self.links[link['rel']] = link['href']

    @property
    def entries(self):
        if self.feed:
            return [self.converter(entry) for entry in self.feed['entry']]
        return []

    @property
    def next_link(self):
        return self.links.get('next')

    @property
    def prev_link(self):
        return self.links.get('previous')


class GmailContact(object):
    def __init__(self, entry):
        self.entry = entry

    @property
    def id(self):
        return self.entry['id']

    @property
    def updated(self):
        return self.entry['updated']

    @property
    def name(self):
        return self.entry.get('title', {}).get('$t', '')

    @property
    def emails(self):
        emails = []
        for e in self.entry['gd$email']:
            emails.append(e.get('address'))
        return emails

    @property
    def category(self):
        return self.entry['category']

    @property
    def link(self):
        return self.entry['link']
