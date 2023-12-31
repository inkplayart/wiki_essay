import requests

import re
import openai

api_key = '...' #put your API kere here, or modify this to use an environment variable, you do you

gptmodel = "gpt-3.5-turbo"

meta = [api_key,gptmodel]

current_search_term = "ENIAC"
filename = "ENIAC.txt"
num_results = 15 #change tihs to whatever you want. More means more options, fewer means more relevant
num_iterations = 6 #more iterations means more information, but higher chance of getting into WEIRD territory



"""
This function, get_response(query, meta_data), is designed to interact with the OpenAI GPT model using the ChatCompletion API.
It takes a user query and metadata as inputs, and returns a response generated by the model.

Parameters:
- query (str): The user's input query or prompt for the model.
- meta_data (list): A list containing relevant metadata information.
  - meta_data[0] (str): The API key to authenticate and access the OpenAI services.
  - meta_data[1] (str): The name or identifier of the specific GPT model to use.

Returns:
- str: The generated response text based on the user query and model's completion.

Note:
- Before calling this function, ensure that the OpenAI library is properly imported and installed.
- The function sets the API key and sends a user message to the GPT model for generating a response.
- The 'temperature' parameter controls the randomness of the response. Lower values (e.g., 0.1) make the output more deterministic, while higher values introduce more randomness.
- The function extracts the content of the generated response from the API response object.
"""

def get_response(query,meta_data):
    openai.api_key = meta_data[0]
    response = openai.ChatCompletion.create(model=meta_data[1],messages=[{"role":"user","content":query}],temperature=0.1)
    
    return response.choices[0].message.content    


"""
    Extracts bulleted list items from the given text.

    Args:
        text (str): The input text containing a bulleted list.

    Returns:
        list: A list of sanitized bulleted list items without the bullet points
              and leading spaces.
"""
def get_search_terms(text):
    pattern = r'^[-•] (.*)?$'  # Assumes bullet points start with a hyphen and a space
    bulleted_list = re.findall(pattern, text, re.MULTILINE)
    return bulleted_list


"""
    Finds the first recommended title that has not been read yet.

    Args:
        read_titles (list): A list of strings representing titles that have already been read.
        recommended_titles (list): A list of strings representing titles recommended to read.

    Returns:
        str: The first title from recommended_titles that has not been read, or "All done!" if all titles
             from recommended_titles have been read.
"""
def find_next_unread_title(read_titles, recommended_titles):
    for title in recommended_titles:
        if title not in read_titles:
            return title
    return "All done!"


"""
Retrieves search results from Wikipedia API based on a query.

Args:
    query (str): The search query to be used for retrieving results.
    num_results (int): The number of search results to retrieve.

Returns:
    list: A list of dictionaries containing search result information.
"""
def get_wikipedia_search_results(query, num_results):
    base_url = "https://en.wikipedia.org/w/api.php"
    
    # Parameters for the API request
    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": query,
        "srlimit": num_results
    }
    
    response = requests.get(base_url, params=params)
    data = response.json()
    
    return data["query"]["search"]

"""
Retrieves the introductory text content of a Wikipedia page based on its title.

Args:
    title (str): The title of the Wikipedia page to retrieve content for.

Returns:
    str: The plain text introductory content of the specified Wikipedia page.
"""
def get_wikipedia_page_content(title):
    base_url = "https://en.wikipedia.org/w/api.php"

    params = {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "exintro": True,
        "titles": title,
        "explaintext": True,  # Get plain text content
        "redirects": True     # Follow redirects
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    page = next(iter(data["query"]["pages"].values()))
    content = page.get("extract", "")

    return content


prompt = "Given the following Wikipedia summary text, generate five wikipedia search terms related to the text that someone could use to explore the topic further. Return the search terms as a bulleted list without any explanation: "

what_i_learned = ""
search_terms = [current_search_term]
seen = []

for i in range(1,num_iterations): 
    search_results = get_wikipedia_search_results(current_search_term, num_results)
    titles = []
    for result in search_results:
        print("=====" + result['title'] + "\n")
        titles.append(result['title'])
    first = find_next_unread_title(seen,titles)
    seen.append(first)
    page_content = get_wikipedia_page_content(first)
    what_i_learned = what_i_learned + "\n\n=====" + first + "\n" + page_content

    res = get_response(prompt + current_search_term,meta)
    
    terms = get_search_terms(res)
    
    current_search_term = find_next_unread_title(search_terms,terms)

print(what_i_learned)
with open(filename,'w',encoding='utf-8') as writer:
    writer.write(what_i_learned)
    
prompt = "Here is an unorganized document. It contains a main theme, but some of the information is irrelevant or out of place. Write a coherent, organized essay of about 1000 words around the three main ideas in the document, in the style of an academic essay. Use information in the document itself to support your arguments."

gptmodel = "gpt-4"
meta = [api_key,gptmodel]
res = get_response(prompt + what_i_learned,meta)
with open(filename.split(".")[0] + "_essay.txt",'w',encoding='utf-8') as writer:
    writer.write(res)