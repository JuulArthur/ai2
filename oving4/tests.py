from main import Node, same_classification, plurality_value, entropy_func
import math

def test_same_classification_true():
	node1 = ['1']
	node2 = ['1']
	node3 = ['1']
	node4 = ['1']
	node5 = ['1']
	nodes = [node1,node2,node3,node4,node5]
	return same_classification(nodes)

def test_same_classification_false():
	node1 = ['1']
	node2 = ['1']
	node3 = ['2']
	node4 = ['1']
	node5 = ['2']
	nodes = [node1,node2,node3,node4,node5]
	return same_classification(nodes)

def test_plurality_value():
	node1 = ['1']
	node2 = ['1']
	node3 = ['2']
	node4 = ['1']
	node5 = ['2']
	nodes = [node1,node2,node3,node4,node5]
	return plurality_value(nodes)

def test_entropy():
	answer = math.floor(entropy_func(0.99)*100)/100
	return answer==0.08

def tests():
	print("test_same_classification true")
	print(test_same_classification_true())
	print("test_same_classification false")
	print(test_same_classification_false()==False)
	print("test_plurality_value")
	print(test_plurality_value()=='1')
	print("test entropy")
	print(test_entropy())

tests()