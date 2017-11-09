#!/usr/bin/env python

"""
YAML support is not part of the Python standard library, so it is possible that
users may find themselves running MARBL scripts in an environment that does not
have PyYAML. To support those users, MARBL developers provide a JSON version of
default_settings.yaml which can be generated by this script (provided the script
is run on a machine with PyYAML).

usage: yaml_to_json.py [-h] [-y YAML_FILE] [-j JSON_FILE]

Convert a YAML file to JSON

optional arguments:
  -h, --help            show this help message and exit
  -y YAML_FILE, --yaml_file YAML_FILE
                        Location of YAML-formatted MARBL configuration file to
                        convert to JSON (default: $MARBLROOT/
                        default_settings.yaml)
  -j JSON_FILE, --json_file JSON_FILE
                        JSON file to be created (default: $MARBLROOT/
                        autogenerated_src/default_settings.json)

"""

#######################################

def _parse_args(marbl_root):
    """ Parse command line arguments
    """

    import argparse
    import os

    parser = argparse.ArgumentParser(description="Convert a YAML file to JSON",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # Command line argument to point to YAML file (default is $MARBLROOT/src/default_settings.yaml)
    parser.add_argument('-y', '--yaml_file', action='store', dest='yaml_file',
                        default=os.path.join(marbl_root, 'src', 'default_settings.yaml'),
                        help='Location of YAML-formatted MARBL configuration file to convert to JSON')

    parser.add_argument('-j', '--json_file', action='store', dest='json_file',
                        default=os.path.join(marbl_root, 'autogenerated_src', 'default_settings.json'),
                        help="JSON file to be created")

    return parser.parse_args()

#######################################

import sys, os, json

# marbl_root is the top-level MARBL directory
marbl_root = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), '..'))
sys.path.append(marbl_root)

# Parse command-line arguments (marbl_root is used to set default for YAML file location)
args = _parse_args(marbl_root)

# Set up logging
import logging
logging.basicConfig(format='%(levelname)s (%(funcName)s): %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

# This tool requires PyYAML, error if it is not available
try:
    import yaml
except:
    logger.error("Can not find PyYAML library")

# Read YAML file
with open(args.yaml_file) as file_in:
    yaml_in = yaml.safe_load(file_in)

# Verify YAML file is consistent with MARBL-defined schema
from MARBL_tools import settings_file_is_consistent
if not settings_file_is_consistent(yaml_in):
    logger.error("Formatting error in %s" % args.yaml_file)
    sys.exit(1)

# Write JSON file
with open(args.json_file, "w") as file_out:
    json.dump(yaml_in, file_out, separators=(',', ': '), sort_keys=True, indent=3)



