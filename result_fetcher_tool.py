# -*- coding: utf-8 -*-
"""
Created on 22/11/2019
@author: Emre Kavur
This script gets evaluation scores of a challenge hosted on grand-challenge.org website.
The result page of the challenge should be defined at "url" .
Results can be exported as csv files.

Necessary packages: bs4, urllib, re, pandas, simplejson
Tested on Python==3.7.4, bs4==0.0.1, urllib3==1.25.3, pandas==0.24.2, simplejson==3.16.0 
"""

from bs4 import BeautifulSoup
import urllib.request
import re
import pandas as pd
import simplejson

### Usage of the script with three examples. You may select one of them:

## 1) Parameters for CHAOS challenge to get DICE values
url = "https://chaos.grand-challenge.org/evaluation/results/"  # Results page of CHAOS challenge.
main_key = 'case'
sub_key = 'Total_scr'  # 'Total_scr', 'DICE', 'ASSD', 'MSSD', 'RAVD', 'DICE_scr', 'ASSD_scr', 'MSSD_scr', 'RAVD_scr' can be selected.
multitask = True
include_empty_tasks = False
exclude_key = 'All_Tasks_Aggregate'
csv_name = 'CHAOS_Total_scr_scores.csv'


## 2) Parameters for SLiver07 challenge to get 'Total_score'
# url = "https://sliver07.grand-challenge.org/evaluation/results/"
# main_key = 'case'
# sub_key = 'Total_score'
# multitask = False
# include_empty_tasks = False
# csv_name = 'SLiver07_scores.csv'

## 3) Parameters for ACDC@LUNGHP challenge to get 'DiceCoefficient' values
# url = "https://acdc-lunghp.grand-challenge.org/evaluation/results/"
# main_key = 'case'
# sub_key = 'DiceCoefficient'
# multitask = False
# include_empty_tasks = False
# exclude_key = ''
# csv_name = 'acdc-lunghp_scores.csv'

def main():
    links = get_user_score_links(url)
    ALL_SCORES = get_challenge_scores(links, include_empty_tasks=False)
    ALL_SCORES.to_csv(csv_name, index=False)


def get_user_score_links(url):
    """
    This function retrieves all links in the challenge result page. After that,
    it filters the links that only belong to submissions results.
    :param url: address of the challenge result page
    """
    resp = urllib.request.urlopen(url)
    soup = BeautifulSoup(resp, from_encoding=resp.info().get_param('charset'), features="html.parser")

    links = []
    for link in soup.find_all('a', href=True):
        if re.search('^{}.*/$'.format(url), link['href']) is not None:
            links.append(link['href'])
    links = list(set(links))
    return links


def get_challenge_scores(links, include_empty_tasks=False):
    """
    This function fetchs scores of all participants in selected challenge.
    :param links: Links of all submissions in the challenge.
    :param empty_tasks: If True, scores of empty tasks will be added as zero points.
    Otherwise empty tasks will be skipped.
    """
    if multitask:
        all_scores = pd.DataFrame(columns=['task', 'alg_name', 'value', 'case'])  # Main dataFrame to store all scores
    else:
        all_scores = pd.DataFrame(columns=['alg_name', 'value', 'case'])  # Main dataFrame to store all scores
    duplicate_names = {}  # In case of multiple submissions, team name is modified.

    for link in links:
        resp = urllib.request.urlopen(link)
        soup = BeautifulSoup(resp, from_encoding=resp.info().get_param('charset'), features="html.parser")
        alg_name, duplicate_names = get_alg_name(soup, all_scores, duplicate_names)
        print(alg_name)
        all_scores = get_alg_data(soup, all_scores, alg_name, include_empty_tasks)

    print('{} results collected'.format(len(links)))
    return all_scores


def get_alg_name(soup, data_frame, duplicate_names):
    """
    This function gets algorithm/team/participant name of the submission. If the name was previously used,
    it adds an index at the end of the name to separate different submissions from same teams.
    :param soup: HTML output of the page.
    :param data_frame: Main DataFrame that stores all scores
    :param duplicate_names: In case of multiple submissions, duplicate names are stored by a dictionary.
    """
    info = soup.find_all('img', alt='User Mugshot')
    alg_name = info[0].text.replace(' ', '')
    if sum(data_frame['alg_name'].str.contains(alg_name)) > 0:
        if alg_name in duplicate_names:
            last_name = duplicate_names[alg_name]
            idx = int(last_name[len(alg_name):])
            alg_name_new = alg_name + str(idx + 1)
        else:
            alg_name_new = alg_name + str(2)
        duplicate_names[alg_name] = alg_name_new
        alg_name = alg_name_new
    return alg_name, duplicate_names


def get_alg_data(soup, all_scores, alg_name, add_empty_tasks):
    """
    This function gets results of the submission from webpage. It returns results in DataFrame object.
    :param soup: HTML output of the page.
    :param alg_name: Algorithm/team/participant name
    :param add_empty_tasks: If True, scores of empty tasks will be added as zero points.
    Otherwise empty tasks will be skipped.
    """
    info = soup.find_all('div', class_='col overflow-auto')
    data = simplejson.loads(info[0].contents[7].text)
    if multitask:
        for key in data:
            if key != exclude_key:
                tmp = pd.DataFrame(columns=list(all_scores))
                values = list(data[key][main_key][sub_key].values())
                values = [0 if i is None else i for i in values]
                if add_empty_tasks or (not add_empty_tasks and sum(values) > 0):
                    cases = list(data[key][main_key][sub_key].keys())
                    task = [key[0:5]] * len(cases)
                    name = [alg_name] * len(cases)
                    tmp['task'] = task
                    tmp['alg_name'] = name
                    tmp['value'] = values
                    tmp[main_key] = cases
                    all_scores = all_scores.append(tmp, ignore_index=True)
    else:
        tmp = pd.DataFrame(columns=list(all_scores))
        values = list(data[main_key][sub_key].values())
        if add_empty_tasks or (not add_empty_tasks and sum(values) > 0):
            cases = list(data[main_key][sub_key].keys())
            name = [alg_name] * len(cases)
            tmp['alg_name'] = name
            tmp['value'] = values
            tmp[main_key] = cases
            all_scores = all_scores.append(tmp, ignore_index=True)
    return all_scores


if __name__ == '__main__':
    main()
