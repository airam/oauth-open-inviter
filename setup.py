from distutils.core import setup

setup(
    name = "oauth_open_inviter",
    version = "0.1",
    author = "airam",
    author_email = "airam@ninjadevs.com",
    description = """Allows to export user contacts from Google, Yahoo! and Hotmail using oauth(2).
                    Based in django-oauth-access(https://github.com/eldarion/django-oauth-access/) and Python-contact-importer(https://github.com/millioner/Python-contact-importer)""",
    long_description = open("README.md").read(),
    license = "BSD",
    url = "https://github.com/airam/oauth_open_inviter",
    packages = [
        "oauth_open_inviter",
        "oauth_open_inviter.lib",
        "oauth_open_inviter.oauth_access",
        "oauth_open_inviter.oauth_access.utils",
        "oauth_open_inviter.provider",
        "oauth_open_inviter.provider.google",
        "oauth_open_inviter.provider.hotmail",
        "oauth_open_inviter.provider.yahoo",
        ],
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
        ]
)
