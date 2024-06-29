from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import pandas as pd
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from scipy.special import softmax
from outscraper import ApiClient
from joblib import load
import warnings
import cleantext
import requests
from bs4 import BeautifulSoup
from .models import UserReviews, GeneralReviews
import time

#setup model (rating predictior)
warnings.filterwarnings("ignore")
lr_model=load('./savedModels/rating_predictor_updated.joblib')

# MODEL1 = f"cardiffnlp/twitter-roberta-base-sentiment"
# tokenizer1 = AutoTokenizer.from_pretrained(MODEL1)
# model1 = AutoModelForSequenceClassification.from_pretrained(MODEL1)

def get_flipkart_reviews(product_name):
    # replace spaces with plus sign for URL
    print("line1")
    search_query = product_name.replace(' ', '+')
    url2 = f'https://www.flipkart.com/search?q={search_query}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&sort=relevance'
    # request Flipkart search page
    print("url ===== ",url2)
    response = requests.get(url2)
    print("Response status code:", response.status_code)  # Print status code for debugging
    # print("Response text:", response.text)  # Print response text for debugging
    
    soup = BeautifulSoup(response.text, 'html.parser')
    # print("Soup object:", soup)
    # get product link from search results
    product_link = soup.find('a', {'class': 'CGtC98'})['href']
    # if product_link:
        # product_link = product_link['href']
        # print(product_link)
        # Now you can use the product_link variable
    # else:
        # print("Product link not found")
    # print(product_link)
    # request product page
    url_ = f'https://www.flipkart.com{product_link}'
    print("line2")
    print("url_ ::: ",url_)
    response = requests.get(url_)
    soup = BeautifulSoup(response.text, 'html.parser')
    reviews_link = [i['href'] for i in soup.find_all('a', href=True) if 'product-reviews' in i['href']][0]
    print("line3")
    stop=reviews_link.index('&aid')
    reviews_link=reviews_link[:stop]
    print(reviews_link)
    url=f'https://www.flipkart.com{reviews_link}'
    print(url)
    review_text=[]
    rating_score=[]
    # Find the div that contains the reviews
    for i in range(1, 2):
        url1=url+"&page="+str(i)
        print("final url:",url1)
        response = requests.get(url1)
        soup = BeautifulSoup(response.content, 'html.parser')
        reviews = soup.find_all('div', {'class': 'ZmyHeo'})
        # print("reviews:",reviews)
        for d in reviews:
            text=d.get_text()
            print("text",text)
            review_text.append(text)
        rate_box=soup.find_all('div', {'class': 'ipqd2A'})
        for r in rate_box:
            rate=r.get_text()
            print("rate",rate)
            rating_score.append(rate)
    min_len=min(len(review_text),len(rating_score))
    review_text=review_text[:min_len]
    rating_score=rating_score[:min_len]
    print("review_text",review_text)
    print("rating_score",rating_score)
    return review_text,rating_score,min_len,url_,url2

# def polarity_scores_roberta_list(review):
#     print(review)
#     print()
#     encoded_text = tokenizer1(review, return_tensors='pt')
#     output = model1(**encoded_text)
#     scores = output[0][0].detach().numpy()
#     scores = softmax(scores)
#     scores_list = [scores[0], scores[1], scores[2]]
#     return scores_list

# def polarity_scores_roberta_list(review):
#     API_URL = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment"
#     headers = {"Authorization": "Bearer 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"}
#     response = requests.post(API_URL, headers=headers, json={"inputs": review})
#     scores = response.json()[0]
#     scores_list = [item['score'] for item in scores]
#     print("scores_list",scores_list)
#     return scores_list

def polarity_scores_roberta_list(review):
    print("Review:", review)
    API_URL = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-roberta-base-sentiment"
    headers = {"Authorization": "Bearer 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"}
    response = requests.post(API_URL, headers=headers, json={"inputs": review})
    print("Response:", response.text)
    scores = response.json()[0]
    scores_list = [item['score'] for item in scores]
    print("scores_list", scores_list)
    return scores_list


