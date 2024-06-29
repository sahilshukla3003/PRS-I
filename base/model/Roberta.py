import requests

def analyze_review_sentiment(review):
    api_token = "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"
    api_url = "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english"
    headers = {"Authorization": f"Bearer {api_token}"}
    payload = {"inputs": review}

    response = requests.post(api_url, headers=headers, json=payload)
    if response.status_code == 200:
        result = response.json()
        sentiment = result[0][0]['label']
        score = result[0][0]['score']
        return sentiment, score
    else:
        raise Exception(f"Error: {response.status_code}, {response.text}")

# Example usage:
# if __name__ == "__main__":
    
#     review = " this is average product "
#     sentiment, score = analyze_review_sentiment(review)
#     print(f"Sentiment: {sentiment}, Score: {score}")
