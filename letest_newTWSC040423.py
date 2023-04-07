import streamlit as st
import snscrape.modules.twitter as sntwitter
from streamlit_extras.dataframe_explorer import dataframe_explorer
import pandas as pd
import datetime
import pymongo
import time

# Background Effect

page_bg_img = """
<style>
[data-testid="stAppViewContainer"]{
background-image: url("https://static.wixstatic.com/media/11062b_54784a6f95eb4ec9a18b8f5d0eafac9f~mv2_d_7113_5041_s_4_2.jpg/v1/fill/w_430,h_305,al_c,q_80,usm_0.66_1.00_0.01/11062b_54784a6f95eb4ec9a18b8f5d0eafac9f~mv2_d_7113_5041_s_4_2.jpg");
background-size: cover;
}
[data-testid="stHeader"]{
background: rgba(0,0,0,0);
}
[data-testid="stToolbar"]{
right : 2rem;
}
[data-testid="stSidebar"]{
background-image: url("https://i.pinimg.com/originals/94/7c/b0/947cb04d01c88eb3da955104657b89a7.jpg");;
background-size: cover;
}
</style>
"""
makr = st.markdown(page_bg_img, unsafe_allow_html=True)

# REQUIRED VARIABLES

client = pymongo.MongoClient("mongodb://localhost:27017/")  # To connect to MONGODB
mydb = client["Twitter_Database"]  # To create a DATABASE
tweets_df = pd.DataFrame()
dfm = pd.DataFrame()
st.write("# Twitter data scraping")
abc = st.sidebar.title("#User input#")
option = st.sidebar.selectbox(
    "How would you like the data to be searched?", ("Keyword", "Hashtag")
)
word = st.sidebar.text_input("Please enter a " + option, "Example: Elon Musk")
start = st.sidebar.date_input(
    "Select the start date", datetime.date(2020, 1, 1), key="d1"
)
end = st.sidebar.date_input("Select the end date", datetime.date(2023, 4, 1), key="d2")
tweet_c = st.sidebar.number_input("How many tweets to scrape", 0, 1000, 5)
tweets_list = []

# user Input_info

st.subheader("DETAILS")
if option == "Keyword":
    st.info("Keyword is " + word)
else:
    st.info("Hashtag is " + word)
st.info("Starting Date is " + str(start))
st.info("End Date is " + str(end))
st.info("Number of Tweets " + str(tweet_c))

# code

if word:
    if option == "Keyword":
        for i, tweet in enumerate(
                sntwitter.TwitterSearchScraper(
                    f"{word} since:{start} until:{end}"
                ).get_items()
        ):
            if i > tweet_c:
                break
            tweets_list.append(
                [
                    tweet.id,
                    tweet.date,
                    tweet.content,
                    tweet.lang,
                    tweet.user.username,
                    tweet.replyCount,
                    tweet.retweetCount,
                    tweet.likeCount,
                    tweet.source,
                    tweet.url,
                ]
            )
        tweets_df = pd.DataFrame(
            tweets_list,
            columns=[
                "ID",
                "Date",
                "Content",
                "Language",
                "Username",
                "ReplyCount",
                "RetweetCount",
                "LikeCount",
                "Source",
                "Url",
            ],
        )
    else:
        for i, tweet in enumerate(
                sntwitter.TwitterHashtagScraper(
                    f"{word} + since:{start} until:{end}"
                ).get_items()
        ):
            if i > tweet_c:
                break
            tweets_list.append(
                [
                    tweet.id,
                    tweet.date,
                    tweet.content,
                    tweet.lang,
                    tweet.user.username,
                    tweet.replyCount,
                    tweet.retweetCount,
                    tweet.likeCount,
                    tweet.source,
                    tweet.url,
                ]
            )
        tweets_df = pd.DataFrame(
            tweets_list,
            columns=[
                "ID",
                "Date",
                "Content",
                "Language",
                "Username",
                "ReplyCount",
                "RetweetCount",
                "LikeCount",
                "Source",
                "Url",
            ],
        )
else:
    st.warning(option, " cant be empty")

st.info("Total Tweets Scraped " + str(len(tweets_df) - 1))

filtered_df = dataframe_explorer(tweets_df)
if st.sidebar.button("Show Tweets"):
    # st.write(tweets_df)
    st.dataframe(filtered_df, use_container_width=True)


# DOWNLOAD AS CSV
#@st.cache_data
def convert_df(df):
    return df.to_csv().encode("utf-8")


if not tweets_df.empty:
    csv = convert_df(tweets_df)
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name="Twitter_data.csv",
        mime="text/csv",
    )

    # DOWNLOAD AS JSON
    json_string = tweets_df.to_json(orient="records")
    st.download_button(
        label="Download data as JSON",
        file_name="Twitter_data.json",
        mime="application/json",
        data=json_string,
    )

    # UPLOAD DATA TO DATABASE
    if st.button("Upload Tweets to Database"):
        coll = word
        coll = coll.replace(" ", "_") + "_Tweets"
        mycoll = mydb[coll]
        dict = tweets_df.to_dict("records")
        if dict:
            mycoll.insert_many(dict)
            ts = time.time()
            mycoll.update_many(
                {},
                {"$set": {"KeyWord_or_Hashtag": word + str(ts)}},
                upsert=False,
                array_filters=None,
            )
            st.success("Successfully uploaded to database")
            st.balloons()
        else:
            st.warning("Cant upload because there are no tweets")

st.subheader("Uploaded Datasets: ")

for i in mydb.list_collection_names():
    mycollection = mydb[i]
    # st.write(i, mycollection.count_documents({}))
    if st.button(i):
        dfm = pd.DataFrame(list(mycollection.find()))

if not dfm.empty:
    st.write(len(dfm) - 1, "Records Found")
    st.write(dfm)