#setup model (gpt3)
# HEADERS = ({'User-Agent':
#             'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
#             AppleWebKit/537.36 (KHTML, like Gecko) \
#             Chrome/90.0.4430.212 Safari/537.36',
#             'Accept-Language': 'en-US, en;q=0.5'})
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US, en;q=0.5'
}

# user define function
# Scrape the data
def getdata(url):
    r = requests.get(url, headers=HEADERS)
    return r.text

def html_code(url):
    # pass the url
    # into getdata function
    htmldata = getdata(url)
    soup = BeautifulSoup(htmldata, 'html.parser')

    # display html code
    return (soup)
def api_call(link):
    # api_client = ApiClient(api_key='Z29vZ2xlLW9hdXRoMnwxMTU3MTI4ODgzMjY3NDgyNTQ2MzF8YzBlN2I4YTE3NQ')
    # result = api_client.amazon_reviews(link, limit=10)
    # reviews = []
    # ratings = []
    # p_name = result[0][1]['product_name']
    # for i in range(len(result[0])):
    #     reviews.append(result[0][i]['body'])
    # for i in range(len(result[0])):
    #     ratings.append(result[0][i]['rating'])
    # return reviews,ratings,p_name
    soup = html_code(link)
    reviews=[]
    ratings=[]
    product_name = soup.find("h1", class_="a-size-large").get_text()
    for item in soup.find_all("div", class_="a-row a-spacing-small review-data"):
        d=item.get_text()
        if d=="":
            reviews.append(" ")
        else:
            #remove \n from the string
            d=d.replace("\n","")
            #limit size of string to 400 characters
            d=d[:400]
            reviews.append(d)
    for item in soup.find_all("span", class_="a-icon-alt"):
        d=item.get_text()
        if "1.0 out of" in d:
            ratings.append(1)
        elif "2.0 out of" in d:
            ratings.append(2)
        elif "3.0 out of" in d:
            ratings.append(3)
        elif "4.0 out of" in d:
            ratings.append(4)
        elif "5.0 out of" in d:
            ratings.append(5)

    return reviews,ratings,product_name

def get_asin(url):
    # if 'amazon' in url:
    asin = url.split('product-reviews/')[1].split('/')[0]
    print(asin)
    return asin

def get_image(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}
    # asin=get_asin(url)
    # ind=url.index('product-reviews')
    # url=url[:ind]+'dp/'+asin+'/ref=cm_cr_arp_d_product_top?ie=UTF8'
    print("image url :",url)
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    # image = soup.find('img', {'class': 'DByuf4'})['src']
    # print(image)
    # return image
    image_tag = "shttps://rukminim2.flixcart.com/image/312/312/ktket…pg3hn-a-apple-original-imag6vpyghayhhrh.jpeg?q=70"

    return image_tag
# Extract the value of the src attribute
    # if image_tag:
    #     image_url = image_tag.get('src')
    #     if image_url:
    #         print("Image URL:", image_url)
    #         # Return the image URL if needed
    #         # return image_url
    #     else:
    #         print("Image URL not found")
    # else:
    #     print("Image tag not found")

def clean(text):
    text = cleantext.clean(text, to_ascii=True, lower=True, no_line_breaks=True, no_urls=True, no_emails=True,no_emoji=True, no_phone_numbers=True, no_numbers=False, no_digits=False, no_currency_symbols=True, no_punct=False, replace_with_url="", replace_with_email="", replace_with_phone_number="", replace_with_number="", replace_with_digit="0", replace_with_currency_symbol="")
    return text

