#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 17:36:48 2020

@author: mac
"""
'''
url = "http://www.omdbapi.com/?i=tt3896198&apikey=53036562"
title = input('title:')
params_m = {'t':title}
response = requests.get(url, params=params_m)
results = response.json()
print(results)
'''

import sqlite3
from bs4 import BeautifulSoup
import requests
import time
import json
from requests_oauthlib import OAuth1
import secret
import pandas as pd
from pandas import DataFrame
import json 
import matplotlib.pyplot as plt
'''
#Yelp data api
place = str(input("Place:"))

API_KEY = secret.API_KEY
client_ID = secret.client_ID
API_token = API_KEY
header = {'authorization': "Bearer " + API_token}


oauth = OAuth1(API_KEY, client_ID)

base_url = 'https://api.yelp.com/v3/businesses/search'
params={'location':place, 'term':'restaurants', 'limit':10}
response = requests.get(base_url, params=params, headers=header)
results = response.json()

#Cache data

'''
#####################################
'''
#The Movie Database
url = "https://api.themoviedb.org/3/discover/movie"

API_KEY_M = secret.API_KEY_M
API_token_M = secret.API_token_M
header_M = {'Authorization': "Bearer " + API_token_M}
params_M={'year':2019, 'page':1, 'sort_by':'popularity.desc'}
response = requests.get(url, params=params_M, headers=header_M)
results_M = response.json()
print(results_M)
'''

CACHE_FILENAME = 'cache_yelp.json'
CACHE_FILENAME_M = 'cache_movie.json'
cache_dict = {}
cache_dict_M = {}
restaurant_dic = {}
restaurant_list = []
base_url = 'https://api.yelp.com/v3/businesses/search'
API_KEY = secret.API_KEY
client_ID = secret.client_ID
API_token = API_KEY
header = {'authorization': "Bearer " + API_token}
API_KEY_M = secret.API_KEY_M
API_token_M = secret.API_token_M
header_M = {'Authorization': "Bearer " + API_token_M}
DB_NAME = 'yelp_db.sqlite'
DB_NAME_M = 'movie_db.sqlite'

def open_cache():
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict

def save_cache(cache_dict):
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close()
        
def construct_unique_key(base_url, params):
    
    param_strings = []
    connector = '_'
    for k in params.keys():
        param_strings.append(f'{k}_{params[k]}')
    param_strings.sort()
    unique_key = base_url + connector + connector.join(param_strings) 
    return unique_key


def make_request_with_cache(base_url, params, headers=header):
    
    global header
    cache_dict = open_cache()
    request_key = construct_unique_key(base_url, params)
    if request_key in cache_dict.keys():
        print("fetching cached data")
        return cache_dict[request_key]
    else:
        print("making new request")
        response = requests.get(base_url, params=params, headers=header)
        results = response.json()
        cache_dict[request_key] = results
        save_cache(cache_dict)
        return cache_dict[request_key]
    
def create_Yelpdb():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    
    drop_info_sql = 'DROP TABLE IF EXISTS "Restaurant"'
    #drop_review_sql = 'DROP TABLE IF EXISTS "Review"'
    
    create_info_sql = '''
        CREATE TABLE IF NOT EXISTS "Restaurant"(
            "Id" INTEGER PRIMARY KEY AUTOINCREMENT,
            "Name" TEXT NOT NULL,
            "Rating" Real NOT NULL,
            "Address" TEXT NOT NULL,
            "Phone" TEXT NOT NULL,
            "Res_id" TEXT NOT NULL
            )
    '''
    
    
    cur.execute(drop_info_sql)
    
    cur.execute(create_info_sql)
    
    conn.commit() #save changes
    conn.close()
    print('\nSuccesfully populated Restaurant...\n')
    
# Get data from Yelp        
def infoYelp(place, category):
    global API_token
    restaurant_list = []
    header = {'authorization': "Bearer " + API_token}
    base_url = 'https://api.yelp.com/v3/businesses/search'
    params={'location':place, 'term':'restaurants', 'categories':category,'limit':50} # , 'limit':10,'sort_by':'rating',
    response = make_request_with_cache(base_url, params=params, headers=header)
    #print(response)
    for item in response['businesses']:
        restaurant_dic = {'name':item['name'], 'attribute':{}}
        restaurant_dic['name'] = item['name']
        restaurant_dic['attribute']['rating'] = item['rating']
        restaurant_dic['attribute']['address'] = item['location']['address1']
        #restaurant_dic['attribute']['price'] = item['price']
        restaurant_dic['attribute']['phone'] = item['phone']
        restaurant_dic['attribute']['id'] = item['id']
        restaurant_list.append(restaurant_dic)
        #json_string = json.dumps(restaurant_list)
    #return json_string
    #return restaurant_dic
        #print(restaurant_dic)
    with open('yelp.json', 'w') as fp:
            json.dump(restaurant_list, fp)
    
    
def populate_db():

    # Populate Countries first (Bars has connections w/Countries...):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Open the json file, read the correct info, and save to db.
    f = open('yelp.json','r')
    jsond = json.loads(f.read())
    f.close()

    for i,c in enumerate(jsond):
        statement = '''
            INSERT INTO Restaurant (
            Name, Rating, Address, Phone, Res_id
            ) VALUES (
            ?, ?, ?, ?, ?
            )
        '''
        insertions = (
        c['name'], c['attribute']['rating'], c['attribute']['address'],c['attribute']['phone'],c['attribute']['id']
        )

        #print(i)
        cur.execute(statement,insertions)
        conn.commit()

    print('\nSuccesfully populated Restaurant...\n')


def open_cache_M():
    ''' Opens the cache file if it exists and loads the JSON into
    the CACHE_DICT dictionary.
    if the cache file doesn't exist, creates a new cache dictionary
    
    Parameters
    ----------
    None
    
    Returns
    -------
    The opened cache: dict
    '''
    try:
        cache_file_M = open(CACHE_FILENAME_M, 'r')
        cache_contents_M = cache_file_M.read()
        cache_dict_M = json.loads(cache_contents_M)
        cache_file_M.close()
    except:
        cache_dict_M = {}
    return cache_dict_M

def save_cache_M(cache_dict_M):
    ''' Saves the current state of the cache to disk
    
    Parameters
    ----------
    cache_dict: dict
        The dictionary to save
    
    Returns
    -------
    None
    '''
    dumped_json_cache_M = json.dumps(cache_dict_M)
    fw = open(CACHE_FILENAME_M,"w")
    fw.write(dumped_json_cache_M)
    fw.close() 

def make_request_with_cache_M(base_url, params, headers=header_M):
    global header
    cache_dict_M = open_cache_M()
    request_key = construct_unique_key(base_url, params)
    if request_key in cache_dict_M.keys():
        print("fetching cached data")
        return cache_dict_M[request_key]
    else:
        print("making new request")
        response = requests.get(base_url, params=params, headers=header_M)
        results = response.json()
        cache_dict_M[request_key] = results
        save_cache_M(cache_dict_M)
        return cache_dict_M[request_key]
    
def create_Moviedb():
    conn = sqlite3.connect(DB_NAME_M)
    cur = conn.cursor()
    
    drop_movie_sql = 'DROP TABLE IF EXISTS "Movie"'
    #drop_genres_sql = 'DROP TABLE IF EXISTS "Genres"'
    
    create_movie_sql = '''
        CREATE TABLE IF NOT EXISTS "Movie"(
            "Id" INTEGER PRIMARY KEY AUTOINCREMENT,
            "Title" TEXT NOT NULL,
            "Popularity" REAL NOT NULL,
            "Release_Date" DATE NOT NULL,
            "Revenue" REAL NOT NULL,
            "Run_Time" REAL NOT NULL,
            "Vote_avg" REAL NOT NULL,
            "Vote_count" REAL NOT NULL
            )
    '''
    
    cur.execute(drop_movie_sql)
    #cur.execute(drop_genres_sql)
    cur.execute(create_movie_sql)
    #cur.execute(create_genres_sql)
    conn.commit() #save changes
    conn.close()
    print('\nSuccesfully populated Movie...\n')

def dataMovie():
    id_url = "https://api.themoviedb.org/3/discover/movie"
    #API_KEY_M = secret.API_KEY_M
    global API_token_M
    movie_list = []
    header_M = {'Authorization': "Bearer " + API_token_M}
    params_id={'api_key':API_KEY_M, 'sort_by':'popularity.desc'} #, 'sort_by':'popularity.desc''year':year 'with_genres':genres,
    response_id = make_request_with_cache_M(id_url, params=params_id, headers=header_M)
    for movie_info in response_id['results']:
        #title = movie_info['title']
        #popularity = movie_info['popularity']
        movie_id = movie_info['id']
        detail_url = "https://api.themoviedb.org/3/movie/" + str(movie_id)
        params_detail={'api_key':API_KEY_M}
        response_detail = make_request_with_cache_M(detail_url, params=params_detail, headers=header_M)
        title = response_detail['original_title']
        popularity = response_detail['popularity']
        release_date = response_detail['release_date']
        revenue = response_detail['revenue']
        runtime = response_detail['runtime']
        vote_avg = response_detail['vote_average']
        vote_count = response_detail['vote_count']
        movie_dict = {'title':title, 'popularity':popularity, 'release_date':release_date, 'revenue':revenue, 'runtime':runtime, 'vote_avg':vote_avg, 'vote_count':vote_count}
        movie_list.append(movie_dict)
    with open('movie.json', 'w') as fp:
        json.dump(movie_list, fp)
    

def populate_db_M():

    # Populate Countries first (Bars has connections w/Countries...):
    conn = sqlite3.connect(DB_NAME_M)
    cur = conn.cursor()

    # Open the json file, read the correct info, and save to db.
    f = open('movie.json','r')
    jsond = json.loads(f.read())
    f.close()

    for i,c in enumerate(jsond):
        #print(c)
        statement = '''
            INSERT INTO Movie (
            Title, Popularity, Release_Date, Revenue, Run_time, Vote_avg, Vote_count
            ) VALUES (
            ?, ?, ?, ?, ?, ?, ?
            )
        '''
        insertions = (
        c['title'], c['popularity'], c['release_date'],c['revenue'],c['runtime'], c['vote_count'], c['vote_avg']
        )

        #print(i)
        cur.execute(statement,insertions)
        conn.commit()

    print('\nSuccesfully populated Movie...\n')
        

        
    
def toprestaurant():
    statement = '''SELECT Name, Phone, Address, Rating FROM Restaurant ORDER BY Rating DESC LIMIT 5 '''
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    result = cur.execute(statement).fetchall()
    df = DataFrame(result)
    df.columns = ["name","phone","address","rating"]
    return df
        
        
def process_command(command):
    spl_com = command.split()
    if 'popularity' in spl_com:
        sql_query = dict(
            select = 
                '''
                SELECT Title, Popularity, Release_Date, Run_Time FROM Movie
                ''',
                order_by = "ORDER BY Popularity",
                limit = "DESC limit 5"
                )
        statement = sql_query['select']+' '+sql_query['order_by']+' '+sql_query['limit']
        # Connect and execute:
        
        conn = sqlite3.connect(DB_NAME_M)
        cur = conn.cursor()
        #print('\n',statement)
        result = cur.execute(statement).fetchall()
        df = DataFrame(result)
        df.columns = ["title","popularity","release_date","run_time"]
        return df

    elif 'count' in spl_com:
        sql_query = dict(
            select = 
                '''
                SELECT Title, Vote_count, Release_Date, Run_Time FROM Movie
                ''',
                order_by = "ORDER BY Vote_count",
                limit = "DESC limit 5"
            )
        statement = sql_query['select']+' '+sql_query['order_by']+' '+sql_query['limit']
        # Connect and execute:
        
        conn = sqlite3.connect(DB_NAME_M)
        cur = conn.cursor()
        #print('\n',statement)
        result = cur.execute(statement).fetchall()
        df = DataFrame(result)
        df.columns = ["title","vote_count","release_date","run_time"]
        return df
    
    elif 'avg' in spl_com:
        sql_query = dict(
            select = 
                '''
                SELECT Title, Vote_avg, Release_Date, Run_Time FROM Movie
                ''',
                order_by = "ORDER BY Vote_avg",
                limit = "DESC limit 5"
                )
        statement = sql_query['select']+' '+sql_query['order_by']+' '+sql_query['limit']
        # Connect and execute:
        
        conn = sqlite3.connect(DB_NAME_M)
        cur = conn.cursor()
        #print('\n',statement)
        result = cur.execute(statement).fetchall()
        df = DataFrame(result)
        df.columns = ["title","vote_avg","release_date","run_time"]
        return df

    else:
        raise SyntaxError()
    

    
def interactive_prompt():
    search=''
    while search != 'exit':
        search = input('What are you looking for? (e.g. Enter Restaurant, Movie) or "exit"\n:')
    
        if search.lower() == 'restaurant':
            create_Yelpdb()
            #infoYelp(place, category
            place = input("What city of the restaurant are you searching for\n: ")
            category = input("What kind of category are you looking for\n: ")
            infoYelp(place, category)
            populate_db()
            print(toprestaurant())
            
        elif search.lower() == 'movie':
            create_Moviedb()
            populate_db_M()
            option = ''
            while option != 'exit':
                option = input("What way do you prefer to read movie data? (e.g graph or data)\n: ")
                if option.lower() == 'exit':
                    break
                elif option.lower() == 'data': 
                    sort = ''
                    while sort != 'exit':
                        sort = input("Which way do you want to sort your data(e.g popularity, count, avg)\n:")
                        if sort.lower() == 'popularity':
                            print(process_command(sort))
                        elif sort.lower() == 'count':
                            print(process_command(sort))
                        elif sort.lower() == 'avg':
                            print(process_command(sort))
                        elif sort.lower() == 'exit':
                            break
                        else:
                            print("[Error]: Please enter a proper option(e.g popularity, count, avg)\n.")
                            continue
                elif option.lower() == 'graph':
                    sort = ''
                    while sort != 'exit':
                        sort = input("Which way do you want to sort your data(e.g popularity, count, avg)\n:")
                        if sort.lower() == 'exit':
                            break
                        elif sort.lower() == 'popularity':
                            df = process_command(sort)
                            xvals = df['title']
                            yvals = df['popularity']
                            #print(xvals)
                        elif sort.lower() == 'count':
                            df = process_command(sort)
                            xvals = df["title"]
                            yvals = df["vote_count"]
                        elif sort.lower() == 'avg':
                            df = process_command(sort)
                            xvals = df["title"]
                            yvals = df["vote_avg"]
                        else:
                            print("[Error]: Please enter a proper option(e.g popularity, count, avg)\n.")
                            continue
                        fig = plt.figure(figsize=(10,4))
                        ax = fig.add_axes([0,0,1,1])
                        #df = sortbyVoteavg()
                        xvals = xvals.tolist()
                        yvals = yvals.tolist()
                        ax.bar(xvals,yvals)
                        plt.show()
                
                else:
                    print("[Error]: Enter a proper way.(graph or data)")
                    break
        elif search.lower() == 'exit':
            print('Thanks for using our service!')
            break
        else:
            print("[Error]: Please enter a proper option.(restaurant or movie)")
            continue
                
   
if __name__ == "__main__":
    interactive_prompt()
    
    
    
    





