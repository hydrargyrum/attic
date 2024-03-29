#!/usr/bin/env python3
# SPDX-License-Identifier: WTFPL

# /// script
# dependencies = ["requests"]
# ///

import argparse
import json
import os
from urllib.parse import urljoin

import requests


# parser
parser = argparse.ArgumentParser(description="Send a Gotify notification")
parser.add_argument("--url", default=os.environ.get("GOTIFY_URL"), help="URL of Gotify server")
parser.add_argument("-t", "--title", help="Notification title")
parser.add_argument("-p", "--priority", type=int, default=0, help="Notification priority (default: 0)")
parser.add_argument("-e", "--extra", action="append", metavar="NAMESPACE::ACTION::KEY=VALUE", default=[])
parser.add_argument("--timeout", type=int, default=60, help="Timeout in seconds for Gotify connection (default: 60)")
parser.add_argument("message", nargs="+")
args = parser.parse_args()

# extra
extra = {}
# foo::bar::baz.qux=42 => {"foo::bar": {"baz": {"qux": "42"}}}
for kv in args.extra:
	k, sep, v = kv.partition("=")
	if not sep:
		parser.error(f"bad extra format: {kv}")
	namespace, sep, k = k.rpartition("::")
	if not sep:
		parser.error(f"bad extra format: {kv}")

	subd = extra.setdefault(namespace, {})
	ks = k.split(".")
	for subk in ks[:-1]:
		subd = subd.setdefault(subk, {})
	subd[ks[-1]] = v

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
response = session.post(
	urljoin(args.url, "message"), json=pdata, timeout=args.timeout,
)
response.raise_for_status()

print(json.dumps(response.json(), indent=2))
