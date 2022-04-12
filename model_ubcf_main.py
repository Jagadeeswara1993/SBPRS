
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd


class Recommendation:
    
    def __init__(self):
        self.final_df = pd.read_pickle(open('picklecopy/processed_data.pkl','rb'))
        self.user_final_rating = pd.read_pickle(open('picklecopy/user_final_rating.pkl','rb'))
        self.model = pd.read_pickle(open('picklecopy/Tuned_logreg_model.pkl','rb'))
        self.raw_data = pd.read_csv("data/sample30.csv")
        self.data_final = pd.concat([self.raw_data[['id','name','brand','categories','manufacturer']],self.final_df], axis=1)
        
        
    def getTopProducts(self, reviews_username):
        items = self.user_final_rating.loc[reviews_username].sort_values(ascending=False)[0:20].index
        features = pickle.load(open('picklecopy/tfidf_vocabulary.pkl','rb'))
        vectorizer = TfidfVectorizer(vocabulary = features)
        temp=self.data_final[self.data_final.name.isin(items)]
        X = vectorizer.fit_transform(temp['reviews'].values.astype('U'))
        temp=temp[['name']]
        temp['prediction'] = self.model.predict(X)
        temp['prediction'] = temp['prediction'].map({'Positive':1,'Negative':0})
        temp=temp.groupby('name').sum()
        temp['positive_percent']=temp.apply(lambda x: x['prediction']/sum(x), axis=1)
        final_list=temp.sort_values('positive_percent', ascending=False).iloc[:5,:].index
        return self.data_final[self.data_final.name.isin(final_list)][['id', 
                               'name']].drop_duplicates().to_html(index=False)


     