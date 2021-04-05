#!/usr/bin/env ruby
# 2012-08-04
# license: Do What The Fuck You Want To Public License version 2 [http://www.wtfpl.net/]

require 'json'
require 'yaml'

puts YAML::safe_load($<.read).to_json
