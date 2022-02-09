#!/usr/bin/env ruby
# 2012-08-04
# SPDX-License-Identifier: WTFPL

require 'json'
require 'yaml'

puts YAML::safe_load($<.read).to_json