def web_scraper(url):
    reviews = []
    ratings=[]
    p_name = 'url'
    image = ''
    created = ''
    # if 'amazon' in url:
    #     counter=0
    #     while True:
    #         try:
    #             reviews,ratings,p_name = api_call(url)
    #             break
    #         except:
    #             if counter==3:
    #                 print("Server Error, Please try again later")
    #                 return redirect('home')
    #             print('waiting for 15 sec')
    #             counter+=1
    #             time.sleep(15)
        #flipkart reviews, append review and rating, continue
    is_available=False
    review = GeneralReviews.objects.filter(product_name=p_name)
    avg_rate = 0
    summary = ''
    len_review = len(reviews)
    # print(reviews)
    # if review.exists():
    #     avg_rate = review[0].rating
    #     summary = review[0].summary
    #     image = review[0].img
    #     created = review[0].created
    # else:
    # try:
    review_text,rating_score,min_len,url1,url2 = get_flipkart_reviews(url)
    for i in range(min_len):
        reviews.append(review_text[i])
        ratings.append(rating_score[i])
    is_available=True
    # except:
    #     print('no flipkart reviews')
    # print("url1:",url1)
    # image = None
    get_image(url2)
    print("image:",image)
    rev_len = len(reviews)

    # rating_scores_int = [int(score) for score in ratings]

    # # Calculate the sum of rating scores
    # total_rating_score = sum(rating_scores_int)

    # # Calculate the average rating score
    # avg_rate = total_rating_score / len(rating_scores_int)
    # print("average_Rate:",avg_rate)
    return avg_rate,url,summary,reviews,ratings,rev_len,image,created,is_available

def get_summary(reviews):
    # text summarization
    merged_reviews = ''
    for i in range(len(reviews)):
        merged_reviews += reviews[i]
    url = "https://article-extractor-and-summarizer.p.rapidapi.com/summarize-text"
    payload = { "text": merged_reviews}
    headers = {
	    "content-type": "application/json",
	    "X-RapidAPI-Key": "c5f70b06ddmsh1f4a649c3843cabp1204ccjsn3025fdfa0cc3",
	    "X-RapidAPI-Host": "article-extractor-and-summarizer.p.rapidapi.com"
    }
    response = requests.post(url, json=payload, headers=headers)
    try:
        summary = response.json()['summary']
    except:
        summary = ''
    return summary

