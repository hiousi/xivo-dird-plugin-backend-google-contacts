XiVO dird plugin google contacts
================================

[![Build Status](https://travis-ci.org/sboily/xivo-dird-plugin-backend-google-contacts.png?branch=master)](https://travis-ci.org/sboily/xivo-dird-plugin-backend-google-contacts)


## Info

This plugin getting contacts from google contacts.

## How to use

In your config.yml enabled the gcontacts plugin

    enabled_plugins:
        backends:
            - gcontacts

and added the source like

    services:
        lookup:
            default:
                sources:
                    - google_contacts

Finally added a configuration for the source in the sources.d like google_contacts.yml

    type: gcontacts
    name: google_contacts
    gcontacts_config:
        username: my_username@gmail.com
        password: my_password
        max_results: 100