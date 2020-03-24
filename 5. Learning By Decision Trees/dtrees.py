import math


class Node:

    def __init__(self, axis, res_dict):
        self.axis = axis
        self.res_dict = res_dict


    def next(self, obj):
        return self.res_dict[obj[self.axis]]

    def classify(self, obj):
        nxt = self.next(obj)
        if isinstance(nxt, Node):
            return nxt.classify(obj)
        
        return nxt


    def __repr__(self):
        return "({0} - {1})".format(self.axis, self.res_dict)
            


class DTree:
    
    def __init__(self, data):
        self.root = self._add(data, [])

    def __repr__(self):
        return str(self.root)

    def _add(self, data, chosen):

        flag = True
        for i in range(len(data)-1):
            if data[i][1] != data[i+1][1]:
                flag = False
                break

        if flag:
            return data[0][1]

        k = len(data[0][0])
        if k == len(chosen):
            return None
        
        avg_disorders = []
        for i in range(k):
            if i in chosen:
                continue
            dct = self.test_split(i, data)
            #print(i, self.get_average_disorder(dct, len(data)))
            avg_disorders.append((self.get_average_disorder(dct, len(data)), dct, i))

        

        best = sorted(avg_disorders, key=lambda x:x[0])[0]
        chosen.append(best[2])
        res_dict = dict()
        for key in best[1]:
            res_dict[key] = self._add(best[1][key], chosen.copy())

        return Node(best[2], res_dict)
    

    def test_split(self, index, data):
        res_dict = dict()
        sample_dist = dict()
        for sample in data:
            try:
                res_dict[sample[0][index]].append(sample)
            except KeyError:
                res_dict[sample[0][index]] = [sample]
                
        return res_dict

    def get_average_disorder(self, dct, total):

        avg_sum = 0
        
        for char in dct:
            pi = len(dct[char])/total
            disorder = 0
            classes = dict()
            for elem in dct[char]:
                try:
                    classes[elem[1]] += 1
                except KeyError:
                    classes[elem[1]] = 1
            for c in classes:
                x = classes[c]/len(dct[char])
                disorder += -x * math.log2(x)

            avg_sum += pi * disorder
        return avg_sum





if __name__ == "__main__":

    
    data=[(['blonde', 'average', 'light', 'no'], True),
          (['blonde', 'tall', 'average', 'yes'], False),
          (['brown', 'short', 'average', 'yes'], False),
          (['blonde', 'short', 'average', 'no'], True),
          (['red', 'average', 'heavy', 'no'], True),
          (['brown', 'tall', 'heavy', 'no'], False),
          (['brown', 'average', 'heavy', 'no'], False),
          (['blonde', 'short', 'light', 'yes'], False)]

    
          
    dt = DTree(data)
    print(dt)

    data = [(['overcast', 'hot', 'high', 'not'], False),
            (['overcast', 'hot', 'high', 'very'], False),
            (['overcast', 'hot', 'high', 'medium'], False),            
            (['sunny', 'hot', 'high', 'not'], True),
            (['sunny', 'hot', 'high', 'medium'], True),
            (['rain', 'mild', 'high', 'not'], False),
            (['rain', 'mild', 'high', 'medium'], False),
            #(['rain', 'hot', 'normal', 'not'], True),
            (['rain', 'cool', 'normal', 'medium'], False),
            (['rain', 'cool', 'normal', 'very'], False),
            (['sunny', 'cool', 'normal', 'very'], True),            
            (['sunny', 'cool', 'normal', 'medium'], True),            
            (['overcast', 'mild', 'high', 'not'], False),
            (['overcast', 'mild', 'high', 'medium'], False),
            (['overcast', 'cool', 'normal', 'not'], True),
            (['overcast', 'cool', 'normal', 'medium'], True),
            (['rain', 'mild', 'normal', 'not'], False),
            (['rain', 'mild', 'normal', 'medium'], False),
            (['overcast', 'mild', 'normal', 'medium'], True),
            (['overcast', 'mild', 'normal', 'very'], True),            
            (['sunny', 'mild', 'high', 'very'], True),            
            (['sunny', 'mild', 'high', 'medium'], True),            
            (['sunny', 'hot', 'normal', 'not'], True),            
            (['rain', 'mild', 'high', 'very'], False)]

    print(DTree(data))
