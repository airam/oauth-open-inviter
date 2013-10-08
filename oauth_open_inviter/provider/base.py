class BaseProvider(object):
    """
    Abstract class for contact importing
    """

    def __init__(self, *args, **kwargs):
        pass

    def get_contacts(self):
        """
        Implements a generator for iterating in contacts
        """
        raise NotImplementedError()

    def get_all_contacts(self):
        """
        Returns a contact list
        """
        return [c for c in self.get_contacts()]
