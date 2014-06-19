/*
ASCII tree
How to make a C++ tree structure, so the source code defining the tree looks like an actual tree.

This is actual C++:

Node("1")
* Node("11")
* Node("12")
* * Node("121")
* * * Node("1211")
* Node("13")

Licence: WTFPLv2
*/

#include <list>
#include <string>
#include <iostream>

using std::list;
using std::string;
using std::cout;
using std::endl;

struct Node {
	Node(const string &value = string());
	Node &operator*();
	Node &operator*(const Node &other);
	
	string value;
	int level;
	list<Node> children;
};

Node::Node(const string &value) : value(value), level(0) {}

Node &Node::operator*() { ++level; return *this; }

Node &Node::operator*(const Node &other) {
	// only called on root
	Node *parent = this;
	for (int i = 0; i < other.level; ++i)
		parent = &parent->children.back();
	parent->children.push_back(other);

	return *this;
}

//////

struct Node2 {
	Node2(const string &value = 0);

	Node2 &operator/(const Node2 &other);

	string value;
	list<Node2> children;
};

Node2::Node2(const string &value) : value(value) {}

Node2 &Node2::operator/(const Node2 &other) {
	children.push_back(other);
	return *this;
}

//////

template <class NodeClass>
void print(const NodeClass &n, const string &prefix = string()) {
	string newprefix = prefix + "/" + n.value;
	cout << newprefix << endl;
	for (typename list<NodeClass>::const_iterator it = n.children.begin(); it != n.children.end(); ++it) {
		
		print(*it, newprefix);
	}
}

int main() {
	Node n =
	        Node("1")
	        * Node("11")
	        * Node("12")
	        * * Node("121")
	        * * * Node("1211")
	        * Node("13");

	Node2 n2 =
	        Node2("1")
	        / Node2("11")
	        / (Node2("12")
	           / (Node2("121")
	              / Node2("1211")))
	        / Node2("13");

	print(n);
	cout << "----" << endl;
	print(n2);
}
