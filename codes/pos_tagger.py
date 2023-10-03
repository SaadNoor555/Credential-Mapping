from transformers import pipeline

class POSTagger:
    __instance = None
    @staticmethod 
    def getInstance():
        """ Static access method. """
        if POSTagger.__instance == None:
            POSTagger()
        return POSTagger.__instance
    
    def __init__(self):
        """ Virtually private constructor. """
        if POSTagger.__instance != None:
            POSTagger.__instance = self.getInstance()
        else:
            self.pipe = self.pipe = pipeline("token-classification", model="TweebankNLP/bertweet-tb2_ewt-pos-tagging")
            POSTagger.__instance = self

    
    def getNouns(self, sen) -> str:
        res = self.pipe(sen)
        nouns = ' '.join([x['word'] for x in res if x['entity']=='NOUN'])
        return nouns
    

if __name__=='__main__':
    pot = POSTagger()
    sen = 'please enter your email'
    print(pot.getNouns(sen))