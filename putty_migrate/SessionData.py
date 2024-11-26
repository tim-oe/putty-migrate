import pprint

class SessionData:
    def __init__(self, name: str = None, host: str = None, user: str = None, key: str = None, title: str = None):
        self._name = name
        self._host = host
        self._user = user
        self._key = key
        self._title = title

    def __str__(self):
        return pprint.pformat(self.__dict__)

    @property
    def name(self):
        """
        name property getter
        :param self: this
        :return: the name
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        name property setter
        :param self: this
        :param: the name
        """
        self._name = name

    @property
    def host(self):
        """
        host property getter
        :param self: this
        :return: the host
        """
        return self._host

    @host.setter
    def host(self, host):
        """
        host property setter
        :param self: this
        :param: the host
        """
        self._host = host

    @property
    def user(self):
        """
        user property getter
        :param self: this
        :return: the user
        """
        return self._user

    @user.setter
    def user(self, user):
        """
        user property setter
        :param self: this
        :param: the user
        """
        self._user = user

    @property
    def key(self):
        """
        key property getter
        :param self: this
        :return: the key
        """
        return self._key

    @key.setter
    def key(self, key):
        """
        key property setter
        :param self: this
        :param: the key
        """
        self._key = key

    @property
    def title(self):
        """
        title property getter
        :param self: this
        :return: the title
        """
        return self._title

    @title.setter
    def title(self, title):
        """
        title property setter
        :param self: this
        :param: the title
        """
        self._title = title
