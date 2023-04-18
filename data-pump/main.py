import pandas as pd
import requests
import numpy as np

EMBEDDER_URL = "http://0.0.0.0:8080/vectors"

def clean_text_json_valid(text):
  # remove newlines
  text = text.replace("\r", " ").replace("\n", " ")
  # remove tabs
  text = text.replace("\t", " ")
  # remove multiple spaces
  text = " ".join(text.split())
  return text

def get_embedded_readme(text):
  # Create the request body
  body = {
    "text": clean_text_json_valid(text)
  }
  # Get the embedded readme
  response = requests.post(EMBEDDER_URL, json=body)
  # Get the embedded vector
  vector = response.json()["vector"]

  n = np.array(vector)

  return n


# get the data
df = pd.read_csv("data.csv")


# store the embedded readmes in a list
embedded_readmes = []
names = []
# iterate over the data
for index, row in df.iterrows():
  # get the repo name
  repo_name = row["repo_name"]
  # get the repo owner
  repo_owner = row["repo_owner"]
  # get the readme text
  readme_text = row["readme_text"]
  # get the readme url
  readme_url = row["readme_url"]

  # validate the readme text
  if(type(readme_text) != str):
    continue
  if(len(readme_text) == 0):
    continue

  # get the embedded readme
  embedded_readme = get_embedded_readme(readme_text)
  embedded_readmes.append(embedded_readme)

 # store the repo name
  names.append(repo_name)

  # if(len(embedded_readmes) == 100):
  #   break


# add everything to a numpy array and save it
np.save("embedded_readmes.npy", np.array(embedded_readmes))
np.save("names.npy", np.array(names))