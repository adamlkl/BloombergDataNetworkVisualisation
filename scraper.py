#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 14:21:43 2019

@author: Adamlkl
"""
from github import Github
from collections import OrderedDict
from collections import defaultdict
import operator
import json

token = "" 

# sort the dict according to their values of their keys
def get_top_count(data, n=1, order=False):

    if n > len(data):
        n = len(data)
    top = sorted(data.items(), key=operator.itemgetter(1), reverse=True)[:n]
    if order:
        return OrderedDict(top)
    return dict(top)

def get_category(loc):
    if loc<=10000:
        category = 0
    elif loc>=10000 and loc<=20000:
        category = 1
    elif loc>20000 and loc<=50000:
        category = 2
    elif loc>50000 and loc<=80000:
        category = 3
    elif loc>80000 and loc<=100000:
        category = 4
    elif loc>100000 and loc<=150000:
        category = 5
    elif loc>150000 and loc<=200000:
        category = 6
    elif loc>200000 and loc<=350000:
        category = 7
    elif loc>350000 and loc<=500000:
        category = 8
    elif loc>500000 and loc<=800000:
        category = 9
    elif loc>800000 and loc<=1200000:
        category = 10
    elif loc>1200000 and loc<=1800000:
        category = 11
    else: 
        category = 12
        
    return category
    
def crawler(org_name, token):
    g = Github(token)
    user = g.get_user(org_name)
    
    repo_lang = defaultdict(list)
    nodes = []
    
    for repo in user.get_repos():
        y = repo.get_languages()
        to = get_top_count(y, n=1)
        loc = 0
        for lang in to:
            repo_lang[lang].append(repo.name)
            loc += to[lang]
        nodes.append({"name":repo.name, "group":get_category(loc)})
        
    links = []       
    for lang in repo_lang:
        for repo in repo_lang[lang]:
            for repo2 in repo_lang[lang]:
                if repo != repo2:
                    links.append({ "source":repo, "target":repo2})
    
    data = {}
    data["nodes"]=nodes
    data["links"]=links
    with open('bloomberg_network_data.json', 'w') as outfile:
        json.dump(data, outfile)
    
def main():
    org_name = "Bloomberg"
    crawler(org_name, token)
    
if __name__ == '__main__':
    main()