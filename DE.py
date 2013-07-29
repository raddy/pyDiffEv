import numpy as np
from floyd import unique_dexes

class DE(object):
     def __init__(self, objective=None, args=(),limits=None,npop=50, ngen=10, F=.5, C=.5):
        """

        """
        if F<0 or F>2:
            raise ValueError('Invalid mixing strength -- set F to float between 0 and 2')
        if C<0 or C>1:
            raise ValueError('Invalid crossover probability -- set C to float between 0 and 1')
        self.objective = wrap_function(objective,args)
        self.limits = np.asarray(limits)
        self.npop = npop
        self.ngen = ngen
        self.C = C
        self.F = F
        self.initial_pop = np.tile(limits[:,0],(npop,1))+np.tile(np.diff(limits).flatten(),(npop,1))*np.random.random((npop,self.limits.shape[0]))
        self.fitness_score = np.zeros(npop)
     
     def crossover(self,mutants):
        return np.where(np.random.random_sample(mutants.shape)<self.C,mutants,self.initial_pop)
     
     def mutate(self):
        diff_indices = lambda count: np.array( [unique_dexes(count,self.npop-1) for dex in xrange(self.npop)])
        fittest_individual = self.initial_pop[np.argmin(self.fitness_score)]
        parents = self.initial_pop[diff_indices(2)]
        return parents[:,0] + np.random.laplace(self.F,self.F/4,(self.npop,1))*(fittest_individual - parents[:,1])
     
     def wrap_function(function, args):
        if function is None:
            return  None
        def function_raper(*raper_args):
            return function(*(raper_args + args))
        return function_raper
        
     def __call__(self,chatty=False):
        for i in xrange(self.ngen):
            self.fitness_score = [self.objective(p) for p in self.initial_pop]
            nextgen = self.crossover(self.mutate())
            nextgen_fitness = [self.objective(p) for p in nextgen]
            better_original_gen = self.fitness_score < nextgen_fitness
            self.initial_pop = np.where(better_original_gen, self.initial_pop, nextgen)
            self.fitness_score = np.where(better_original_gen, self.fitness_score, nextgen_fitness)
            if chatty:
                print('  {:5d}/{:5d}  F = {:7.5f}'.format(i+1, self.ngen, self.fitness_score.min()))
        return DE_Result(self.initial_pop,self.fitness_score)
class DE_Result(object):
    def __init__(self,pop,scores):
        self._population = pop
        self._fitness = scores
    @property
    def population(self):
        return self._population
    @property
    def fittest(self):
        return self._population[np.argmin(self._fitness)]
    @property
    def minimum(self):
        return np.min(self._fitness)