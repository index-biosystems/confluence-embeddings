import pinecone
import os
from atlassian import Confluence
import requests
import openai
import tiktoken
from bs4 import BeautifulSoup
import setup
from atlassian import Confluence
import re

getAllSpaces = False

allSpaceKeys = ['BIR',
                'BD',
                'INDEX',
                'ITHD',
                'EC',
                'REG',
                'RD',
                'SUP',
                'HR']

pinecone.init(
    os.getenv('PINECONE_API_KEY'), 
    os.getenv('PINECONE_API_ENV'))

confluence = Confluence(
    url='https://index.atlassian.net',
    username=os.getenv('CONFLUENCE_USERNAME'),
    password=os.getenv('CONFLUENCE_API_KEY'))

# Get all relevant spaces and pages.

if getAllSpaces:
    getAllSpaces = confluence.get_all_spaces()

    allSpaceKeys = []

    for space in getAllSpaces['results']:
        allSpaceKeys.append(space['key'])

# Else use the predetermined spaces.

allPages = {}

for spaceKey in allSpaceKeys:
    allPages[spaceKey] = confluence.get_all_pages_from_space(spaceKey)

allPagesContent = {}

# Request all pages from each space.

for key, pages in allPages.items():
    allPagesContent[key] = []

    for page in pages:
        r = requests.get(f"https://index.atlassian.net/wiki/{page['_links']['webui']}", auth=(os.getenv('CONFLUENCE_USERNAME'), os.getenv('CONFLUENCE_API_KEY')))
        soup = BeautifulSoup(r.content, 'html.parser')
        content = soup.find("div", id = 'content').get_text(separator=' ')
        allPagesContent[key].append(content)

# Get all the text from each page, add it to a dict where the page is the key and the text is the value.

allPagesText = {}

for key, pages in allPagesContent.items():
    allPagesText[key] = []

    for page in pages:
        allPagesText[key].append(page)

# Tokenize the text.

allPagesTextTokenized = {}

for key, pages in allPagesText.items():
    allPagesTextTokenized[key] = []

    for page in pages:
        allPagesTextTokenized[key].append(openai.Completion.create(
            engine="davinci",
            prompt=page,
            temperature=0,
            max_tokens=64,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=["\n"]
        )['choices'][0]['text'])

# Get an openai embedding for each page.

allPagesEmbeddings = {}

for key, pages in allPagesTextTokenized.items():
    allPagesEmbeddings[key] = []

    for page in pages:
        allPagesEmbeddings[key].append(openai.Embedding.create(page))

# Save the embedding to Pinecone

for key, pages in allPagesEmbeddings.items():
    for page in pages:
        pinecone.create_index(key, pinecone.IndexInfo(metric='cosine', shards=1))
        pinecone.insert(key, page['id'], page['vector'])

# Get the embedding for a page.

def getEmbedding(page):
    return openai.Embedding.retrieve(page)

# Get the most similar pages to a page.

def getSimilarPages(page, spaceKey):
    return pinecone.query(spaceKey, page, top_k=5)

