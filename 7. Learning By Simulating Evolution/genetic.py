import random,time

INT_MAX = pow(2,32) - 1

def timing(f):
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print('{:s} function took {:.3f} ms'.format(f.__name__, (time2-time1)*1000.0))

        return ret
    return wrap


def get_best_sol_value(solutions, g, v, G):

    bw = INT_MAX
    bv = 0
    bsol = None
    for sol in solutions:
        sw, sv = get_weight_val(sol,g,v)
        if sv > bv:
            if sw <= G or sw < bw or bsol is None:
                bw = sw
                bv = sv
                bsol = sol

        elif bw > G and sw <= G or bsol is None:
            bw = sw
            bv = sv
            bsol = sol

    return bsol, bw, bv


def get_weight_val(solution, g, v):

    weight = 0
    value = 0
    
    for i, s in enumerate(solution):
        if s == 1:
            weight += g[i]
            value += v[i]

    return weight, value

def get_sol_score(weight, value, G):
    if G >= weight:
        score = value
    else:
        score = -(weight / value)

    return score



@timing
def genetic_algorithm(G, N, g, v, pop_size, num_iter, cross_r=0.85, mut_r=0.1, clone_r=0.5):

    population = initial_population(G, g, v, pop_size)
    it = 0
    fitness, best_fit = get_fitness(population, G, g, v)
    gx = [0]
    gy = [best_fit]
    while it < num_iter:
        it += 1
        population = new_population(population, fitness, pop_size, cross_r, mut_r, clone_r)
        fitness, best_fit = get_fitness(population, G, g, v)
        gx.append(it)
        gy.append(best_fit)



    sol, w, v = get_best_sol_value(population, g, v, G)
    return v, [i for i, x in enumerate(sol) if x == 1], w <= G
    

def initial_population(G, g, v, pop_size):
    l = len(g)
    population = [[random.randint(0,1) for i in range(l)] for j in range(pop_size)]
    return population
    
    
def get_fitness(population, G, g, v):
    fitness = []
    best_fit = - INT_MAX
    for indiv in population:
        weight, value = get_weight_val(indiv, g, v)
        
        fit = get_sol_score(weight, value, G)
        if fit > best_fit:
            best_fit = fit

        fitness.append(fit)

    return fitness,best_fit
                
def new_population(population, fitness, pop_size, cross_r, mut_r, clone_r):

    top = sorted(zip(fitness, population), key=lambda x : x[0], reverse=True)[:len(population)//4]
    
    new_pop = []
    cl = 1
    new_pop.append(top[0][1])
    for i in range(pop_size-1):
        R = random.random()
        if R < cross_r:
            new_pop.append(crossover(random.choice(top)[1], random.choice(top)[1]))
        elif R < cross_r + mut_r:
            new_pop.append(mutate(random.choice(top)[1]))
        else:
            new_pop.append(top[cl % len(top)][1].copy())
            cl += 1

    return new_pop
            

def crossover(sol1, sol2):
    index = random.randint(0, len(sol1) - 2)

    child = []
    child.extend(sol1[:index])
    child.extend(sol2[index:])
    return child

def mutate(sol):
    index = random.randint(0, len(sol)-1)
    s = sol.copy()
    s[index] = 1 if s[index] == 0 else 0

    return s
    

def solve(G, N, g, v, pop_size, num_iter, cross_r=0.85, mut_r=0.1, clone_r=0.5):
    return genetic_algorithm(G, N, g, v, pop_size, num_iter, cross_r, mut_r, clone_r)

