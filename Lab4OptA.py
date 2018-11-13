"""
@author: William E Basquez
@Course: CS 2302
@Assignment: Lab 4, Option A
@Instructor: Diego Aguirre
@T.A: Manoj Saha
@Last modification: Nov 13, 2018
"""
import os
import time
import math
class Node:
    def __init__(self, line_input):
        self.word = line_input[0]
        self.new_vectors = line_input[1:]
        self.next = None

    def position(self, word):
        """
        This function tests 3 hash functions to see which one is faster
        """
        pos = ord(word[0]) - 97
        #pos = ord(word[0]) % 26
        #pos = len(word) % 26
        return pos

class hash_table:
    def __init__(self):
        self.size = 26
        self.buckets = [None] * 26

    def insert(self, info):
        new_node = Node(info)
        position = new_node.position(new_node.word)
        """
        If the bucket is empty, a new node is added
        """
        if self.buckets[position] is None:
            self.buckets[position] = new_node
        else:
            """
            Otherwise, we use a temp to traverse the end of the linked list at that bucket, then we add the new node
            """
            temp = self.buckets[position]
            while temp != None:
                if temp.next is None:
                    temp.next = new_node
                    return
                temp = temp.next

    def get_bucket(self, bucket):
        """
        This function returns an array of nodes instead of a linked. Same as list_to_arr
        the difference is that this one is used to calculate how many nodes are in a bucket
        """
        temp = self.buckets[bucket]
        arr_nodes = []
        while temp != None:
            arr_nodes.append(temp.word)
            temp = temp.next

        return arr_nodes

    def load_factor(self):
        total_elements = 0
        for i in range(self.size):
            total_elements += len(self.get_bucket(i))
        return math.ceil(total_elements / self.size)

    def biggest_bucket(self):
        """
        This function traverses the table and calculates which bucket has the most nodes
        This is useful to calculate the number of comparisons, at most, that the Table
        will need to perform
        """
        max_size = 0
        for i in range(self.size):
            if len(self.get_bucket(i)) > max_size:
                max_size = len(self.get_bucket(i))
        return max_size

def is_valid(word):
    """
    This function helps to make sure that the words have 'valid' characters
    In other words, makes sure that words are from the English language and
    not from another language.
    Searching, it was found that lowercase letters have an ordinal number from [97:122], therefore
    it checks these limits
    """
    counter = 0
    for i in range(len(word)):
        if ord(word[i]) > 96 and ord(word[i]) < 123:
            counter+=1
    """
    If the counter equals the length of the word, it is said that the word is valid (from the English language)
    Else, it's not utilized
    """
    if counter == len(word):
        return True
    else:
        return False

def reader():
    """
    This function reads a text file and stores the information in a list that will be used later to make nodes and insert into the Table
    """
    #filename = "glove.6B.50d.txt"
    #filename = "20000lines.txt"
    #filename = "40000lines.txt"
    #filename = "half_file.txt"
    filename = "new_list.txt"
    #filename = "temp.txt"
    #filename = "words.txt"
    file_input = []
    if os.path.exists(filename):
        lines = open(filename, encoding="utf-8",errors="ignore")

        for line in lines:
            word = line.strip('\n')
            new_word = word.split(' ')
            """
            The 'isalpha' function helps eliminate any word that begins with a symbol instead of a letter
            if the word in fact starts with a letter, it's appended to the list
            """
            if new_word[0].isalpha():
                file_input.append(new_word)

        if len(file_input) == 0:
            print("Existing file, but empty")
    else:
        print("File not found")

    return file_input

def list_to_arr(head):
	"""
	This function turns a linked-list into an array, but this function is used to sort a bucket
	The sorting of this list is implemented with a list, to do merge sort
	"""
	temp = head
	arr = []

	if head == None:
		return None

	while temp != None:
		arr.append(temp)
		temp = temp.next

	return arr

