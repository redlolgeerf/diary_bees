#!/usr/bin/env python
# encoding: utf-8

import requests
from bs4 import BeautifulSoup
from django.conf import settings

class BeeParser(object):
    '''
    Receive profile page and make list of bees:
    [tuple(id, name)]
    Page structure is like:
        <body>
        <div id="contant">
        <p align="justify"><a>BEE</a></p>
        </div>
        </body>
    '''
    def __init__(self, page):
        self.bees = []
        page = BeautifulSoup(page)
        div = page.find_all(id="contant")
        if div:
            bee_tag = page.find_all(self.b_sort)[-1]
            for tag in bee_tag:
                if tag.name != 'a':
                    continue
                self.bees.append((self.uid_from_href(tag['href']), tag.text))

    def uid_from_href(self, srting):
        return srting.split('?')[1]

    def b_sort(self, tag):
        '''
        Only <p align="justify"> contains needed information.
        '''
        try:
            if tag.name == 'p' and tag['align'] == "justify":
                return True
        except KeyError:
            return False

class Grabber(object):
    '''
    Grab user pages from diary while persisting session.
    Usage:
        g = Grabber()
        print(g.get_bees(1692226))
    '''

    DIARY_URL = settings.DIARY_URL
    PROFILE_URL = settings.PROFILE_URL
    USERNAME = settings.USERNAME
    PASS = settings.PASS
    PASS_HASH = settings.PASS_HASH

    def __init__(self):
        self._session = None
        self._cookies_set = False

    @property
    def session(self):
        '''
        Return session, create one if none.
        '''
        if not self._session:
            self._session = requests.Session()
        return self._session

    def authenticate(self):
        """
        Login to diary.
        Does not work. God knows why.
        """
        r = self.session.get(self.DIARY_URL)
        page = BeautifulSoup(r.text)

        forms = page.find_all('form')
        for form in forms:
            if 'login.php' in form['action']:
                login_form = form
                break
        LOGIN_URL = login_form['action']
        def sig(tag):
            try:
                s = tag.get('name', None)
                if s == 'signature':
                    return True
            except AttributeError:
                pass
        signature = login_form.find(sig)['value']

        params = {
                'user_login': self.USERNAME,
                'user_pass': self.PASS,
                'save': 'on',
                'signature': signature,
               }
        r = self.session.post(self.DIARY_URL + LOGIN_URL,
                              params=params, allow_redirects=True)

    def get(self, url, **option):
        '''
        Just calls session.get with **option, but ensures,
        that we have right cookies.
        '''
        if not self._cookies_set:
            cookies = dict(user_login=self.USERNAME, user_pass=self.PASS_HASH)
            page = self.session.get(url, cookies=cookies, **option)
            self._cookies_set = True
        else:
            page = self.session.get(url, **option)
        return page

    def get_profile_page(self, d_id):
        '''
        Return page of member's profile.
        '''
        url = self.DIARY_URL + self.PROFILE_URL.format(d_id)
        return self.get(url)

    def get_bees(self, uid):
        '''
        Download the page and grab bees with bees parser.
        '''
        page = self.get_profile_page(uid).content
        return BeeParser(page).bees
