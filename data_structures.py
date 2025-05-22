class HashMap:
    def __init__(self, size=10):
        self.size = size
        self.table = [[] for _ in range(size)]
    
    def _hash(self, key):
        return hash(key) % self.size
    
    def add(self, key, value):
        index = self._hash(key)
        for item in self.table[index]:
            if item[0] == key:
                item[1] = value
                return
        self.table[index].append([key, value])
    
    def get(self, key):
        index = self._hash(key)
        for item in self.table[index]:
            if item[0] == key:
                return item[1]
        return None

class LinkedQueue:
    def __init__(self):
        self.front = None
        self.rear = None
    
    def enqueue(self, data):
        new_node = {'data': data, 'next': None}
        if self.rear is None:
            self.front = self.rear = new_node
        else:
            self.rear['next'] = new_node
            self.rear = new_node
    
    def dequeue(self):
        if self.is_empty():
            return None
        temp = self.front
        self.front = temp['next']
        if self.front is None:
            self.rear = None
        return temp['data']
    
    def is_empty(self):
        return self.front is None

class MaxHeap:
    def __init__(self):
        self.heap = []
    
    def insert(self, transaction):
        self.heap.append(transaction)
        self._heapify_up(len(self.heap) - 1)
    
    def extract_max(self):
        if not self.heap:
            return None
        max_val = self.heap[0]
        self.heap[0] = self.heap[-1]
        self.heap.pop()
        self._heapify_down(0)
        return max_val
    
    def _heapify_up(self, index):
        parent = (index - 1) // 2
        if parent >= 0 and self.heap[index]['amount'] > self.heap[parent]['amount']:
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            self._heapify_up(parent)
    
    def _heapify_down(self, index):
        largest = index
        left = 2 * index + 1
        right = 2 * index + 2
        if left < len(self.heap) and self.heap[left]['amount'] > self.heap[largest]['amount']:
            largest = left
        if right < len(self.heap) and self.heap[right]['amount'] > self.heap[largest]['amount']:
            largest = right
        if largest != index:
            self.heap[index], self.heap[largest] = self.heap[largest], self.heap[index]
            self._heapify_down(largest)

class BalanceBST:
    def __init__(self):
        self.root = None
    
    def insert(self, account):
        self.root = self._insert(self.root, account)
    
    def _insert(self, node, account):
        if node is None:
            return {'account': account, 'left': None, 'right': None}
        if account.balance < node['account'].balance:
            node['left'] = self._insert(node['left'], account)
        else:
            node['right'] = self._insert(node['right'], account)
        return node
    
    def search_range(self, low, high):
        result = []
        self._search_range(self.root, low, high, result)
        return result
    
    def _search_range(self, node, low, high, result):
        if node is None:
            return
        if low <= node['account'].balance <= high:
            result.append(node['account'])
        if node['account'].balance >= low:
            self._search_range(node['left'], low, high, result)
        if node['account'].balance <= high:
            self._search_range(node['right'], low, high, result) 