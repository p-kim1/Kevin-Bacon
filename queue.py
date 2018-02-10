class Queue:
    def __init__(self):
        self.items=[]

    def isEmpty(self):
        return self.items==[]

    def enqueue(self,item):
        self.items.insert(0,item)
        
    def dequeue(self):
        return self.items.pop()

    def size(self):
        return len(self.items)

    def clone(self):
        items=self.items[:]
        self.copy=Queue()
        for item in items[::-1]:
            self.copy.enqueue(item)
        return self.copy
        
    def __eq__(self,other):
        return self.items==other.items

    def peek(self):
        return self.items[-1]

def queueInOrder(queue):
    qCopy=queue.clone()
    num=qCopy.dequeue()
    while not None:
        
        if num<qCopy.peek():
            print(num,qCopy.peek())
            num=qCopy.dequeue()
            if qCopy.isEmpty():
                return True
        else:
            return False
