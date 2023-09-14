# pip install -U sentence-transformers

from sentence_transformers import SentenceTransformer, util


def getSimilarity(sen1, sen2):
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

    #Compute embedding for both lists
    embedding_1= model.encode(sen1, convert_to_tensor=True)
    embedding_2 = model.encode(sen2, convert_to_tensor=True)

    return float(util.pytorch_cos_sim(embedding_1, embedding_2))

if __name__=='__main__':
    print(getSimilarity('Put Your Username Here', 'username'))