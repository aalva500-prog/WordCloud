# *********************************************************************
# Author     : Aaron Alvarez
# Course     : COP 4813: Web Application Programming
# Professor  : Gregory Reis
# Program    : Project 1 - Streamlit + 1 API + JSON Documents
# Purpose    : The goal of this first project is to create a Web application using Python,
#               Streamlit platform, the New York Times API and JSON documents to transmit
#               data across the network.
# Date       : 10/01/2020
#
#   Certification:
#   I hereby certify that this work is my own and none of it is the work of any other person.
# ..........{ Aaron Alvarez }..........
# *********************************************************************

import streamlit as st
import nltk
from nltk import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
import requests
import main_functions
from wordcloud import WordCloud
import matplotlib.pyplot as plt

nltk.download("punkt")
nltk.download("stopwords")

# Extract API_key from api_key.jason
api_key_dict = main_functions.read_from_file("JSON_Files/api_key.json")
my_api_key = api_key_dict["my_api_key"]

# Display Title
st.title("COP 4813 - Web Application Programming")
st.title("Project 1")

# Part A - The Stories API
st.header("Part A - The Stories API")

st.write("This app uses the top stories API to display the most common words used in the top current "
         "articles based on a specific topic selected by the user. The data is displayed as a line chart and "
         "as a wordcloud image.")

# Topic Selection
st.subheader("I - Topic Selection")

# Enter name
name = st.text_input("Please enter your name")

# Select Topic
topics = st.selectbox("Select a topic of your interest", ["", "arts", "automobiles", "books", "business", "fashion",
                                                          "food", "health", "home", "insider", "magazine", "movies",
                                                          "nyregion", "obituaries", "opinion", "politics", "realestate",
                                                          "science", "sports", "sundayreview", "technology", "theater",
                                                          "t-magazine", "travel", "upshot", "us", "world"])

st.set_option('deprecation.showPyplotGlobalUse', False)

# Verify that a name was inserted and a topic was selected
if len(name) > 0 and len(topics) > 0:
    # Display message showing user's name and the topic selected
    st.write("Hi {}, you selected the {} topic.".format(name, topics))

    # Extract information from API using the topic selected and the API_key
    url = "https://api.nytimes.com/svc/topstories/v2/" + topics + ".json?api-key=" + my_api_key

    # Make the request
    response = requests.get(url).json()

    # Save information to my_response.json file
    main_functions.save_to_file(response, "JSON_Files/top_stories.json")

    # Get information from my_response.json
    my_articles = main_functions.read_from_file("JSON_Files/top_stories.json")

    # Save the extracted information
    str1 = ""

    for i in my_articles["results"]:
        str1 = str1 + i["abstract"]

    # Get words from the text
    words = word_tokenize(str1)

    # Get rid of the punctuation marks
    words_no_punctuation = []

    for w in words:
        if w.isalpha():
            words_no_punctuation.append(w.lower())

    # Get rid of the stop words
    stopwords = stopwords.words("english")

    clean_words = []

    for w in words_no_punctuation:
        if w not in stopwords:
            clean_words.append(w)

    # Display the Frequency option
    st.subheader("II - Frequency Distribution")
    frequencyChk = st.checkbox("Click here to generate frequency distribution")

    # Display frequency distribution graph
    if frequencyChk:
        fdist = FreqDist(clean_words)

        most_common_words = fdist.most_common(10)
        top_words = []
        word_count = []

        for j in most_common_words:
            top_words.append(j[0])
            word_count.append(j[1])

        plt.figure(figsize=(10, 6))
        plt.plot(top_words, word_count, color='green', linewidth=2, marker='d')
        plt.xlabel('Words')
        plt.ylabel('Count')
        plt.grid()
        st.pyplot()

    # Display Wordcloud option
    st.subheader("III - Wordcloud")
    wordCloudChk = st.checkbox("Click here to generate wordcloud")

    # Display WordCloud
    if wordCloudChk:
        # Wordcloud generation
        wordcloud = WordCloud().generate(str1)

        # Display the generated image
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.show()
        st.pyplot()
        st.text("Wordcloud generated for {} topic.".format(topics))

# Part B - Most Popular Articles
st.header("Part B - Most Popular Articles")

st.write("Select if you want to see the most shared, emailed or viewed articles.")

# Select preferred set of articles
types = st.selectbox("Select you preferred set of articles", ["", "shared", "emailed", "viewed"])

# Select the period of time
time = st.selectbox("Select the period of time (last days)", ["", "1", "7", "30"])

if len(types) > 0 and len(time) > 0:
    # Extract information from API using the topic selected and the API_key
    url1 = "https://api.nytimes.com/svc/mostpopular/v2/" + types + "/" + time + ".json?api-key=" + my_api_key

    # Make the request
    response1 = requests.get(url1).json()

    # Save information to my_response.json file
    main_functions.save_to_file(response1, "JSON_Files/most_popular.json")

    # Get information from my_response.json
    my_articles1 = main_functions.read_from_file("JSON_Files/most_popular.json")

    # Save the extracted information
    str = ""

    for i in my_articles1["results"]:
        str = str + i["abstract"]

    # Wordcloud generation
    wordcloud1 = WordCloud().generate(str)

    # Display the generated image
    plt.imshow(wordcloud1)
    plt.axis("off")
    plt.show()
    st.pyplot()
    st.text("Wordcloud generated for {} articles in the last {} days.".format(types, time))
