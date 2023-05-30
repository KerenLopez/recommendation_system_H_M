import pandas as pd

pathArticles = 'articles.csv'
pathClusters = 'kmodesClusters.csv'
pathMerged = 'merged.csv'

df_articles = pd.read_csv(pathArticles)
df_clusters = pd.read_csv(pathClusters)
df_clientsAndPurchases = pd.read_csv(pathMerged)


df_articles = df_articles.drop("Unnamed: 0", axis=1)
df_clusters = df_clusters.drop("Unnamed: 0", axis=1)
df_clientsAndPurchases = df_clientsAndPurchases.drop("Unnamed: 0", axis=1)

class doRecommendations():
    def recommendation(self, clientID):
        df_client = df_clientsAndPurchases[df_clientsAndPurchases['customer_id']==clientID]
        clusters = []
        df_recomended = pd.DataFrame()   
        articles = pd.DataFrame()   
        for i in df_articles.columns:
            df_recomended[i] = [] 
        for i in df_clusters.columns:
            articles[i] = [] 
        for index, transaction in df_client.iterrows():
            ar_id=transaction[1]
            row=df_clusters[df_clusters["article_id"]==ar_id]
            cluster=row["Cluster No"].values[0]
            clusters.append(cluster)
        unique_clusters = list(set(clusters))
        for cluster in unique_clusters:
            row = df_clusters[df_clusters["Cluster No"] == cluster].sample(6)
            articles=articles.append(row)
        for index, article in articles.iterrows():
            df_recomended = df_recomended.append(df_articles[df_articles['article_id']==article[0]], ignore_index=True)
        return df_recomended,df_client 
    def purchasedArticles(self, df):
        df_purchased = pd.DataFrame()
        for i in df_articles.columns:
            df_purchased[i] = [] 
        for index, article in df.iterrows():
            df_purchased = df_purchased.append(df_articles[df_articles['article_id']==article[1]], ignore_index=True)
        return df_purchased 