# Create your views here.
def home(request):
    if request.method == 'POST':
            reviews = []
            ratings=[]
            p_name = ''
            image = ''
            created = ''
            rating_count = [0,0,0,0,0]
            rev_len=1
            iter = [1,2,3,4,5]
            url = request.POST['query']
            if url == '':
                return render(request, 'base/home.html')
            avg_rate, p_name, summary, reviews, ratings, rev_len, image, created, is_available = web_scraper(url)

            # if avg_rate != 0:
            #     review = GeneralReviews.objects.filter(product_name=p_name)
            #     print(p_name)
            #     avg_rate = review[0].rating
            #     summary = review[0].summary
            #     check=None
            #     if request.user.is_authenticated:
            #         check = UserReviews.objects.filter(product_name=p_name, user=request.user)
            #     else:
            #         return render(request, 'base/home.html', {'avg' : avg_rate, 'iter' : iter, 'p_name' : p_name, 'summary': summary, 'img': image, 'created': created})
            #     if request.user.is_authenticated and not check.exists():
            #         user = request.user
            #         review_save = UserReviews.objects.create(summary=review[0].summary, rating=review[0].rating, product_name=review[0].product_name,neg=review[0].neg,neu=review[0].neu,pos=review[0].pos,user=user,flipkart=is_available,img=image)
            #         review_save.save()
            #     return render(request, 'base/home.html', {'avg' : avg_rate, 'iter' : iter, 'p_name' : p_name, 'summary': summary, 'img': image, 'created': created})
            summary = get_summary(reviews)
            res = []
            op = []
            rev_len = len(reviews)
            columns = ['Id', 'roberta_neg', 'roberta_neu', 'roberta_pos','Score']
            try:
                res = []
                for i in range(rev_len):
                    # reviews[i]=clean(reviews[i])
                    res.append([i] + polarity_scores_roberta_list(reviews[i]) + [ratings[i]])
            except Exception as e:
                print("Error:", e)

            df_results = pd.DataFrame(res, columns=columns)
            rev_rate=0
            star = 0
            print("rev_len",rev_len)
            avg_pos=0
            avg_neg=0
            avg_neu=0
            for index, row in df_results.iterrows():
                avg_pos+=row['roberta_pos']
                avg_neg+=row['roberta_neg']
                avg_neu+=row['roberta_neu']
                print("---------------->",avg_pos)
                print("---------------->",avg_neg)
                star += float(lr_model.predict([[row['roberta_neg'],row['roberta_neu'],row['roberta_pos']]])[0])
                current_rating=float(row['Score'])
                print(current_rating)
                rev_rate+=current_rating
                rating_count[int(current_rating)-1]+=1
            avg_pos/=rev_len
            avg_neg/=rev_len
            avg_neu/=rev_len
            star/=rev_len
            rev_rate/=rev_len
            avg_rate = (star+rev_rate)/2
            avg_rate = round(avg_rate, 2)
            print("Avg Rating : ",avg_rate)
            print("Star Rating : ",star)
            user = None
            if request.user.is_authenticated:
                user = request.user
                review = UserReviews.objects.create(summary=summary, rating=avg_rate, product_name=p_name,neg=avg_neg,neu=avg_neu,pos=avg_pos,user=user,flipkart=is_available,img=image)
                review.save()
                review2 = GeneralReviews.objects.create(summary=summary, rating=avg_rate, product_name=p_name,neg=avg_neg,neu=avg_neu,pos=avg_pos,flipkart=is_available,sc_1=rating_count[0],sc_2=rating_count[1],sc_3=rating_count[2],sc_4=rating_count[3],sc_5=rating_count[4],img=image)
                review2.save()
            else:
                review = GeneralReviews.objects.create(summary=summary, rating=avg_rate, product_name=p_name,neg=avg_neg,neu=avg_neu,pos=avg_pos,flipkart=is_available,sc_1=rating_count[0],sc_2=rating_count[1],sc_3=rating_count[2],sc_4=rating_count[3],sc_5=rating_count[4],img=image)
                review.save()
            return render(request, 'base/home.html', {'avg' : avg_rate, 'iter' : iter, 'star' : star, 'rev' : rev_rate, 'p_name' : p_name, 'summary': summary, 'img': image,'rating_data':rating_count,'avg_pos':avg_pos,'avg_neg':avg_neg,'avg_neu':avg_neu, 'created': created})
    return render(request, 'base/home.html')

def about(request):
    
    return render(request , 'base/about.html')


def payment(request,plan):
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        address = request.form.get('address')+','+request.form.get('city')+','+request.form.get('zipcode')
        pstatus = 'success'
    if plan == 'soldier':
            amt = 38
    elif plan == 'commander':
            amt = 69
    elif plan == 'prince':
            amt = 138
    else:
        amt = 0
    return render(request, 'base/payment.html',{'amt':amt})

def success(request):
    return render(request, 'base/success.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST['uname']
        email = request.POST['email']
        message = request.POST['message']
        send_mail(
            'Contact Form',
            message,
            email,
            ['sahilshukla959@gmail.com'],
            fail_silently=False,
        )
        return render(request, 'base/contact.html')
    return render(request, 'base/contact.html')

@login_required
def reviews(request, pname):
    iter = [1,2,3,4,5]
    highlighted=GeneralReviews.objects.filter(product_name=pname)
    highlighted=highlighted[0]
    return render(request, 'base/reviews.html', {'reviews': UserReviews.objects.all(), 'iter': iter, 'highlighted':highlighted,'check':True})

@login_required
def history(request):
    iter = [1,2,3,4,5]
    return render(request, 'base/reviews.html', {'reviews': UserReviews.objects.all(), 'iter': iter,'check':False})


from .forms import ReviewForm
from .model.Roberta import analyze_review_sentiment

def analyze_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review_text = form.cleaned_data['text']
            sentiment, score = analyze_review_sentiment(review_text)
            return JsonResponse({'sentiment': sentiment, 'score': score})
    else:
        form = ReviewForm()
    return render(request, 'base/customreview.html', {'form': form})

