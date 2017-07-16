import os
import requests
import pickle
from git import Repo
from datetime import datetime
from jinja2 import Template,Environment, FileSystemLoader

dir_path = os.path.dirname(os.path.realpath(__file__))

def fetchjson(urlstr):
    #Fetch results
    response = requests.get(url=urlstr)
    return response.json()


#load cache
try:
    with open(os.path.join(dir_path,'cache.pickle'), "rb") as input_file:
        cache = pickle.load(input_file)
except (EnvironmentError,EOFError):
    cache = {}
    cache['last_run'] = datetime(2000,1,1).strftime('%Y-%m-%dT%H:%M:%SZ')

last_run = datetime.strptime(cache['last_run'],'%Y-%m-%dT%H:%M:%SZ')

# import pprint
# pprint.pprint(cache)
# exit()

i = 0
for repo in fetchjson('https://api.github.com/search/repositories?q=scoop+buckets&per_page=500')['items']:
    
    name = repo['name']
    repofoldername = repo['full_name'].replace('/','+')
    git_clone_url = repo['git_url']
    html_url = repo['html_url']
    repo_score = repo['score']
    last_updated = datetime.strptime(repo['updated_at'],'%Y-%m-%dT%H:%M:%SZ')    

    if(not repofoldername in cache):
        #Delete folder if exists
        #clone repo to cache folder
        i += 1
        Repo.clone_from(git_clone_url, os.path.join(dir_path,'cache',repofoldername))
        cache[repofoldername] = {'name':name,'url':html_url,'score':float(repo_score),'entries':[]}        
    
    elif repofoldername in cache and (last_updated > last_run ):
        i += 1
        repo = Repo(os.path.join(dir_path, 'cache', repofoldername))
        o = repo.remotes.origin
        o.pull()

    if(not os.path.isdir(os.path.join(dir_path,'cache',repofoldername))):
        continue

    cache[repofoldername]['entries'] = []
    for f in os.listdir(os.path.join(dir_path,'cache',repofoldername)):
        file_path = os.path.join(dir_path,'cache',repofoldername,f)
        if(os.path.isfile(file_path) and os.path.splitext(file_path)[1] == '.json'):            
            cache[repofoldername]['entries'].append(os.path.splitext(f)[0])


#update last run
cache['last_run'] = datetime.strftime(datetime.now().replace(hour=0, minute=0, second=0),'%Y-%m-%dT%H:%M:%SZ')

try:
    with open(os.path.join(dir_path,'cache.pickle'), "wb") as input_file:
        pickle.dump(cache,input_file)
except EnvironmentError:
    pass
print(i,' repos updated')


#Sort Repos by github score
repos = [repo for repo in cache.keys()]
actual_repos = [ repo for repo in repos if (repo != 'last_run' and len(cache[repo]['entries']) > 0) ]
sorted(actual_repos, key=lambda repo:cache[repo]['score'])
print(str(len(actual_repos)) + 'valid repositories found.')

#Update Readme file
TEMPLATE_ENVIRONMENT = Environment(
    autoescape=False,
    loader=FileSystemLoader(os.path.join(dir_path, 'template')),
    trim_blocks=False)
context = {
        'sortedrepos':actual_repos,
        'cache': cache
}
markdown_content = TEMPLATE_ENVIRONMENT.get_template('ReadmeTemplate.tpl').render(context)
with open(os.path.join(dir_path,'..','README.md'), "w") as readme_file:
    readme_file.write(markdown_content)

print('[INFO] Script Finished...')