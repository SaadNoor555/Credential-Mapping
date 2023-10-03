# pip install -U sentence-transformers

from sentence_transformers import SentenceTransformer, util
import json
from transformers import pipeline

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')


pipe = pipeline("token-classification", model="TweebankNLP/bertweet-tb2_ewt-pos-tagging")

def get_POS(sen):
    res = pipe(sen)
    nouns = ' '.join([x['word'] for x in res if x['entity']=='NOUN'])
    return nouns
def getSimilarity(sen1, sen2):
    

    #Compute embedding for both lists
    embedding_1= model.encode(sen1, convert_to_tensor=True)
    embedding_2 = model.encode(sen2, convert_to_tensor=True)

    return float(util.pytorch_cos_sim(embedding_1, embedding_2))

if __name__=='__main__':
    f1 = open('inputfields1.json')
    f2 = open('loginConfig.json')
    inputFields = json.load(f1)
    inputFields = inputFields['inputs']
    loginConfig = json.load(f2)
    for x in inputFields:
        sim = 0
        value = ''
        for key in loginConfig.keys():
            sen = x['nearest label']
            print(sen)
            sen = get_POS(sen)
            tmp = getSimilarity(sen, key)
            print("{}, {}, {}".format(sen, key, str(tmp)))
            if tmp>sim:
                sim=tmp
                value = loginConfig[key]
        x['value'] = value
        x['similarity'] = sim