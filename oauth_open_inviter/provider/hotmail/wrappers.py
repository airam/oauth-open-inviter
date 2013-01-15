class HotmailFeed(object):
    def __init__(self, feed, converter):
        self.feed = feed
        self.converter = converter

    @property
    def entries(self):
        if self.feed:
            return [self.converter(entry) for entry in self.feed['entry']]
        return []

    @property
    def next_link(self):
        return self.feed['paging'].get('next')

    @property
    def prev_link(self):
        return self.feed['paging'].get('previous')


class HotmailContact(object):
    def __init__(self, entry):
        self.entry = entry

    @property
    def id(self):
        return self.entry['id']

    @property
    def updated(self):
        return self.entry['updated_time']

    @property
    def first_name(self):
        return self.entry.get('first_name')

    @property
    def last_name(self):
        return self.entry.get('last_name')

    @property
    def name(self):
        return self.entry.get('name', '')

    @property
    def emails(self):
        emails = []
        for e in self.entry['email_hashes']:
            emails.append(e)
        return emails

    @property
    def user_id(self):
        return self.entry['user_id']

    @property
    def is_friend(self):
        return self.entry['is_friend']

    @property
    def is_favorite(self):
        return self.entry['is_favorite']

    @property
    def gender(self):
        return self.entry['gender']
