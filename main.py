import re
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import seaborn as sns
import os
import nltk
nltk_data_path = os.path.join(os.getcwd(), 'nltk_data')
nltk.data.path.append(nltk_data_path)
nltk.download('punkt', download_dir=nltk_data_path)
nltk.data.path.clear()
nltk.download('punkt_tab')
nltk.download("stopwords")




# Function to preprocess WhatsApp chat data
def PreProcessData(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({"User Message": messages, "Date": dates})
    df["Date"] = pd.to_datetime(df["Date"], format='%m/%d/%y, %H:%M - ')

    users = []
    messages = []
    for message in df["User Message"]:
        entry = re.split(r'([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])
    df['user'] = users
    df['message'] = messages
    df.drop(columns=["User Message"], inplace=True)

    # Extract datetime components
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["Day"] = df["Date"].dt.day
    df["Hour"] = df["Date"].dt.hour
    df["Minute"] = df["Date"].dt.minute
    return df

st.title("WhatsApp Chat Analyzer")

uploaded_file = st.file_uploader("Upload your WhatsApp chat file (.txt)", type="txt")

if uploaded_file is not None:
    data = uploaded_file.read().decode("utf-8")
    df = PreProcessData(data)

    st.subheader("Number of Messages Over Time")
    message_counts = df.groupby(df["Date"].dt.date).size()
    plt.figure(figsize=(12, 6))
    plt.plot(message_counts.index, message_counts.values, color="blue")
    plt.xlabel("Date")
    plt.ylabel("Number of Messages")
    plt.title("Number of Messages Over Time")
    plt.xticks(rotation=45)
    st.pyplot(plt)

    # Top 15 Users by Number of Messages
    st.subheader("Top 10 Users by Number of Messages")
    user_counts = df.groupby("user").size().sort_values(ascending=False).head(10)
    plt.figure(figsize=(12, 12))
    user_counts.plot(kind="bar", color="teal")
    plt.xlabel("User")
    plt.ylabel("Number of Messages")
    plt.title("Top 15 Users by Number of Messages")
    plt.xticks(rotation=90)
    plt.tight_layout()
    st.pyplot(plt)

    st.subheader("Word Cloud")
    all_test = "".join(df["message"].astype(str))
    tokenizer = word_tokenize(all_test)
    filtered_words = [word for word in tokenizer if word.isalpha() and word not in stopwords.words('english')]
    text = Counter(filtered_words)
    text.pop("Media",None)
    text.pop("omitted",None)
    word_cloud = WordCloud(height=800, width=1600).generate_from_frequencies(text)
    plt.figure(figsize=(12, 6))
    plt.imshow(word_cloud)
    plt.axis("off")
    st.pyplot(plt)

    df['DayOfWeek'] = df['Date'].dt.dayofweek
    heatmap_data = df.groupby(['DayOfWeek', 'Hour']).size().unstack(fill_value=0)
    st.subheader("Heatmap of WhatsApp Messages by Day of the Week and Hour")
    plt.figure(figsize=(12, 6))
    sns.heatmap(heatmap_data, annot=True, fmt='d', cbar_kws={"label": 'Number of Messages'})
    plt.xlabel('Hour of the Day')
    plt.ylabel('Day of the Week')
    plt.xticks(range(24), [f'{i}:00' for i in range(24)], rotation=45)
    plt.yticks(range(7), ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], rotation=0)
    st.pyplot(plt)


else:

     st.write("Please upload a WhatsApp chat file to analyze.")



