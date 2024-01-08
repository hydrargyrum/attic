#!/usr/bin/env python3
# SPDX-License-Identifier: WTFPL

import json
import sys


class Merger:
    def recurse(self, schema):
        if schema['type'] == 'array':
            if schema['_all_items']:
                for el in schema['_all_items']:
                    self.recurse(el)
                self.merge(schema['_all_items'])
                schema['items'] = schema['_all_items'][0]
                del schema['_all_items']
        elif schema['type'] == 'object':
            for v in schema['properties'].values():
                self.recurse(v)

    def merge(self, schemas):
        # assert len(set(s['type'] for s in schemas) - {'null'}) <= 1
        dest = schemas[0]
        for el in schemas[1:]:
            self.merge_one(dest, el)

    def merge_one(self, dest, other):
        if dest['type'] == 'null':
            # if other['type'] == 'null':
            #     return
            dest.update(other)
            return
        elif other['type'] == 'null':
            return
        assert dest['type'] == other['type']
        func = getattr(self, f"do_merge_{dest['type']}", None)
        if func is not None:
            func(dest, other)

    def do_merge_object(self, dest, other):
        for ok in other['properties']:
            if ok in dest['properties']:
                self.merge_one(other['properties'][ok], dest['properties'][ok])
            else:
                dest['properties'][ok] = other['properties'][ok]

    def do_merge_array(self, dest, other):
        self.merge([dest['items'], other['items']])


class Builder:
    def typing(self, data):
        if data is None:
            return {'type': 'null'}
        elif isinstance(data, bool):
            return {'type': 'bool'}
        elif isinstance(data, int):
            return {'type': 'number'}
        elif isinstance(data, str):
            return {'type': 'string'}
        elif isinstance(data, list):
            ret = {'type': 'array'}
            types = [self.typing(item) for item in data]
            ret['items'] = {}
            ret['_all_items'] = types
            return ret
        elif isinstance(data, dict):
            ret = {'type': 'object', 'properties': {}}
            for k, v in data.items():
                ret['properties'][k] = self.typing(v)
            return ret
        else:
            raise AssertionError()

    def create(self, data):
        ret = {"$schema": "http://json-schema.org/schema#"}
        ret.update(self.typing(data))
        return ret


data = json.load(sys.stdin)
schema = Builder().create(data)
Merger().recurse(schema)
print(json.dumps(schema, indent=4))
