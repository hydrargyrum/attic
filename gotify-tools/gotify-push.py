#!/usr/bin/env python3
# SPDX-License-Identifier: WTFPL

import argparse
import json
import os
from urllib.parse import urljoin

import requests


# parser
parser = argparse.ArgumentParser()
parser.add_argument("--url", default=os.environ.get("GOTIFY_URL"))
parser.add_argument("--title")
parser.add_argument("--priority", type=int, default=0)
parser.add_argument("--extra", action="append", metavar="NAMESPACE::ACTION::KEY=VALUE", default=[])
parser.add_argument("message", nargs="+")
args = parser.parse_args()

# extra
extra = {}
for kv in args.extra:
	k, sep, v = kv.partition("=")
	if not sep:
		parser.error(f"bad extra format: {kv}")
	k, sep, subk = k.rpartition("::")
	if not sep:
		parser.error(f"bad extra format: {kv}")
	extra.setdefault(k, {})[subk] = v

# session
session = requests.Session()
session.headers["X-Gotify-Key"] = os.environ["GOTIFY_TOKEN"]

# data to post
pdata = {
	"title": args.title,
	"priority": args.priority,
	"message": " ".join(args.message),
	"extras": extra,
}

# request
response = session.post(urljoin(args.url, "message"), json=pdata)
response.raise_for_status()

print(json.dumps(response.json(), indent=2))
