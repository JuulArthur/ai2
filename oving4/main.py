from math import log
import random

class Node:
	def __init__(self, attribute):
		self.attribute = attribute
		self.children = {}

def input_file(fname):
	f = open('test.txt')
	content = f.readlines()
	f.close
	return content

def split_input(array):
	examples = []
	for row in array:
		element = row.split('\t')
		examples.append(element)
	return examples

def remove_endings(array):
	for i in range (0,len(array)-1):
		element = array[i].pop()
		array[i].append(element[0])
	return array

def plurality_value(examples):
	ones = 0
	twos = 0
	for example in examples:
		if example[-1] == '1':
			ones += 1
		else:
			twos += 1
	return '1' if ones > twos else '2'

def same_classification(examples):
	attribute = examples[0][-1]
	for example in examples:
		if example[-1] != attribute:
			return False
	return True

def entropy(q):
	B = -(q*log(q,2)+(1-q)*log(1-q,2))
	return B

def get_absolute_entropy(examples):
	positives = 0
	for example in examples:
		if example[-1]=='-1':
			positives+=1
	return entropy(positives/len(examples))

def importance(attributes, examples, use_random=False):
	if use_random:
		attribute = attributes.pop(random.randrange(len(attributes)))
		return attribute
	absolute_entropy = get_absolute_entropy(examples)
	best_attribute = -1
	attribute_gain = 0
	else:
		for attribute in attributes:
			gain = absolute_entropy - check_attribute(attribute)
			if best_attribute == -1 or attribute_gain < gain:
				best_attribute = attribute
				attribute_gain = gain
	return attributes.pop(best_attribute)

def check_attribute(examples, attribute):
	positives = 0
	negatives = 0

	for example in examples:
		if example[attribute] == '1' and example[-1] == '1':
			positives += 1
		elif example[attribute] == '1' and example[-1] == '2':
			negatives += 1

	entropy = ((positives+negatives)/examples)*entropy(positives/(positives+negatives))

	positives = 0
	negatives = 0

	for example in examples:
		if example[attribute] == '2' and example[-1] == '1':
			positives += 1
		elif example[attribute] == '2' and example[-1] == '2':
		negatives += 1

	entropy += ((positives+negatives)/examples)*entropy(positives/(positives+negatives))
	return entropy

def decisiontree_learning(examples, attributes, parent_examples):
	if len(examples) == 0:
		return plurality_value(parent_examples)
	elif same_classification(examples):
		# If all examples has the same classification we can just return the classification of the first one
		return examples[0].attribute
	elif len(attributes) == 0:
		return plurality_value(examples)
	else:
		attribute = importance(attributes, examples)
		attributes.remove(attribute)
		node = Node(attribute)
		for value in ['1','2']:
			exs = []
			for example in examples:
				if example[attribute]==value:
					exs.append(example)
			subtree = decisiontree_learning(exs, attributes, examples)
			node.children.append(subtree)
		return tree
		
def main():
	content = input_file('test.txt')
	print content
	examples = split_input(content)
	examples = remove_endings(examples)
	print examples
