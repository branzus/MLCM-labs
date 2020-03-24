


class Node:


    def __init__(self, axis, value, left, right):
        self.axis = axis
        self.value = value
        self.left = left
        self.right = right


    def next(self, v):
        return self.right if v[self.axis] > self.value else self.left


    def classify(self, obj):
        nxt = self.next(obj)
        if isinstance(nxt, Node):
            return nxt.classify(obj)
        
        return nxt




class KDtree:

    def __init__(self, objects):
        self.root = self._add(objects)
        

    def _add(self, objects, depth=0):
        if len(objects) == 1:
            return objects[0][1]
        
        k = len(objects[0][0])

        axis = depth % k
        srt = sorted(objects, key=lambda x : x[0][axis])

        midh = len(srt) // 2
        midl = midh - 1
        return Node(axis,
                    (srt[midh][0][axis] + srt[midl][0][axis]) / 2,
                    left = self._add(srt[:midh], depth + 1),
                    right = self._add(srt[midh:], depth + 1))
    
    
        
    def classify(self, obj):
        return self.root.classify(obj)
    




if __name__ == "__main__":

    tree = KDtree([([1,2], 'Red'),
                   ([2,1], 'Violet'),
                   ([4,2], 'Blue'),
                   ([6,1], 'Green'),
                   ([2,5], 'Orange'),
                   ([2,6], 'Red'),
                   ([5,6], 'Yellow'),
                   ([6,5], 'Purple')
    ])

    print(tree.classify([5,3]))


    
