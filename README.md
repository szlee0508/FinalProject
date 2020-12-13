# FinalProject_szlee
## If you’d like to see further information, please go to final_project.docx.

### 1. API Application:
Yelp API & The Movie Database(TMD) API 

Please put your API key in “secret.py” file, the format of API Key will be like

API_KEY=””(This is for Yelp)

client_ID =””(This is for Yelp)

API_KEY_M=””(This is for TMD)

API_token_M=””(This is for TMD)

### 2. Code structure:
final_proj.py

In the first part, I created an database and table for both Yelp and The Movie Database. There are six fields in Restaurant table, including Id, Name, Rating, Address, Phone and Res_id; there are eight columns in Movie table, including Id, Title, Popularity, Release_Date, Revenue, Run_time, Vote_count and Vote_avg.

Secondly, user can choose which information they want to know, restaurants or movie. If they type restaurant, it will connect to Restaurant table in yelp_db database. I applied cache and infoYelp() to retrieve data from Yelp based on a city and a category which entering by user. After typing a city and a category, it will return top 5 restaurant which contain name, phone, address and rating information based on their search word.

On the other hand, if they type movie for the first interactive step, it will connect to Movie table in movie_db database. The user can enter the presentation of the data they want to see, the dataframe or bar graph, they can also choose how to order the data. 

### 3. User guide:
Install requirements.txt

Run the final_proj.py in the command line
