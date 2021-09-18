from django.shortcuts import render,HttpResponse
import pandas as pd 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Create your views here.
def index(requests):
    df =pd.read_csv('static/final_movie_data.csv')
    if requests.method =="POST":
        flag=True
        movie =requests.POST.get('search')
        reclist=[]
        try:
            reclist =recommend(movie)
        except:
            reclist =["Sorry we can't find your movie in our database."]
            flag=False
        
        context={'flag':flag,'post':True,'reclist':reclist,'movie':movie,'mlist':list(df['title'])}
        return render(requests,'main/index.html',context=context)
    else:
        context ={'flag':False,'post':False,'movie':"",'mlist':list(df['title'])}
        return render(requests,'main/index.html',context=context)





def recommend(movie):
    df_comb =pd.read_csv('static/final_movie_data.csv')
    cv=CountVectorizer()
    count_matrix = cv.fit_transform(df_comb['comb'])
    similarity =cosine_similarity(count_matrix)
    i=df_comb.loc[df_comb['title']==movie].index[0]
    List =list(enumerate(similarity[i]))
    List_sorted =sorted(List,reverse=True,key=lambda x:x[1])
    Final_list=List_sorted[:16]    
    recommend_list =[]
    for i in range(len(Final_list)):
        a=Final_list[i][0]
        recommend_list.append([df_comb['title'][a],df_comb['overview'][a]])

    return recommend_list

