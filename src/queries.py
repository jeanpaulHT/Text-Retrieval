from index import Index, calc_tf_idf
from preprocessor import Preprocessor
from collections import Counter
# import numpy as np
import heapq

# def cos_similarity(a, b):
#     return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


class QueryEngine:
    def __init__(self, preprocessor: Preprocessor, index: Index):
        self.preprocessor: Preprocessor = preprocessor
        self.index: Index= index

    # def search(self, query):
    #     q_parse = self.preprocessor._parse_line(
    #         query, Preprocessor.skipped_symbols)
    #     q_process = self.preprocessor._preprocess_text(q_parse).split(' ')

    #     q_freq = Counter(q_process)
    #     t_data = filter(
    #         lambda x: x[0] is not None, 
    #         (self.index.full_entry(t) for t in q_process)
    #     )
    #     def post_struct(w, idf, p_list): 
    #         return (w, idf, { 
    #             id: calc_tf_idf(tf, idf) for id, tf in p_list
    #         }) 
        
    #     posts = [post_struct(word, idf, p_list) for word, idf, p_list in t_data]

    #     tweets = { id for _, _, p_dict in posts for id in p_dict }
    #     data = {}
    #     idfs = {}
        
    #     for word, idf, post_dict in posts:
    #         idfs[word] = idf
    #         data[word] = [post_dict.get(doc, 0) for doc in tweets]
            
    #     df = pd.DataFrame.from_dict(data, orient='index', columns=list(tweets))
    #     q_vec = pd.DataFrame(
    #         calc_tf_idf(q_freq[word], idfs[word]) for word in df.index
    #     )
    #     q_vec_np = q_vec.to_numpy()

    #     score = {
    #         tweet: cos_similarity(df[tweet].to_numpy(), q_vec_np) 
    #             for tweet in tweets
    #     }
    
    #     result = heapq.nlargest(self.depth, score, key=score.get)
    #     return result

    @staticmethod
    def split_query(query, preprocessor):
        q_parse = preprocessor._parse_line(query, preprocessor.skipped_symbols)
        q_process = preprocessor._preprocess_text(q_parse).split(' ')
        return q_process

        
    def search(self, queryText, k):
        query = self.split_query(queryText, self.preprocessor)
        tf_terms_q = Counter(query)
        score = {}

        for term in query:
            _, idf, posting_list = self.index.full_entry(term)
            tf_tq = tf_terms_q[term]
            w_tq = calc_tf_idf(tf_tq, idf)

            for document, tf_td in posting_list:
                w_td = calc_tf_idf(tf_td, idf)
                score.setdefault(document, 0)
                score[document] += w_td * w_tq
        
        for document in score.keys():
            score[document] = score[document] / self.index.get_norm(document)
        
        return heapq.nlargest(k, score.keys(), key=lambda x: score[x])
        


