from math import log
import random

class Node:
	'''
	The node is the class used to build up the tree. Each node in the tree has an attribute,
	which is the attribute checked at that node and children to each value that attribute
	can have. The children are either characters or nodes themselves
	'''
	def __init__(self, attribute):
		self.attribute = attribute
		self.children = {}

def input_file(fname):
	'''
	Method used to read file
	'''
	f = open('test.txt')
	content = f.readlines()
	f.close
	return content

def split_input(array):
	'''
	Method used to order the input from file to an array we can use
	'''
	examples = []
	for row in array:
		element = row.split('\t')
		examples.append(element)
	return examples

def remove_endings(array):
	'''
	All the last elements are "\n" and we need to remove that
	'''
	for i in range (0,len(array)-1):
		element = array[i].pop()
		array[i].append(element[0])
	return array

def plurality_value(examples):
	'''
	Finds the most common class in the examples given
	'''
	ones = 0
	twos = 0
	for example in examples:
		if example[-1] == '1':
			ones += 1
		else:
			twos += 1
	return '1' if ones > twos else '2'

def same_classification(examples):
	'''
	Checks if all the examples left has the same class
	'''
	attribute = examples[0][-1]
	for example in examples:
		if example[-1] != attribute:
			return False
	return True

def entropy_func(q):
	'''
	Calculate the entropy, used for finding the most important attribute to split on
	'''
	try:
		B = 0.0-(q*log(q,2)+(1-q)*log(1-q,2))
		return B
	except ValueError:
		return 0.0

def get_absolute_entropy(examples):
	'''
	Get th entropy to the whole set
	'''
	positives = 0.0
	for example in examples:
		if example[-1]=='1':
			positives+=1
	return entropy_func(positives/len(examples))

def importance(attributes, examples, use_random=False):
	'''
	This function finds the most important attributes, and return this attribute and its position
	'''
	if use_random:
		random_number = random.randrange(len(attributes))
		attribute = attributes.pop(random_number)
		return random_number, attribute
	else:
		absolute_entropy = get_absolute_entropy(examples)
		best_attribute = -1
		attribute_gain = 0
		for i in range(0,len(attributes)):
			#print("gain")
			gain = absolute_entropy - check_attribute(examples, attributes[i])
			if best_attribute == -1 or attribute_gain < gain:
				best_attribute = i
				attribute_gain = gain
	return best_attribute, attributes[best_attribute]

def check_attribute(examples, attribute):
	'''
	Returns the entropy of this attribute, used to check how important it is
	'''
	positives = 0.0
	negatives = 0.0
	entropy = 0.0

	for example in examples:
		if example[attribute] == '1' and example[-1] == '1':
			positives += 1
		elif example[attribute] == '1' and example[-1] == '2':
			negatives += 1

	if(positives+negatives>0):
		entropy = ((positives+negatives)/len(examples))*entropy_func(positives/(positives+negatives))

	positives = 0.0
	negatives = 0.0

	for example in examples:
		if example[attribute] == '2' and example[-1] == '1':
			positives += 1
		elif example[attribute] == '2' and example[-1] == '2':
			negatives += 1

	if(positives+negatives>0):
		entropy += ((positives+negatives)/len(examples))*entropy_func(positives/(positives+negatives))
	
	return entropy

def decisiontree_learning(examples, attributes, parent_examples, use_random=False):
	'''
	This is the function used by the training set to build the tree
	'''
	if len(examples) == 0:
		# We have no more examples and have to return the most common value from our parents
		return plurality_value(parent_examples)
	elif same_classification(examples):
		# If all examples has the same classification we can just return the classification of the first one
		return examples[0][-1]
	elif len(attributes) == 0:
		# If we have no more attributes to split the elements on we just have to return the most common value
		return plurality_value(examples)
	else:
		pos, attribute = importance(attributes, examples, use_random)
		sub_attributes = attributes[:pos] + attributes[pos+1:]
		node = Node(attribute)
		for value in ['1','2']:
			exs = []
			for example in examples:
				if example[attribute]==value:
					exs.append(example)
			subtree = decisiontree_learning(exs, sub_attributes, examples, use_random)
			node.children[value]=subtree
		return node

def create_treedict(root, level=0, result_dict={}):
	'''
	Create a dictionary from our nodes, used to print out the tree
	'''
	# Hack to check if anything is in the dictionary at this level
	# If it is we don't want to create a new one, but rather fill the one we have
	try:
		len(result_dict[level])
	except KeyError:
		result_dict[level] = []
	nodestring = "node: "
	nodestring += str(root.attribute)
	nodestring += " "
	result_dict[level].append(nodestring)

	for child in root.children.keys():
		valuestring = "Value: " + child + " "
		if isinstance(root.children[child], Node):
			result_dict[level].append(valuestring+"Node: " + str(root.children[child].attribute))
			create_treedict(root.children[child], level+1, result_dict)
		else:
			result_dict[level].append(valuestring+"Class: " + root.children[child])
	return result_dict

def print_tree(tree):
	'''
	Prints out the dictionary created at create_treedict
	'''
	i = 0
	while True:
		try:
			print(str(i)+str(tree[i]))
		except KeyError:
			break
		if i == 100:
			break
		i += 1

def dig_node(node, example):
	'''
	Used in test_tree to follow the nodes until we can check if this example correlates with
	the tree we have made
	'''
	child_node = node.children[example[node.attribute]]
	if (isinstance(child_node,Node)):
		return dig_node(child_node, example)
	return check_correct(child_node, example)

def check_correct(child_node, example):
	'''
	Simple method used to check if the example correlates with the value from the tree
	'''
	if child_node == example[-1]:
		return 1
	return 0

def test_tree(node, examples):
	'''
	Function used to test the tree
	'''
	correct = 0.0
	for example in examples:
		child_node = node.children[example[node.attribute]]
		if (isinstance(child_node,Node)):
			correct += dig_node(child_node, example)
		else:
			correct += check_correct(child_node, example)
	return correct/len(examples)



def main():
	content = input_file('training.txt')
	examples = split_input(content)
	examples = remove_endings(examples)

	attributes = [j for j in range(0,len(examples[0])-1)]

	rand_tree = decisiontree_learning(examples, attributes, examples, True)
	gain_tree = decisiontree_learning(examples, attributes, examples, False)
	
	content = input_file('test.txt')
	examples = split_input(content)
	examples = remove_endings(examples)

	print("printing tree without gain")
	tree = create_treedict(rand_tree)
	print_tree(tree)

	print("printing tree with gain")
	tree = create_treedict(gain_tree)
	print_tree(tree)

	print("Accuracy of tree without gain")
	print(test_tree(rand_tree, examples))

	print("Accuracy of tree with gain")
	print(test_tree(gain_tree, examples))
	


main()
