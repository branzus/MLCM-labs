import math


def euclidean_distance(a, b):
    assert(len(a) == len(b))

    s = 0
    for i in range(0,len(a)):
        s += (a[i] - b[i]) * (a[i] - b[i])

    return math.sqrt(s)


class KNN:

    def __init__(self, k=1, objects=[], weighted=False, distance=euclidean_distance):
        self.objects = objects.copy()
        self.k = k
        self.weighted = False
        self.distance = distance

    def add_sample(self, obj):
        self.objects.append(obj)



    def classify(self, obj):
        dists = []
        for point, label in self.objects:
            dists.append((self.distance(obj, point), label))

        dists = sorted(dists, key=lambda x : x[0])

        relevant = dists[:self.k]
        #print(relevant)

        if relevant[0][0] == 0:
            return dists[0][1]

        dct = dict()

        mval = 0
        mlabel = None
        
        for dist, label in relevant:
            try:
                dct[label] += 1/(dist * dist) if self.weighted else 1
            except KeyError:
                dct[label] = 1/(dist * dist) if self.weighted else 1
            if dct[label] > mval:
                mval = dct[label]
                mlabel = label

        return label

                

        
if __name__ == "__main__":


    knn = KNN(k=1,
                  weighted=False,
                  distance=euclidean_distance,
                  objects=[
                      ([1,2], 'Red'),
                      ([2,1], 'Violet'),
                      ([4,2], 'Blue'),
                      ([6,1], 'Green'),
                      ([2,5], 'Orange'),
                      ([2,6], 'Red'),
                      ([5,6], 'Yellow'),
                  ])
    knn.add_sample(([6,5], 'Purple'))


    print(knn.classify([5, 3]))


    
        
