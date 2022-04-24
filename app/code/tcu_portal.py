from calendar import c
import re
from xml.dom.minidom import Attr
import requests
from bs4 import BeautifulSoup
import hashlib
import datetime

class TcuPortal:
    def __init__(self, id_, pw, user='', sso=True):
        # Start session
        self.session = requests.session()
        self.user = user

        if sso:
            self.login_with_sso(id_, pw)
        else:
            self.login_with_org(id_, pw)

        self.message_page  = None
        self.oshirase_page = None
        self.daredemo_page = None

    def login_with_org(self, id_, pw):
        # Access to TCU portal
        page = self.session.get('https://portal.off.tcu.ac.jp/OldIndex.aspx')
        if page.status_code != requests.codes.ok:
            raise Exception('TCUポータルサイトにアクセスできません。')

        # Login with TCU account
        data = self.get_asp_event(page, 'btnLogin')
        data.update({
            'txtLoginId': id_,
            'txtPassword': pw
        })
        self.top_page = self.session.post('https://portal.off.tcu.ac.jp/OldIndex.aspx', data=data)
        if self.top_page.status_code != requests.codes.ok:
            raise Exception('TCUポータルサイトへのログインに失敗しました。')

    def login_with_sso(self, id_, pw):
        # SSO header
        sso_headers = {
            'User-Agent': 'Crawler (Mozilla/5.0)' # Mozilla/5.0がないと認証することすら認めてくれない
        }

        # Access to TCU portal
        page = self.session.get('https://portal.off.tcu.ac.jp/')
        if page.status_code != requests.codes.ok:
            raise Exception('TCUポータルサイトにアクセスできません。')

        # Redirect to SSO page
        data = {
            '_eventId_proceed': ''
        }
        page = self.session.post(page.url, data=data, headers=sso_headers)
        if page.status_code != requests.codes.ok:
            raise Exception('TCUポータルサイトのSSOページのリダイレクトに失敗しました。')

        # Login with TCU account
        data = {
            'twauthstatus': 'useridpwd',
            'twuser': id_,
            'twpassword': pw,
            'login': 'ログイン'
        }
        page = self.session.post('https://sso.tcu.ac.jp/idp/Authn/External?conversation=e2s1', data=data, headers=sso_headers)
        if page.status_code != requests.codes.ok:
            raise Exception('TCUポータルサイトにアクセスできません。')

        if 'ユーザー名またはパスワードが違います。' in page.text:
            raise Exception('TCUポータルサイトへのログインに失敗しました。')

        # Redirect to TCU portal
        bs = BeautifulSoup(page.text, 'html.parser')
        data = {
            'RelayState': bs.find(attrs={'name': 'RelayState'}).get('value'),
            'SAMLResponse': bs.find(attrs={'name': 'SAMLResponse'}).get('value')
        }
        self.top_page = self.session.post('https://portal.off.tcu.ac.jp/Shibboleth.sso/SAML2/POST', data=data)
        if self.top_page.status_code != requests.codes.ok:
            raise Exception('TCUポータルサイトのSSOページのリダイレクトに失敗しました。')

    def logout(self):
        # Logout
        data = self.get_asp_event(self.top_page, 'ctl00$ctl00$btnLogoutBtn')
        self.session.post(self.top_page.url, data=data)

    def get_asp_event(self, page, asp_target):
        bs = BeautifulSoup(page.text, 'html.parser')

        data = {
            '__VIEWSTATE'         : bs.find(attrs={'name': '__VIEWSTATE'         }).get('value'),
            '__VIEWSTATEGENERATOR': bs.find(attrs={'name': '__VIEWSTATEGENERATOR'}).get('value'),
            '__VIEWSTATEENCRYPTED': bs.find(attrs={'name': '__VIEWSTATEENCRYPTED'}).get('value'),
            '__EVENTVALIDATION'   : bs.find(attrs={'name': '__EVENTVALIDATION'   }).get('value'),
            '__EVENTTARGET'       : asp_target
        }
        return data
    
    def get_message_list(self, since=None, until=None):
        # Access to message page
        if self.message_page is None:
            data = self.get_asp_event(self.top_page, 'ctl00$ctl00$MainContent$Contents$ExLinkButton2')
            self.message_page = self.session.post(self.top_page.url, data=data)
            if self.message_page.status_code != requests.codes.ok:
                raise Exception('TCUポータルサイトのメッセージページにアクセスできません。')
        message_page = self.message_page

        messages = []
        while True:
            # Parse message page
            message_bs = BeautifulSoup(message_page.text, 'html.parser')
            table = message_bs.find(attrs={'id': 'MainContent_Contents_updPanel'}).findAll('table', class_='dv')[0].findAll('tr', recursive=False)[1:]

            # Get messages
            for line in table:
                # Check date
                date = line.findAll('td')[1].get_text().strip()
                date = datetime.datetime.strptime(date, '%Y/%m/%d %H:%M:%S')
                if since is not None and date < since:
                    return messages
                if until is not None and date > until:
                    continue

                # Get message details
                asp_target = line.find('a').get('href')
                asp_target = re.findall('^javascript:__doPostBack\\(\'([^\']+)\'.+\\)$', asp_target)[0]
                data = self.get_asp_event(message_page, asp_target)
                message_detail_page = self.session.post(message_page.url, data=data)
                if message_detail_page.status_code != requests.codes.ok:
                    raise Exception('TCUポータルサイトのメッセージ詳細ページにアクセスできません。')
                detail_bs = BeautifulSoup(message_detail_page.text, 'html.parser')

                # Replace return code
                for i in detail_bs.select('br'):
                    i.replace_with('\n')

                # Get message
                message = {
                    'date'     : detail_bs.find(attrs={'id': 'MainContent_Contents_lblDate'      }).get_text(),
                    'sender'   : detail_bs.find(attrs={'id': 'MainContent_Contents_lblSender'    }).get_text(),
                    'title'    : detail_bs.find(attrs={'id': 'MainContent_Contents_lblTitle'     }).get_text(),
                    'important': detail_bs.find(attrs={'id': 'MainContent_Contents_lblImportance'}).get_text() == '重要',
                    'body'     : detail_bs.find(attrs={'id': 'MainContent_Contents_lblBody'      }).get_text()
                }
                message['id'] = hashlib.md5('tcu_portal_message::{date}_{sender}_{title}::{user}'.format(**message, user=self.user).encode()).hexdigest()

                # Add file links
                file_links = []
                file_d = detail_bs.find(attrs={'id': 'TblFile'})
                if file_d is not None:
                    for a in file_d.findAll('a'):
                        asp_target = a.get('href')
                        asp_target = re.findall('^javascript:__doPostBack\\(\'([^\']+)\'.+\\)$', asp_target)[0]
                        data = self.get_asp_event(message_detail_page, asp_target)
                        file_page = self.session.post(message_detail_page.url, data=data, allow_redirects=False)
                        file_link = {
                            'name': a.get_text().strip(),
                            'url' : 'https://portal.off.tcu.ac.jp' + file_page.headers['Location']
                        }
                        file_links.append(file_link)
                data['file_links'] = file_links

                # Add URL links
                url_links = []
                url_d = detail_bs.find(attrs={'id': 'MainContent_Contents_trURLLink'})
                if url_d is not None:
                    for tr in url_d.findAll('tr'):
                        td = tr.findAll('td')
                        url_link = {
                            'name': td[2].get_text().strip(),
                            'url' : td[1].get_text().strip()
                        }
                        url_links.append(url_link)
                data['url_links'] = url_links

                messages.append(message)

            # Next page
            asp_target = message_bs.find(attrs={'id': 'MainContent_Contents_ContactsDataPager'}).findAll('a')[-2].get('href')
            if asp_target is None:
                return messages
            asp_target = re.findall('^javascript:__doPostBack\\(\'([^\']+)\'.+\\)$', asp_target)[0]
            data = self.get_asp_event(message_page, asp_target)
            message_page = self.session.post(message_page.url, data=data)
            if message_page.status_code != requests.codes.ok:
                raise Exception('TCUポータルサイトのメッセージページにアクセスできません。')

    def get_oshirase_list(self, since=None, until=None):
        # Access to oshirase page
        if self.oshirase_page is None:
            data = self.get_asp_event(self.top_page, 'ctl00$ctl00$MainContent$Contents$lnkBtnOsrList')
            self.oshirase_page = self.session.post(self.top_page.url, data=data)
            if self.oshirase_page.status_code != requests.codes.ok:
                raise Exception('TCUポータルサイトのお知らせページにアクセスできません。')
        oshirase_page = self.oshirase_page

        oshirases = []
        while True:
            # Parse oshirase page
            oshirase_bs = BeautifulSoup(oshirase_page.text, 'html.parser')
            table = oshirase_bs.find(attrs={'id': 'MainContent_Contents_updPanel'}).findAll('table', class_='dv')[0].findAll('tr', recursive=False)[1:]

            # Get oshirases
            for line in table:
                # Check date
                date = line.findAll('td')[0].get_text().strip()
                date = datetime.datetime.strptime(date, '%Y/%m/%d')
                if since is not None and date < since:
                    return oshirases
                if until is not None and date > until:
                    continue

                # Get oshirase details
                asp_target = line.find('a').get('href')
                asp_target = re.findall('^javascript:__doPostBack\\(\'([^\']+)\'.+\\)$', asp_target)[0]
                data = self.get_asp_event(oshirase_page, asp_target)
                oshirase_detail_page = self.session.post(oshirase_page.url, data=data)
                if oshirase_detail_page.status_code != requests.codes.ok:
                    raise Exception('TCUポータルサイトのお知らせ詳細ページにアクセスできません。')
                detail_bs = BeautifulSoup(oshirase_detail_page.text, 'html.parser')

                # Replace return code
                for i in detail_bs.select('br'):
                    i.replace_with('\n')

                # Get oshirase
                oshirase = {
                    'date'      : line.findAll('td')[0].get_text().strip(),
                    'registrant': detail_bs.find(attrs={'id': 'MainContent_Contents_lblRegistrant'}).get_text(),
                    'title'     : detail_bs.find(attrs={'id': 'MainContent_Contents_lblTitle'     }).get_text(),
                    'body'      : detail_bs.find(attrs={'id': 'MainContent_Contents_lblBody'      }).get_text()
                }
                oshirase['id'] = hashlib.md5('tcu_portal_oshirase::{date}_{registrant}_{title}::{user}'.format(**oshirase, user=self.user).encode()).hexdigest()

                # Add file links
                file_links = []
                file_d = detail_bs.find(attrs={'id': 'TblFile'})
                if file_d is not None:
                    for a in file_d.findAll('a'):
                        asp_target = a.get('href')
                        asp_target = re.findall('^javascript:__doPostBack\\(\'([^\']+)\'.+\\)$', asp_target)[0]
                        data = self.get_asp_event(oshirase_detail_page, asp_target)
                        file_page = self.session.post(oshirase_detail_page.url, data=data, allow_redirects=False)
                        file_link = {
                            'name': a.get_text().strip(),
                            'url' : 'https://portal.off.tcu.ac.jp' + file_page.headers['Location']
                        }
                        file_links.append(file_link)
                oshirase['file_links'] = file_links

                # Add URL links
                url_links = []
                url_d = detail_bs.find(attrs={'id': 'MainContent_Contents_trURLLink'})
                if url_d is not None:
                    for tr in url_d.findAll('tr'):
                        td = tr.findAll('td')
                        url_link = {
                            'name': td[2].get_text().strip(),
                            'url' : td[1].get_text().strip()
                        }
                        url_links.append(url_link)
                oshirase['url_links'] = url_links

                oshirases.append(oshirase)

            # Next page
            asp_target = oshirase_bs.find(attrs={'id': 'MainContent_Contents_ContactsDataPager'}).findAll('a')[-2].get('href')
            if asp_target is None:
                return oshirases
            asp_target = re.findall('^javascript:__doPostBack\\(\'([^\']+)\'.+\\)$', asp_target)[0]
            data = self.get_asp_event(oshirase_page, asp_target)
            oshirase_page = self.session.post(oshirase_page.url, data=data)
            if oshirase_page.status_code != requests.codes.ok:
                raise Exception('TCUポータルサイトのお知らせページにアクセスできません。')
    
    def get_daredemo_list(self, since=None, until=None):
        # Access to daredemo page
        if self.daredemo_page is None:
            data = self.get_asp_event(self.top_page, 'ctl00$ctl00$MainContent$Contents$ExLinkButton4')
            self.daredemo_page = self.session.post(self.top_page.url, data=data)
            if self.daredemo_page.status_code != requests.codes.ok:
                raise Exception('TCUポータルサイトの誰でも投稿ページにアクセスできません。')
        daredemo_page = self.daredemo_page

        daredemos = []
        while True:
            # Parse daredemo page
            daredemo_bs = BeautifulSoup(daredemo_page.text, 'html.parser')
            table = daredemo_bs.find(attrs={'id': 'MainContent_Contents_updPanel'}).findAll('table', class_='dv')[1].findAll('tr', recursive=False)[1:]

            # Get daredemos
            for line in table:
                # Check date
                date = line.findAll('td')[0].get_text().strip()
                date = datetime.datetime.strptime(date, '%Y/%m/%d')
                if since is not None and date < since:
                    return daredemos
                if until is not None and date > until:
                    continue

                # Get daredemo details
                asp_target = line.find('a').get('href')
                asp_target = re.findall('^javascript:__doPostBack\\(\'([^\']+)\'.+\\)$', asp_target)[0]
                data = self.get_asp_event(daredemo_page, asp_target)
                daredemo_detail_page = self.session.post(daredemo_page.url, data=data)
                if daredemo_detail_page.status_code != requests.codes.ok:
                    raise Exception('TCUポータルサイトの誰でも投稿詳細ページにアクセスできません。')
                detail_bs = BeautifulSoup(daredemo_detail_page.text, 'html.parser')

                # Replace return code
                for i in detail_bs.select('br'):
                    i.replace_with('\n')

                # Get daredemo
                daredemo = {
                    'date'      : line.findAll('td')[0].get_text().strip(),
                    'registrant': detail_bs.find(attrs={'id': 'MainContent_Contents_lblRegistrant'}).get_text(),
                    'title'     : detail_bs.find(attrs={'id': 'MainContent_Contents_lblTitle'     }).get_text(),
                    'body'      : detail_bs.find(attrs={'id': 'MainContent_Contents_lblBody'      }).get_text()
                }
                daredemo['id'] = hashlib.md5('tcu_portal_daredemo::{date}_{registrant}_{title}::{user}'.format(**daredemo, user=self.user).encode()).hexdigest()

                # Add file links
                file_links = []
                file_d = detail_bs.find(attrs={'id': 'TblFile'})
                if file_d is not None:
                    for a in file_d.findAll('a'):
                        asp_target = a.get('href')
                        asp_target = re.findall('^javascript:__doPostBack\\(\'([^\']+)\'.+\\)$', asp_target)[0]
                        data = self.get_asp_event(daredemo_detail_page, asp_target)
                        file_page = self.session.post(daredemo_detail_page.url, data=data, allow_redirects=False)
                        file_link = {
                            'name': a.get_text().strip(),
                            'url' : 'https://portal.off.tcu.ac.jp' + file_page.headers['Location']
                        }
                        file_links.append(file_link)
                daredemo['file_links'] = file_links

                # Add URL links
                url_links = []
                url_d = detail_bs.find(attrs={'id': 'MainContent_Contents_trURLLink'})
                if url_d is not None:
                    for tr in url_d.findAll('tr'):
                        td = tr.findAll('td')
                        url_link = {
                            'name': td[2].get_text().strip(),
                            'url' : td[1].get_text().strip()
                        }
                        url_links.append(url_link)
                daredemo['url_links'] = url_links

                daredemos.append(daredemo)

            # Next page
            asp_target = daredemo_bs.find(attrs={'id': 'MainContent_Contents_ExDataPager1'}).findAll('a')[-2].get('href')
            if asp_target is None:
                return daredemos
            asp_target = re.findall('^javascript:__doPostBack\\(\'([^\']+)\'.+\\)$', asp_target)[0]
            data = self.get_asp_event(daredemo_page, asp_target)
            daredemo_page = self.session.post(daredemo_page.url, data=data)
            if daredemo_page.status_code != requests.codes.ok:
                raise Exception('TCUポータルサイトの誰でも投稿ページにアクセスできません。')
