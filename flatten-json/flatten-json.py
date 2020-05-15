#!/usr/bin/env python3
# license: WTFPLv2 [http://www.wtfpl.net/]

import argparse
import json
import sys
import textwrap


def flatten(obj, separator):
	def recurse(obj, prefix=()):
		if isinstance(obj, dict):
			for k, v in obj.items():
				recurse(v, prefix + (k,))
		elif isinstance(obj, list):
			for n, v in enumerate(obj):
				recurse(v, prefix + (str(n),))
		else:
			ret[separator.join(prefix)] = obj

	ret = {}
	recurse(obj)
	return ret


class ImpossibleList(Exception):
	pass


def expand_nolists(obj, separator):
	ret = {}
	for k, value in obj.items():
		path = k.split(separator)
		sub = ret
		for path_el in path[:-1]:
			sub = sub.setdefault(path_el, {})
		sub[path[-1]] = value
	return ret


def expand_lists(obj, separator):
	# should we expand {"0": 0, "1": 1} to itself or to [0, 1]?
	# we try to guess!

	def generic_setdefault(sub, path_el, default):
		if isinstance(sub, dict):
			return sub.setdefault(path_el, default)
		else:
			assert isinstance(sub, list)

			if isinstance(path_el, str):
				if path_el.isdigit():
					path_el = int(path_el)
				else:
					raise ImpossibleList()

			if len(sub) > path_el:
				return sub[path_el]
			elif len(sub) + 1 > path_el:
				sub.append(default)
				return sub[path_el]
			else:
				raise ImpossibleList()

	def list_to_dict(lis):
		assert isinstance(lis, list)

		dct = {}
		for n, v in enumerate(lis):
			dct[n] = v
		return dct

	# We create each element as a list first
	# and as soon as we encounter that prevents us from being a list
	# e.g. a non-numeric or too-far key, then we transform it in a dict.

	# encapsulate root list so we can change root element type seamlessly
	# without making a special case
	ret = {'root': []}
	for k, value in obj.items():
		path = k.split(separator)

		parent = ret
		parent_key = 'root'
		sub = ret['root']

		for n, path_el in enumerate(path, 1):
			if n < len(path):
				# not the last component, those are containers
				# create a new list by default
				to_set = []
			else:
				# last path component, it's not a container but a value
				to_set = value

			if path_el.isdigit():
				path_el = int(path_el)

			new_parent = sub
			try:
				sub = generic_setdefault(sub, path_el, to_set)
			except ImpossibleList:
				sub = parent[parent_key] = list_to_dict(sub)
				sub = generic_setdefault(sub, path_el, to_set)
			parent = new_parent
			parent_key = path_el

	return ret['root']


def main():
	parser = argparse.ArgumentParser(
		description=textwrap.dedent('''

		Flatten a JSON tree or expand a simple JSON object.

		Flattening
		----------

		Flattening a JSON tree will return a single object with all keys at the
		same level. Deep paths are encoded in the keys.

		For example, this JSON:

			{
				"foo": {
					"bar": 42
					"elements": [1, 2]
				},
				"baz": true
			}

		will be flattened to:

			{
				"foo/bar": 42,
				"foo/elements/0": 1,
				"foo/elements/1": 2,
				"baz": true
			}

		Empty objects and empty lists will vanish as only terminal nodes
		are present in a flattened object.

		Expanding
		---------

		This is the reverse operation of flattening.

		Lists are ambiguous, for example the {"0": 123} JSON can either
		represent:
			- a list with a single element 123
			- a dict with a "0" key and a 123 value

		It will try hard to use lists whereever possible, unless --no-lists
		is given.

		Also, empty dicts and lists were removed during flattening.
		Thus, flattening-then-expanding cannot always restore the exact
		same object as original input.
		'''),
		formatter_class=argparse.RawDescriptionHelpFormatter,
	)
	parser.add_argument('--flatten', action='store_const', const=flatten, dest='op')
	parser.add_argument('--expand', action='store_const', const=expand_lists, dest='op')
	parser.add_argument('--no-lists', action='store_true')
	parser.add_argument('--separator', default='/')
	args = parser.parse_args()

	if args.no_lists:
		if args.op is flatten:
			parser.error('--no-lists can only be used with --expand')
		args.op = expand_nolists

	obj = json.load(sys.stdin)
	op_cb = (args.op or flatten)
	obj = op_cb(obj, separator=args.separator)
	json.dump(obj, sys.stdout)


if __name__ == '__main__':
	main()
