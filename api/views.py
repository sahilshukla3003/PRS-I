from urllib import response
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ReviewSerializer
from base.models import GeneralReviews
from base.views import api_call, web_scraper, get_summary, polarity_scores_roberta_list, clean, lr_model
import pandas as pd

# Create your views here.

@api_view(['GET'])
def getRoutes(request):
    routes = [
        {
            'Endpoint': '/api/review/',
            'method': 'GET',
            'body': None,
            'description': 'Returns AI generated review for a product'
        },
        {
            'Endpoint': '/api/summary/<product_url>/',
            'method': 'GET',
            'body': None,
            'description': 'Returns summary of reviews for a product'
        },
        {
            'Endpoint': '/api/rating/<product_url>/',
            'method': 'GET',
            'body': None,
            'description': 'Returns rating of a product'
        },
        {
            'Endpoint': '/api/name/<product_url>/',
            'method': 'GET',
            'body': None,
            'description': 'Returns name of a product'
        }
    ]
    return Response(routes)

@api_view(['GET','POST'])
def getReview(request):
    product_url = request.data.get('product_url')
    reviews = []
    ratings=[]
    p_name = ''
    rev_len=1
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}
    if product_url is None:
        return Response('Please enter a valid URL')
    elif 'amazon' in product_url:
        reviews,ratings,p_name = api_call(product_url)
        rev_len = len(reviews)
    review_data = GeneralReviews.objects.filter(product_name=p_name)
    # get summary from the database if it exists
    print("review_data",review_data)
    if review_data.exists():
        serializer = ReviewSerializer(review_data, many=True)
        return Response(serializer.data)
    else:
        summary = get_summary(reviews)
        res = []
        op = []
        rev_len = len(reviews)
        columns = ['Id', 'roberta_neg', 'roberta_neu', 'roberta_pos','Score']
        try:
            for i in range(rev_len):
                #reviews[i]=clean(reviews[i])
                res.append([i]+polarity_scores_roberta_list(reviews[i])+[ratings[i]])
        except:
            pass
        df_results = pd.DataFrame(res, columns=columns)
        rev_rate=0
        star = 0
        print(rev_len)
        avg_pos=0
        avg_neg=0
        avg_neu=0
        for index, row in df_results.iterrows():
            avg_pos+=row['roberta_pos']
            avg_neg+=row['roberta_neg']
            avg_neu+=row['roberta_neu']
            star += lr_model.predict([[row['roberta_neg'],row['roberta_neu'],row['roberta_pos']]])
            rev_rate+=row['Score']
        avg_pos/=rev_len
        avg_neg/=rev_len
        avg_neu/=rev_len
        print("avg_pos:",avg_pos)
        print("avg_neg:",avg_neg)
        print("avg_neu:",avg_neu)
        star/=rev_len
        rev_rate/=rev_len
        avg_rate = (star[0]+rev_rate)/2
        avg_rate = round(avg_rate, 2)
        user = None
        if request.user.is_authenticated:
            user = request.user
        review = GeneralReviews.objects.create(summary=summary, rating=avg_rate, product_name=p_name,neg=avg_neg,neu=avg_neu,pos=avg_pos, user=user)
        review.save()
        review_data = GeneralReviews.objects.filter(product_name=p_name)
        serializer = ReviewSerializer(review_data, many=True)
        return Response(serializer.data)


