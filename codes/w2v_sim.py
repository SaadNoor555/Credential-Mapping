from scipy import spatial
import gensim.downloader as api
import numpy as np


class W2VSimilarity:
    __instance = None
    @staticmethod
    def getInstance():
        if W2VSimilarity.__instance==None:
            W2VSimilarity()
        return W2VSimilarity.__instance
    
    def __init__(self) -> None:
        if W2VSimilarity.__instance != None:
            W2VSimilarity.__instance = self.getInstance()
        else:
            self.model = api.load("glove-wiki-gigaword-50") #choose from multiple models https://github.com/RaRe-Technologies/gensim-data
    
    def preprocess(self, sen):
        return [i.lower() for i in sen.split()]

    def get_vector(self, s):
        return np.sum(np.array([self.model[i] for i in self.preprocess(s)]), axis=0)

    def getSimilarity(self, s1: str, s2: str):
        return spatial.distance.cosine(self.get_vector(s1), self.get_vector(s2))

if __name__=='__main__':
    sen1 = 'email'
    sen2 = 'email'
    w2v = W2VSimilarity()
    print(w2v.getSimilarity(sen1, sen2))
