JSON2SQLite is a tool to insert JSON data in a SQLite database, by mapping dictionary keys or list indices to SQL table columns. It can also update rows.

Let's create a sample database:

	% sqlite3 sample.sqlite "CREATE TABLE elements (id INTEGER PRIMARY KEY, name TEXT, protons INT, neutrons INT)"

And insert a dict as a row:

	% json2sqlite -d sample.sqlite -t elements -j '{"id": 1, "name": "hydrogen", "protons": 1, "neutrons": 0}'
	% sqlite3 sample.sqlite "SELECT * FROM elements"
	id          name        protons     neutrons  
	----------  ----------  ----------  ----------
	1           hydrogen    1           0         

Lists/tuples are also supported as rows, but the order has to match the column order.

	% json2sqlite -d sample.sqlite -t elements -j '[2, "helium", 2, 2]'
	% sqlite3 sample.sqlite "SELECT * FROM elements"
	id          name        protons     neutrons  
	----------  ----------  ----------  ----------
	1           hydrogen    1           0         
	2           helium      2           2         

A list containing dicts will insert each dict as a row:

	% json2sqlite -d sample.sqlite -t elements -j '[{"id": 3, "name": "deuterium", "protons": 1, "neutrons": 1}, {"id": 4, "name": "tritium", "protons": 1, "neutrons": 2}]'
	% sqlite3 sample.sqlite "SELECT * FROM elements"
	id          name        protons     neutrons  
	----------  ----------  ----------  ----------
	1           hydrogen    1           0         
	2           helium      2           2         
	3           deuterium   1           1         
	4           tritium     1           2         

Or a dict containing lists:

    % json2sqlite -d sample.sqlite -t elements -j '{"id": [3, 4], "name": ["deuterium", "tritium"], "protons": [1, 1], "neutrons": [1, 2]}'

And list of list/tuples will also work:

	% json2sqlite -d sample.sqlite -t elements -j '[[5, "lithium", 3, 3], [6, "lithium", 3, 4]]'
	% sqlite3 sample.sqlite "SELECT * FROM elements"
	id          name        protons     neutrons  
	----------  ----------  ----------  ----------
	1           hydrogen    1           0         
	2           helium      2           2         
	3           deuterium   1           1         
	4           tritium     1           2         
	5           lithium     3           3         
	6           lithium     3           4         

Using dicts, not all keys/columns are required. Missing columns will have the default SQL value.

	% json2sqlite -d sample.sqlite -t elements -j '{"id": 7, "name": "nitrogen", "protons": 7}'
	% sqlite3 sample.sqlite "SELECT * FROM elements"
	id          name        protons     neutrons  
	----------  ----------  ----------  ----------
	1           hydrogen    1           0         
	2           helium      2           2         
	3           deuterium   1           1         
	4           tritium     1           2         
	5           lithium     3           3         
	6           lithium     3           4         
	7           nitrogen    7                     

It's possible to update rows with certain columns matching. The match should be on column 'id' (with -u), and the value for the match is 7. All other dict keys will be written ('neutrons' in this case). The columns that are not refered to by the dict ('name' and 'protons') will be ignored.

	% json2sqlite -d sample.sqlite -t elements -j '{"id": 7, "neutrons": 7}' -u id
	% sqlite3 sample.sqlite "SELECT * FROM elements"
	id          name        protons     neutrons  
	----------  ----------  ----------  ----------
	1           hydrogen    1           0         
	2           helium      2           2         
	3           deuterium   1           1         
	4           tritium     1           2         
	5           lithium     3           3         
	6           lithium     3           4         
	7           nitrogen    7           7         

It's possible to match on multiple columns by using several '-u'. Here we'll update rows having 'protons = 3 and neutrons = 3' by setting their name to 'lithium-6' (and will ignore the id column):

	% json2sqlite -d sample.sqlite -t elements -j '{"protons": 3, "neutrons": 3, "name": "lithium-6"}' -u protons -u neutrons
	% sqlite3 sample.sqlite "SELECT * FROM elements"
	id          name        protons     neutrons  
	----------  ----------  ----------  ----------
	1           hydrogen    1           0         
	2           helium      2           2         
	3           deuterium   1           1         
	4           tritium     1           2         
	5           lithium-6   3           3         
	6           lithium     3           4         
	7           nitrogen    7           7         
