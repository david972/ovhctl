# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
ovhctl OVH API client

Authors:
    - David ALEXANDRE <david.alexandre@bluelabs.fr>

ovhctl get|create|delete|update iploadbalancing
Usage:
    ovhctl (-h | --help)
    ovhctl get iploadbalancing [<servicename>] [--farm <farm>] [--level <level>] [--output <format>]
    ovhctl create iploadbalancing --file <filename> [--level <level>] [--output <format>]

Options:
    -h, --help
        show this screen
    --level <debug|info|warn|error>
        Logger level
        values are: "debug" "info" "warm" and "error"
        [default: info]
    --output (yaml|json|table)
        Output format
        [default: json]
"""
from __future__ import (unicode_literals, absolute_import, print_function,)

# standard
import os
import sys
import logging

# third-party
import json
import yaml
import colorlog
import ovh
from docopt   import docopt, DocoptExit
from tabulate import tabulate
from operator import itemgetter

# local
from ovhctl.release import __version__
from ovhctl.iploadbalancing import Iploadbalancing

LOG = logging.getLogger(__name__)

def init_logger(level):
    """init the logger
    Args:
        level (str): level of log (debug, info, warn, error)
    """

    if "color" in os.environ.get("TERM", ""):
        console_formatter = colorlog.ColoredFormatter('%(log_color)s%(message)s')
        console_handler = colorlog.StreamHandler()
    else:
        console_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s',"%Y-%m-%d %H:%M:%S")
        console_handler = logging.StreamHandler()

    console_handler.setFormatter(console_formatter)

    logger = logging.getLogger("ovhctl")
    logger.addHandler(console_handler)
    logger.setLevel(getattr(logging, level.upper()))

def output_(data, format):
    """output format"""
    if data == None or len(data) == 0:
        LOG.info("No resource")
        sys.exit(0)
    # if len(data) == 1 and data[list(data.keys())[0]]['vCPU'] == 0:
    #     LOG.info("No resource")
    #     sys.exit(0)
    if format == "json":
        print(json.dumps(data, indent=2, sort_keys=True))
    elif format == "yaml":
        print(yaml.safe_dump(data,default_flow_style=False))
    else:
        print("table")
        # result = []
        # for group in data:
        #     result.append([
        #         group,
        #         data[group]['vCPU'],
        #         data[group]['MEM'],
        #         data[group]['HDD']
        #     ])
        # headers = [u'Group', u'CPU', u'MEM', u'HDD']
        # sorted_result = sorted(result, key=itemgetter(0))
        # print(tabulate(
        #     sorted_result,
        #     headers=headers,
        #     tablefmt="simple").encode('utf-8')
        # )

def main():
    """ Main function """
    try:
        arguments = docopt(__doc__, version=__version__)
        init_logger(arguments['--level'])
    except DocoptExit:
        print(__doc__)
        sys.exit(1)
    if not os.path.isfile(os.path.expanduser("~/.ovh.conf")):
        LOG.error("Configuration your ovh credential first")
        sys.exit(2)
    client = ovh.Client(config_file=os.path.expanduser("~/.ovh.conf"))
    if arguments['--output'] not in [ 'json', 'yaml', 'table']:
        LOG.error("Incorrect output format")
        print(__doc__)
        sys.exit(3)
    if arguments.get("iploadbalancing"):
        LOG.debug("ip iploadbalancing")
        ib = Iploadbalancing(arguments=arguments, client=client)
        data = ib.run()
        output_(data, format=arguments['--output'])
        sys.exit(0)

if __name__ == "__main__":
    main()