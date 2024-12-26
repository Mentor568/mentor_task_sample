import requests
import pandas as pd
from datetime import datetime
from openai import ChatCompletion
from transformers import pipeline
import json

# Replace with your API keys and configurations
OPENAI_API_KEY = "your-openai-api-key"

# LLM Initialization
def initialize_openai():
    ChatCompletion.api_key = OPENAI_API_KEY

def initialize_llama():
    return pipeline("text-classification", model="facebook/bart-large-mnli")

# Function to fetch news data from an API
def fetch_news(api_url, query_params):
    try:
        response = requests.get(api_url, params=query_params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching news: {e}")
        return None

# Example risk analysis with OpenAI GPT
def analyze_risk_with_gpt(content):
    try:
        response = ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert in supply chain risk analysis."},
                {"role": "user", "content": content}
            ]
        )
        return response.choices[0].message['content']
    except Exception as e:
        print(f"Error with OpenAI GPT: {e}")
        return None

# Example sentiment analysis with LLaMA
def analyze_sentiment_with_llama(content, llama_pipeline):
    try:
        results = llama_pipeline(content)
        return results
    except Exception as e:
        print(f"Error with LLaMA: {e}")
        return None

# Aggregating global supply chain data into a structured format
def aggregate_data(news_data):
    try:
        structured_data = []
        for article in news_data['articles']:
            structured_data.append({
                "source": article['source']['name'],
                "title": article['title'],
                "description": article['description'],
                "content": article['content'],
                "published_at": article['publishedAt']
            })
        return pd.DataFrame(structured_data)
    except Exception as e:
        print(f"Error structuring data: {e}")
        return None

# Main pipeline
def main():
    # Initialize models
    initialize_openai()
    llama_pipeline = initialize_llama()
    
    # Example: Fetch news data
    news_api_url = "https://newsapi.org/v2/everything"
    query_params = {
        "q": "supply chain disruption",
        "from": datetime.now().strftime('%Y-%m-%d'),
        "sortBy": "relevance",
        "apiKey": "your-newsapi-key"
    }
    news_data = fetch_news(news_api_url, query_params)
    if not news_data:
        return
    
    # Aggregate data into structured format
    structured_data = aggregate_data(news_data)
    if structured_data is None:
        return
    
    # Analyze risk and sentiment
    for _, row in structured_data.iterrows():
        print(f"Analyzing article: {row['title']}")
        gpt_analysis = analyze_risk_with_gpt(row['content'])
        sentiment_analysis = analyze_sentiment_with_llama(row['content'], llama_pipeline)
        
        print("\nRisk Analysis:")
        print(gpt_analysis)
        print("\nSentiment Analysis:")
        print(sentiment_analysis)

if __name__ == "__main__":
    main()
