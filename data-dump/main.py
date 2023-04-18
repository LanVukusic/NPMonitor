import requests
import bs4
import re
import pandas as pd
from tqdm import tqdm
import time

def clean_markdown(markdown_text):
  # remove all the images
  markdown_text = re.sub(r"!\[.*\]\(.*\)", "", markdown_text)

  # replace links with the link text
  markdown_text = re.sub(r"\[.*\]\(.*\)", "", markdown_text)


  # remove all the html tags
  markdown_text = re.sub(r"<.*>", "", markdown_text)

  # remove all the html comments
  markdown_text = re.sub(r"<!--.*-->", "", markdown_text)

  # remove special characters
  markdown_text = re.sub(r"[^a-zA-Z0-9\s]", " ", markdown_text)

  # remove all the extra spaces
  markdown_text = re.sub(r"\s+", " ", markdown_text)

  # remove all new lines
  markdown_text = re.sub(r" +", " ", markdown_text)

  return markdown_text

with open("data.md", "r") as f:
    data = f.read()

    # get all capture groups from the regex
    matches = re.findall(r"]\((.*)\)", data)

    # iterate over capture groups and collect all urls in a list
    urls = []
    for match in matches:
        urls.append(match)


l = []
# iterate over urls and download them
for url in tqdm(urls):
  with requests.session() as s:
    try:
      r = s.get(url)
      if r.status_code != 200:
        # if we get rate limited, wait for 5 minutes and try again
        print("ZzZz")
        time.sleep(40)
      
      soup = bs4.BeautifulSoup(r.text, "html.parser")
      # find the download link
      github_link = soup.find("a", {"aria-labelledby": "repository repository-link"})["href"]

      # github link parsed is in the form of : https://github.com/lodash/lodash

      # get the repo name
      repo_name = github_link.split("/")[-1]

      # get the repo owner
      repo_owner = github_link.split("/")[-2]

      # get the url to the raw readme file
      # master branch 
      readme_urls = [
        f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/master/README.md",
        f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/main/README.md",
        f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/master/readme.md",
        f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/main/readme.md",
        f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/master/Readme.md",
        f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/main/Readme.md",
      ]

      repo_markdown = ""
      for readme_url in readme_urls:
        r = s.get(readme_url)
        if r.status_code == 200:
          repo_markdown = clean_markdown(r.text)
          # print(repo_markdown)
          break
      
      if repo_markdown == "":
        continue
    
      l.append({
        "repo_url": github_link,
        "repo_name": repo_name,
        "repo_owner": repo_owner,
        "readme_url": readme_url,
        "readme_text": repo_markdown
      })
    except Exception as e:
      print(e)
      pass

df = pd.DataFrame(l)
df.to_csv("data.csv", index=False)
