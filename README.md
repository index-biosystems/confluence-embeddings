# Confluence Embeddings

Confluence Embeddings is a simple application that allows users of Atlassian's Confluence knowledgebase to provide OpenAI's GPT LLM with additional proprietary context that is not available on the open internet. 

Once all of your pages in confluence have the correct 'embedding' label (see Usage & Setup for more information), the contextualizer.py script will scrape those labelled pages for content, tokenize that content and create embeddings for upsertion into Pinecone's vector database. The streamlit app will take the prompt entered, do a similarity search on the vector databse, and take the top result from that search and chain that result into a GPT4 prompt question. This is how you can provide GPT4 with proprietary context for your prompts.

This is a very simple implementation and I will likely make some updates as we use this more frequently at Index. You're of course welcome to use it at your organization as well. Please share any improvements.

## Installation

Clone the repository.

## Usage & Setup

1. Install all dependencies.
2. Create an .env and update the variables.
3. Select the spaces that you'd like to use by updating the allSpaceKeys list in the page-labeller.py file. 
4. Run the page-labeller.py file to update all pages in each of those spaces with the "embedding" page label. This is the label that is subsequently used by the contextualizer.py file to create the embeddings for upserting into Pinecone.
5. Run `streamlit run app.py` from the root of the directory to get the app running on your browser.

## Todos

1. Add namespaces and metadata to the embeddings.
2. ...

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)