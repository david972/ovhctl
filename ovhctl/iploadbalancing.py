#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
iploadbalancing OVH resource

Authors:
    - David ALEXANDRE <david.alexandre@bluelabs.fr>

"""
import logging
import yaml
import os

LOG = logging.getLogger(__name__)
resourceName = 'ipLoadbalancing'
class Iploadbalancing:
    arguments = {}
    def __init__(self, client, arguments):
        """Main function"""
        self.arguments = arguments
        self.client = client

    def read_(self):
        servicename = None
        data = {}
        if self.arguments['<servicename>']:
            LOG.debug("set servicename = %s" % self.arguments['<servicename>'])
            servicename = self.arguments['<servicename>']
        if servicename and self.arguments['--farm']:
            return self.getFarm(servicename)
        if servicename:
            LOG.debug("uri /%s/%s" % (resourceName, servicename))
            return self.client.get("/%s/%s" % (resourceName, servicename))
        else:
            LOG.debug("uri /%s" % resourceName)
            return self.client.get("/%s" % resourceName)
        return data

    def getFarm(self, servicename):
        if self.arguments['<farm>']:
            LOG.debug("uri /%s/%s/http/farm/%s" % (resourceName, servicename, self.arguments['<farm>']))
            return self.client.get("/%s/%s/http/farm/%s" % (resourceName, servicename, self.arguments['<farm>']))
        LOG.debug("uri /%s/%s/http/farm" % (resourceName, servicename))
        return self.client.get("/%s/%s/http/farm" % (resourceName, servicename))

    def create_(self):
        data = {}
        req = {}
        if not self.arguments['<filename>'] or not os.path.isfile(self.arguments['<filename>']):
            LOG.error("File not exists")
            return data
        with open(self.arguments['<filename>'], 'r') as stream:
            try:
                req = yaml.safe_load(stream)
            except yaml.YAMLError as e:
                LOG.error(e)
                return {}
        self.client.post('/%s/%s/http/farm' % (resourceName, req['servicename']), 
            balance=req['balance'],
            displayName=req['displayName'],
            port=req['port'],
            probe=req['probe'],
            stickiness=req['stickiness'],
            vrackNetworkId=req['vrackNetworkId'],
            zone=req['zone'],
        )
        return data

    def run(self):
        if self.arguments["get"]:
            return self.read_()
        if self.arguments["create"]:
            return self.create_()
        if self.arguments["delete"]:
            print("delete")
            return []
        if self.arguments["update"]:
            print("update")
            return []
        raise Exception('command erreur')

