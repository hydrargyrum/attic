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


def expand(obj, separator, no_lists=False):
	# should we expand {"0": 0, "1": 1} to itself or to [0, 1]?
	# we try to guess! unless told not to guess

	if no_lists:
		listable = []
	else:
		listable = sorted(build_list_candidates(obj, separator))

	def get_create(sub, path_el, default):
		if isinstance(sub, dict):
			return sub.setdefault(path_el, default)
		else:
			assert isinstance(sub, list)
			path_el = int(path_el)
			if len(sub) > path_el:
				return sub[path_el]
			assert path_el == len(sub)
			sub.append(default)
			return sub[path_el]

	ret = {}
	# prepare by building lists first
	for path in listable:
		sub = ret
		for path_el in path[:-1]:
			sub = get_create(sub, path_el, {})
		get_create(sub, path[-1], [])

	for k, value in obj.items():
		path = k.split(separator)
		sub = ret
		for path_el in path[:-1]:
			sub = get_create(sub, path_el, {})
		get_create(sub, path[-1], value)

	# if we don't care about building a list, we just need that:
	# for k, value in obj.items():
	# 	path = k.split(separator)
	# 	sub = ret
	# 	for path_el in path[:-1]:
	# 		sub = sub.setdefault(path_el, {})
	# 	sub[path[-1]] = value

	return ret


def build_list_candidates(obj, separator):
	# guess where are lists

	# first, convert all keys to tuples (so we can forget about the separator)
	all_keys = set(tuple(key.split(separator)) for key in obj)
	# {"foo/bar": 0} -> {("foo", "bar")}

	# add intermediate levels
	# {("foo", "bar")} -> {("foo",), ("foo", "bar")}
	for path in list(all_keys):
		for n in range(len(path)):
			all_keys.add(path[:n])
	all_keys.remove(())

	# Sorting by length is useful to do some kind of breadth-first browsing!
	# For example, we will have: foo, foo/bar, foo/baz, foo/bar/qux
	# instead of (with lexical sort): foo/bar, foo/bar/qux, foo/baz
	# With lexical sort, foo/bar/qux would prevent to find all foo subkeys (bar and baz)
	# By sorting by depth, we have foo/bar and foo/baz close to each other
	# and so it's breadth-first traversing.
	all_keys = sorted(all_keys, key=lambda k: (len(k), k))
	# The goal is that if we find a key that's not at the same level
	# or that has a different prefix, then we know that we have browsed all siblings.
	# When reaching foo/bar/baz, we're sure there won't be any other keys than bar and baz
	# directly under foo. So we can check if there's a list and it's complete.

	# compat dict: key = path, value = list of direct children of path (the key).
	# We only accept integers in those dict-value lists.
	# The values will be used later for hole-verification.
	# compat contains the candidates that may be lists after the input expand.
	compat = {}
	# incompat: set of paths that we know that cannot be lists after the input expand.
	# For example, if there's a non-numeric key under a path prefix
	# then this path prefix cannot be a list, only a dict.
	# It's a set because we don't need more info about this path:
	# it's incompatible and that's all.
	incompat = set()
	previous = ()  # parent of the previous iteration
	parent = None  # just make sure it's defined

	def has_hole(lis):
		for i in range(len(lis)):
			if lis[i] != i:
				return False
		return True

	def check_holes(parent):
		# We've visited all siblings of parent
		# and it was not incompatible.
		# Check there are no holes in the list.
		# If there's only [0, 2]
		# then the input JSON did not represent a list but a dict
		# else we would have had [0, 1], or [0, 1, 2]
		assert parent in compat
		assert parent not in incompat

		if not has_hole(compat[parent]):
			# There's a hole, this parent is not a list.
			compat.pop(parent, None)
			incompat.add(parent)

	for path in all_keys:
		parent = path[:-1]

		if parent == previous:  # we're traversing siblings of a parent
			if parent in incompat:
				# This parent is poisoned.
				# Nothing interesting here.
				continue
		else:  # this key is not a sibling of previous key's parent
			if previous in compat:
				check_holes(previous)
			previous = parent

		# Here, either we're "compatible" so far (under this parent)
		# or we're encountering a new parent and have seen any child yet
		# (so, we're compat so far too, because there were no incompatible
		# child yet)
		if path[-1].isdigit():
			compat.setdefault(parent, []).append(int(path[-1]))
		else:
			# This key prevents this parent from being a list.
			# We have to be a dict. Poison this parent.
			compat.pop(parent, None)
			incompat.add(parent)

	# End of the loop: we need to do the verification of the last parent we had.
	# We usually do it when we encounter a different parent
	# but the loop ended, so we do the last parent here.
	if parent in compat:
		check_holes(parent)

	# The values were used only for the sake of hole-verification.
	# Only the valid list paths are useful for caller.
	return list(compat)


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
	parser.add_argument('--expand', action='store_const', const=expand, dest='op')
	parser.add_argument('--no-lists', action='store_true')
	parser.add_argument('--separator', default='/')
	args = parser.parse_args()

	if args.op is flatten and args.no_lists:
		parser.error('--no-lists can only be used with --expand')

	obj = json.load(sys.stdin)
	op_cb = (args.op or flatten)
	if args.no_lists:
		obj = expand(obj, separator=args.separator, no_lists=True)
	else:
		obj = op_cb(obj, separator=args.separator)
	json.dump(obj, sys.stdout)


if __name__ == '__main__':
	main()
