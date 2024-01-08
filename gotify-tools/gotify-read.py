#!/usr/bin/env python3
# SPDX-License-Identifier: WTFPL

import argparse
import json
import os
import re
from urllib.parse import urljoin

import requests


# parser
parser = argparse.ArgumentParser(
	description="Read Gotify notifications and output in JSON",
)
parser.add_argument("--url", help="URL of Gotify server")
parser.add_argument("--limit", type=int, help="Limit the number of retrieved messages")
parser.add_argument("--after", type=int, help="Display messages after this id only")
parser.add_argument("--appid", type=int, dest="app_id", help="Gotify app (reader) ID")
parser.add_argument("--pretty", action="store_true", help="Display in human format instead of JSON")
args = parser.parse_args()

if not args.url:
	parser.error("missing --url param")

# session
session = requests.Session()
session.headers["X-Gotify-Key"] = os.environ["GOTIFY_TOKEN"]

# url
route = "message"
if args.app_id:
	route = f"application/{args.app_id}/message"

# request
response = session.get(urljoin(args.url, route))
response.raise_for_status()

# paging loop
messages = []
while True:
	jdata = response.json()
	messages.extend(jdata["messages"])

	if args.limit and len(messages) >= args.limit:
		messages = messages[:args.limit]
		break
	if args.after and messages and messages[-1]["id"] <= args.after:
		messages = [
			msg for msg in messages
			if msg["id"] > args.after
		]
		break

	next_url = jdata["paging"].get("next")
	if not next_url:
		break
	response = session.get(next_url)

if not args.pretty:
	print(json.dumps(messages, indent=2))
else:
	for msg in messages:
		print(f"""+----------\n| {msg["title"]}\n+----------""")
		print(re.sub(r"^", "| ", msg["message"], flags=re.M))
		if msg.get("extras"):
			print("+----------")
			for k, sub in msg["extras"].items():
				for subk, v in sub.items():
					print(f"| {k} {subk} = {v}")
		print()
