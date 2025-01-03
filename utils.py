from bing_image_downloader import downloader
from gtts import gTTS
import os
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
import json
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from config import config
import google.generativeai as genai
# function to download images
def image_downloader(query, limit):
    search_term = query
    limit = limit

    downloader.download(search_term, limit=limit, output_dir='dataset',
                    adult_filter_off=True, force_replace=False, timeout=60)
    return "success"

def scrape_clean_content(url, word_limit=600):
    try:
        # Send an HTTP GET request to the website
        response = requests.get(url)
        response.raise_for_status()

        # Parse the HTML content of the website
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract all text content
        raw_text = soup.get_text(separator=' ', strip=True)

        # Clean and split the text into words
        words = raw_text.split()
        cleaned_words = [word for word in words if word.isalnum()]  # Remove non-alphanumeric characters

        # Limit the text to the specified word count
        cleaned_text = ' '.join(cleaned_words[:word_limit])

        return cleaned_text
    except requests.exceptions.RequestException as e:
        return f"Error accessing the website: {e}"
    
def get_content(scraped_content, lang = 'malayalam'):
    try:
        genai.configure(api_key=config.GOOGLE_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")
        template = """scraped content: {scraped_content}
        can you provide a 30 s reel content in malayalam Language with the scraped content given? Don't give any explanation. Only give output in json format as given as the below format.
        output format: {{"content": "audio content in malayalam..."}}"""
        prompt = PromptTemplate(input_variables=["scraped_content"], template=template)
        query = prompt.format(scraped_content = scraped_content)

        response = model.generate_content(query)
        response_text = response.text
        # Remove the backticks and newline characters
        cleaned_response = response_text.replace("```json", "").replace("```", "").strip()
        data =  json.loads(cleaned_response)
        content = data['content']
        return content
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def create_audio(audio_content):
    try:
        text = audio_content
        # Create a TTS object
        tts = gTTS(text, lang='ml')

        # Save to a file
        tts.save("malayalam.mp3")
        return "success"
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
    
