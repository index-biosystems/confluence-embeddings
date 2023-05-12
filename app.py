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
                'ITSAMPLE',
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

# Get all the text from each page.

# Tokenize the text.

# Convert into an embedding

# Save the embedding to Pinecone