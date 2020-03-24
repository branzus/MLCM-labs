





class KnownObject:

    def __init__(self, name, attributes, relevant, irrelevant=[]):
        self.name = name
        self.relevant = relevant
        self.irrelevant = irrelevant
        self.attributes = attributes



    def has_attribute(self, attrib):
        return attrib in self.attributes


    def __repr__(self):
        return "{0} : {1} because {2}. Also {3}.".format(self.name, self.attributes, self.relevant, self.irrelevant)

    
class UnknownObject:

    def __init__(self, attributes):
        self.attributes = attributes

    def __repr__(self):
        return 'Unknown object that {0}'.format(self.attributes)


class Learner:

    def __init__(self, name, attributes, knowledge_base):
        self.knowbase = knowledge_base
        self.attributes = attributes
        self.essential = attributes
        self.name = name
        self.infer(init=True)
        


    def infer(self, init=False):
        essential = []

        changed = False
        
        for att in self.essential:
            found = False
            for obj in self.knowbase:
                if obj.has_attribute(att):
                    found = True
                    changed = True
                    essential.extend(obj.relevant)

            if not found:
                if init:
                    print('Can\'t infer the properties of a {0} object.'.format(att))
                else:
                    essential.append(att)
                    
        self.essential = essential

        if changed:
            self.infer()


    def is_satisfied_by(self, obj):
        print('Determining if {0} is {1}.'.format(obj, self.name))
        for ess in self.essential:
            if ess not in obj.attributes:
                return False
        return True


    '''
    def get_base_attributes(self, attributes):
        changed = False
        characteristics = []
        for att in attributes:
            found = False
            for obj in self.knowbase:
                if obj.has_attribute(att):
                    changed = True
                    found = True
                    characteristics.extend(obj.relevant)
            if not found:
                characteristics.append(att)

        if changed:
            return self.get_base_attributes(characteristics)
        return characteristics
    '''
        
        
            

    def __repr__(self):
        return 'I was told an object is a {0} because {1}.\nI inferred it is a {0} because {2}.'.format(self.name, self.attributes, self.essential)
    

    




if __name__ == "__main__":

    brick = KnownObject('brick', ['is stable'], ['has flat bottom'], ['is heavy'])
    print(brick)
    glass = KnownObject('glass', ['enables drinking'],
                     ['carries liquids', 'is liftable'],
                     ['pretty'])
    print(glass)

    briefcase = KnownObject('briefcase', ['is liftable'], ['is light', 'has handle'])

    print(briefcase)

    bowl = KnownObject('bowl', ['carries liquids'], ['has concavity'])
    print(bowl)

    print('----------------------------------------------------------')
    cup_rule = Learner('cup', ['is stable', 'enables drinking'], [brick, glass, briefcase, bowl])
    print(cup_rule)
    print('----------------------------------------------------------')

    possible_cup = UnknownObject(['is light', 'made of porcelain', 'has decoration', 'has concavity', 'has handle', 'has flat bottom'])

    
    print(cup_rule.is_satisfied_by(possible_cup))
