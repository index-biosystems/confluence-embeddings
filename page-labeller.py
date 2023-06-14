import config
from config import os

from atlassian import Confluence

getAllSpaces = False

# Add your space keys here.

allSpaceKeys = ['BIR',
                'BD',
                'INDEX',
                'ITHD',
                'EC',
                'REG',
                'RD',
                'SUP',
                'HR']

confluence = Confluence(
    url=os.getenv('CONFLUENCE_URL'),
    username=os.getenv('CONFLUENCE_USERNAME'),
    password=os.getenv('CONFLUENCE_API_KEY'))

# Get all relevant spaces and pages.

if getAllSpaces:
    getAllSpaces = confluence.get_all_spaces()

    allSpaceKeys = []

    for space in getAllSpaces['results']:
        allSpaceKeys.append(space['key'])

# Get all pages from each space.

allPages = {}

for spaceKey in allSpaceKeys:
    allPages[spaceKey] = confluence.get_all_pages_from_space(spaceKey)

# Add an 'embedding' label for each page. Sometimes the page ID is not found, so we'll just skip those and deal with them manually.

for key, pages in allPages.items():
    for page in pages:
        try:
            confluence.set_page_label(page['id'], 'embedding')
        except Exception:
            pass