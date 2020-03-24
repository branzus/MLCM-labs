


class Link:

    def __init__(self, typ, mandatory=False, forbidden=False):
        self.type = typ
        assert(not(mandatory and forbidden))
        self.mandatory = mandatory
        self.forbidden = forbidden


    def __eq__(self, other):
        return self.type == other.type

    def __repr__(self):
        assert(not (self.mandatory and self.forbidden))
        if self.mandatory:
            return 'must ' + self.type
        if self.forbidden:
            return 'must-not ' + self.type
        return self.type

    def copy(self):
        return Link(self.type)

class Type:

    def  __init__(self, typ, ptype=None):
        self.type = typ
        self.parent = ptype

    def get_parent_types(self):
        if self.parent is None:
            return []

        lst = [self.parent]
        lst.extend(self.parent.get_parent_types())
        return lst

    def __eq__(self, other):
        if not isinstance(other, Type):
            return False
        return self.type == other.type
        
    
class Node:

    def __init__(self, name, typ, link_dict={}):
        self.link_dict = link_dict
        self.name = name
        self.type = typ

    def add_link(self, node, link):

        try:
            self.link_dict[node.name].append(link)
        except KeyError:
            self.link_dict[node.name] = [link]


    def __hash__(self):
        return self.name.__hash__()

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False        
        return self.name.__eq__(other.name)
    def __repr__(self):
        return "{0} ({1})".format(self.name, self.type.type)

class Sample:

    def __init__(self, nodes, link_dict):
        self.nodes = nodes
        self.link_dict = link_dict


    def __repr__(self):
        return str(self.link_dict)

    def require_link(self, n1, n2, link):
        index = self.link_dict[(n1, n2)].index(link)
        self.link_dict[(n1,n2)][index].mandatory = True

    def forbid_link(self, n1, n2, link):
        link.forbidden = True
        try:
            self.link_dict[(n1, n2)].append(link)
        except KeyError:
            self.link_dict[(n1, n2)] = [link]


        

class Learner:

    def __init__(self, initial_sample):
        self.sample = initial_sample

    def process_example(self, example, positive):
        if not positive:
            self.specialize(example)
        else:
            self.generalize(example)


    def generalize(self, example):

        for n in example.nodes:
            i = self.sample.nodes.index(n)
            sn = self.sample.nodes[i]
            if i >= 0 and n.type != sn.type:
                pn = n.type.get_parent_types() 
                psn = sn.type.get_parent_types()
                same_base = False
                for pt in pn:
                    if pt in psn:
                        # Climb-Tree
                        sn.type = pt
                        same_base = True
                        break
                if not same_base: # Drop-Link (no Enlarge-Set)
                    sn.type = None

        # Close Interval not needed in our arch example since we're not dealing with numbers.


    def specialize(self, example):
        sd = self.sample.link_dict
        to_require = {}
        to_forbid = {}
        for nodes in sd:
            if nodes not in example.link_dict:
                to_require[nodes] = sd[nodes].copy()
            else:
                for link in sd[nodes]:
                    if link.forbidden:
                        continue
                    if link not in example.link_dict[nodes]:
                        try:
                            to_require[nodes].append(link)
                        except KeyError:
                            to_require[nodes] = [link]


        for nodes in example.link_dict:
            if nodes not in sd:
                to_forbid[nodes] = example.link_dict[nodes].copy()
            else:
                for link in example.link_dict[nodes]:
                    if link not in sd[nodes]:
                        try:
                            to_forbid[nodes].append(link)
                        except KeyError:
                            to_forbid[nodes] = [link]

                            
        
        for nodes, links in to_require.items():
            for link in links:
                self.sample.require_link(*nodes, link)

        for nodes, links in to_forbid.items():
            for link in links:
                self.sample.forbid_link(*nodes, link)


                
    def __repr__(self):
        return str(self.sample)


if __name__ == "__main__":

    block = Type('block')
    brick = Type('brick', block)
    wedge = Type('wedge', block)
    
    n1 = Node('n1', brick)
    n2 = Node('n2', brick)
    n3 = Node('n3', brick)
    n3_w = Node('n3', wedge)
    
    sample = Sample([n1,n2,n3],
                    {(n1,n2) : [Link('left-of')],
                     (n1,n3) : [Link('support')],
                     (n2,n3) : [Link('support')]})

    print(sample)

    print('------------------------------------------------------')
    
    lrn = Learner(sample)
    lrn.process_example(Sample([n1,n2,n3],
                               {(n1,n2) : [Link('left-of')]}), False)

    
    print(lrn)


    print('------------------------------------------------------')
    
    lrn.process_example(Sample([n1,n2,n3],
                               {(n1,n2) : [Link('left-of'),
                                           Link('touch')],
                                (n1, n3) : [Link('support')],
                                (n2, n1) : [Link('touch')],
                                (n2, n3) : [Link('support')]}), False)

    
                                
    print(lrn)
    print('------------------------------------------------------')
    
    sample = Sample([n1,n2,n3_w],
                    {(n1,n2) : [Link('left-of')],
                     (n1,n3_w) : [Link('support')],
                     (n2,n3_w) : [Link('support')]})
    lrn.process_example(sample, True)
    print(lrn)
    
