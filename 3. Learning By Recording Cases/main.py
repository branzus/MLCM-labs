import KNN
import kdtree





objects = [([1,2], 'Red'),
           ([2,1], 'Violet'),
           ([4,2], 'Blue'),
           ([6,1], 'Green'),
           ([2,5], 'Orange'),
           ([2,6], 'Red'),
           ([5,6], 'Yellow'),
           ([6,5], 'Purple')]

knn = KNN.KNN(k=1,
              weighted=False,
              distance=KNN.euclidean_distance,
              objects=objects)

kd = kdtree.KDtree(objects)


obj = [1,4]
print('Regular k-NN  classifies {0} as: {1}'.format(obj, knn.classify(obj)))
print('k-d tree      classifies {0} as: {1}'.format(obj, kd.classify(obj))) 


              
