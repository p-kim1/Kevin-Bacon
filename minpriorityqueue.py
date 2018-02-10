class MinPriorityQueue:
    def __init__(self, items = [], priorities = []):
        """Given no parameters, creates an empty priority queue. Optionally, a list of items and a corresponding list of priority values can be provided which will be used to initialize the queue"""
        self.buildPriorityQueue(items, priorities)

    def isEmpty(self):
        """Returns True if the priority queue is empty. False otherwise."""
        return self.numItems == 0

    def getSize(self):
        """Returns the number of items in the queue."""
        return self.numItems

    def peek(self):
        """Returns (but does not remove) the minimum priority element."""
        return self.items[0]

    def dequeue(self):
        """Removes and returns the minimum priority element."""
        item = self.items[0]

        if len(self.priorities) > 1:
            self.priorities[0] = self.priorities.pop()
            self.items[0] = self.items.pop()
            
            self.percolateDown(0)
        else:
            self.priorities.pop()
            self.items.pop()
    
        self.numItems -= 1
        return item

    def percolateDown(self, idx):
        """Takes the item/priority pair at the given index and moves it to the appropriate place in the heap ordering."""
        node = idx
        minChild = self.getMinChild(node)
        done = False
        while minChild != None and not done:
            if self.priorities[node] > self.priorities[minChild]:
                tmpPriority = self.priorities[node]
                tmpItem = self.items[node]

                self.priorities[node] = self.priorities[minChild]
                self.items[node] = self.items[minChild]

                self.priorities[minChild] = tmpPriority
                self.items[minChild] = tmpItem

                node = minChild
                minChild = self.getMinChild(node)
            else:
                done = True

    def getMinChild(self, idx):
        """Returns the index of the child with the smallest priority value (or none if there are no children)."""
        leftChild = 2*idx + 1
        rightChild = 2*idx + 2
        
        if leftChild < len(self.priorities) and rightChild < len(self.priorities):
            if self.priorities[leftChild] < self.priorities[rightChild]:
                return leftChild
            else:
                return rightChild
        elif leftChild < len(self.priorities):
            return leftChild
        else:
            return None

    def enqueue(self, item, priority):
        """Adds a new item with the given priority value."""
        self.items.append(item)
        self.priorities.append(priority)

        self.percolateUp(len(self.priorities) - 1)       

        self.numItems += 1

    def percolateUp(self, idx):
        """Takes the item/priority pair at the given index and moves them to the appropriate place in the heap ordering."""
        node = idx
        parent = (idx - 1)//2
        done = False
        while parent >= 0 and not done:
            if self.priorities[parent] > self.priorities[node]:
                tmpPriority = self.priorities[parent]
                tmpItem = self.items[parent]
                
                self.priorities[parent] = self.priorities[node]
                self.items[parent] = self.items[node]
                
                self.priorities[node] = tmpPriority
                self.items[node] = tmpItem
                
                node = parent
                parent = (node - 1)//2
            else:
                done = True

    def buildPriorityQueue(self, items, priorities):
        """Discards the current contents of the queue and efficiently fills the queue using the given list of items and corresponding list of priority values."""
        self.items = items[:]
        self.priorities = priorities[:]
        self.numItems = len(items)

        for i in range(len(items)//2, -1, -1):
            self.percolateDown(i)

    def decreasePriority(self, item, originalPriority, lowerPriority):
        if lowerPriority < originalPriority:
            for i in range(len(self.items)):
                if self.items[i] == item and self.priorities[i] == originalPriority:
                    self.priorities[i] = lowerPriority
                    self.percolateUp(i)
                    return