def differ_index(str1, str2):
    """
    This function takes in 2 strings and returns the index at which a the words are different (different letter)
    This is used when sorting the words in a bucket (to keep words in descending order) and searching for a word
    (if the ordinal number at this index is less / more than the one in the word we want to look for, it uses the first / second
    half of the list to make searching faster)
    """
    shorter_word = min(len(str1), len(str2))
    I1 = 0
    I2 = 0
    finalI = 0

    while finalI < shorter_word:
        if str1[I1] == str2[I2]:
            finalI+=1
        else:
            break
        I1+=1
        I2+=1
    return finalI

def merge(left_part, right_part, new_array):
	"""
	This function pulls together the las 2 halves of sorted sublists
	"""
	left_size = len(left_part)
	right_size = len(right_part)
	a,b,c = 0,0,0

	while a < left_size and b < right_size:
		if differ_index(left_part[a].word, right_part[b].word) == len(left_part[a].word):
			new_array[c] = left_part[a]
			a+=1
		elif differ_index(left_part[a].word, right_part[b].word) == len(right_part[b].word):
			new_array[c] = right_part[b]
			b+=1
		else:
			index = differ_index(left_part[a].word, right_part[b].word)
			if ord(left_part[a].word[index]) < ord(right_part[b].word[index]):
				new_array[c] = left_part[a]
				a+=1
			else:
				new_array[c] = right_part[b]
				b+=1
		c+=1

	while a < left_size:
		new_array[c] = left_part[a]
		a+=1
		c+=1

	while b < right_size:
		new_array[c] = right_part[b]
		b+=1
		c+=1

	return new_array

def merge_sort(array):
	"""
	Regular merge-sort function
	This function reduces a list by half until there's only 1 'element', and ther it calls
	'merge' to pull together sorted sublists
	"""
	if array == None:
		return None
	arr_size = len(array)
	if arr_size < 2:
		return array
	mid = arr_size // 2
	left = [None] * mid
	right = [None] * (arr_size - mid)

	for i in range(mid):
		left[i] = array[i]

	for j in range(mid, arr_size):
		right[j-mid] = array[j]

	left_sorted = merge_sort(left)
	right_sorted = merge_sort(right)
	final_array = merge(left_sorted, right_sorted, array)

	return final_array

def binarySearch (arr, lbound, rbound, word):
	"""
	This function searches for a word in a list of nodes.
	The reason this form of searching was used, it's because of it's speed
	Using recursion was a good appreach for this problem
	"""
	if rbound >= lbound:
		mid = lbound + (rbound - lbound)//2
		comp_index = differ_index(arr[mid].word, word)
		if arr[mid].word == word:
			return mid
		elif comp_index == len(arr[mid].word):
			return binarySearch(arr, mid+1, rbound, word)
		elif comp_index == len(word):
			return binarySearch(arr, lbound, mid-1, word)
		elif comp_index < len(arr[mid].word) and comp_index < len(word):
			if ord(arr[mid].word[comp_index]) < ord(word[comp_index]):
				return binarySearch(arr, mid+1, rbound, word)
			else:
				return binarySearch(arr, lbound, mid-1, word)
	else:
		return -1

def comparisons(arr):
	"""
	This function calculater the biggest number of comparisons that the function 'search' will compute, at most in a bucket
	it varies with each bucket
	"""
	return math.ceil(math.log2(len(arr)))

def main():
    words = reader()
    H = hash_table()
    for i in range(len(words)):
        if is_valid(words[i][0]) == True:
            H.insert(words[i])
    searchee_word = "federer" #any word
    bucket_num = ord(searchee_word[0]) - 97
    arr = list_to_arr(H.buckets[bucket_num])
    merge_sort(arr)
    if arr is None or len(arr) < 1:
        print("Empty bucket")
    else:
        print("In an array of size", len(arr), ",", searchee_word,"is at position:", binarySearch(arr, 0, len(arr), searchee_word))
        print("Table's load factor is:", H.load_factor(),"nodes")
        print("The biggest bucket has:", H.biggest_bucket(), "nodes, with at most", math.ceil(math.log2(H.biggest_bucket())),"comparisons")

main()
