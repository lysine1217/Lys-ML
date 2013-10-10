import numpy as np

class KMeans:

    # lst should be reformed like [[1.0,2.0],[3.0,4.0]]
    def __init__(self, lst, k):
        self.lst = np.array(lst)
        self.n   = len(lst)
        self.dim = len(lst[0])
        self.k   = k
        self.kc  = []
        self.nd  = np.zeros(self.n)

        # set center of i cluster to random choosed point
        for i in xrange(self.k):
            self.kc.append(lst[np.random.randint(self.n)])

        self.kc = np.array(self.kc)
            
    def train(self, iterations):

        for ii in xrange(iterations):

            flag = 0

            # expectation phases
            for i in xrange(self.n):
                min_distance = 100000000
                for j in xrange(self.k):
                    ij_distance = np.linalg.norm(self.lst[i]-self.kc[j])
                    if ij_distance < min_distance:
                        min_distance = ij_distance
                        self.nd[i] = j
                        flag = 1

            if(flag==0):
                return ;

                        
            # maximization phases
            self.kcount = [0]*self.k
            self.ksum   = [[0.0]*self.dim]*self.k
        
            for i in xrange(self.n):
                self.kcount[self.nd[i]] += 1
                self.ksum[self.nd[i]] += self.lst[i]

            for i in xrange(self.k):
                self.kc[i] = self.ksum[i] / self.kcount[i]

        
            # calc error
            error = 0.0

            for i in xrange(self.n):
                error += np.linalg.norm(self.lst[i]-self.kc[self.nd[i]])

            print "error %.6lf" %error
        

            
        
        
                    

        
        
