# -*- coding: utf-8 -*-
#
# Copyright (C) 2014 Sylvain Boily
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>

import logging

from xivo_dird import BaseSourcePlugin
from xivo_dird import make_result_class
import gdata.contacts.client

logger = logging.getLogger(__name__)


class GcontactsPlugin(BaseSourcePlugin):

    def load(self, args):
        self._gcontacts_config = args['config']['gcontacts_config']
        self.name = args['config']['name']
        logger.debug('gcontacts config %s', self._gcontacts_config)
        self.contact_client = gdata.contacts.client.ContactsClient()
        self.contact_client.ClientLogin(self._gcontacts_config['username'], self._gcontacts_config['password'], "")
        self._SourceResult = make_result_class(self.name, None,
                                               source_to_dest_map=args['config'].get(self.SOURCE_TO_DISPLAY))

    def name(self):
        return self.name

    def search(self, term, profile=None, args=None):
        contents = self._fetch_content(term=term)
        
        return [self._source_result_from_content(content) for content in contents]

    def _source_result_from_content(self, content):
        return self._SourceResult(content)

    def _fetch_content(self, term):
        query = gdata.contacts.client.ContactsQuery(text_query=term.encode("UTF-8"))
        query.max_results = self._gcontacts_config['max_results']
        feed = self.contact_client.GetContacts(q=query)

        if not feed.entry:
            return ()

        return [self._result_from_query(entry) for entry in feed.entry if self._result_from_query(entry)]


    def _result_from_query(self, entry):
        contact = { 'firstname' : None,
                    'lastname' : None,
                    'number' : None,
                    'email' : None,
                    'entity' : None,
                    'faxnumber' : None,
                    'mobile_phone_number' : None,
                  }

        if entry.name:
            if entry.name.given_name:
                contact['firstname'] = entry.name.given_name.text.encode("UTF-8")
            if entry.name.family_name:
                contact['lastname'] = entry.name.family_name.text.encode("UTF-8")
        else:
            return False

        if entry.organization and entry.organization.name:
            contact['entity'] = entry.organization.name.text.encode("UTF-8")

        for phone in entry.phone_number:
            phone_type = phone.rel.split('#')[1]
            if "home" in phone_type:
                contact['number'] = phone.text
            if "mobile" in phone_type:
                contact['mobile_phone_number'] = phone.text
            if "work" in phone_type:
                contact['number'] = phone.text

        for email in entry.email:
            if email.primary and email.primary == 'true':
                contact['email'] = email.address

        return contact
