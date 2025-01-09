import re
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import seaborn as sns

# nltk.download("punkt")
# nltk.download("stopwords")

# Function to preprocess WhatsApp chat data
def PreProcessData(data, os_type, time_format):
    if os_type == "Apple":
        if time_format == "24 Hours":
            pattern = r'\[\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}:\d{1,2}\]\s'
            df = pd.DataFrame({"User Message": re.split(pattern, data)[1:]})
            dates = re.findall(pattern, data)
            date_format = ["[%d/%m/%y, %H%M%S] ","[%d/%m/%y, %H%M] ","[%m/%d/%y, %H:%M:%S] ","[%m/%d/%y, %H%M%S] "]
            for fmt in date_format:
                df["Date"] = pd.to_datetime(dates, format=fmt,errors="coerce")
                if not df["Date"].isna().all():
                    break
        elif time_format == "12 Hours":
            pattern = r'\[\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}:\d{1,2}\s(?:AM|PM)\]\s'

            df = pd.DataFrame({"User Message": re.split(pattern, data)[1:]})
            dates = re.findall(pattern, data)
            date_format = ["[%d/%m/%y, %H%M%S %p] ","[%d/%m/%y, %H:%M:%S %p] ","[%m/%d/%y, %H:%M:%S %p] ","[%m/%d/%y, %H:%M %p] "]
            for fmt in date_format:
                df["Date"] = pd.to_datetime(dates, format=fmt,errors="coerce")
                if not df["Date"].isna().all():
                    break
    elif os_type == "Android":
        if time_format == "24 Hours":
            pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s-\s'
            df = pd.DataFrame({"User Message": re.split(pattern, data)[1:]})
            dates = re.findall(pattern, data)
            date_format = ['%m/%d/%y, %H:%M:%S - ','%m/%d/%y, %H:%M: - ','%d/%m/%y, %H:%M:%S - ','%d/%m/%y, %H:%M - ']
            for fmt in date_format:
                df["Date"] = pd.to_datetime(dates, format=fmt,errors="coerce")
                if not df["Date"].isna().all():
                    break
        elif time_format == "12 Hours":
            pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s(?:am|pm)\s-\s'
            df = pd.DataFrame({"User Message": re.split(pattern, data)[1:]})
            dates = re.findall(pattern, data)
            date_format = ['%m/%d/%y, %H:%M:%S %p - ','%m/%d/%y, %H:%M %p - ','%d/%m/%y, %H:%M:%S %p - ','%d/%m/%y, %H:%M %p - ']
            for fmt in date_format:
                df["Date"] = pd.to_datetime(dates, format=fmt,errors="coerce")
                if not df["Date"].isna().all():
                    break
   

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

st.markdown("""
    <div style="text-align: left; font-weight: bold; font-size: 12px;">
        Android - 12 Hour - Txt file format should be day/month/year pm<br>
        24 Hour - Txt file format should be day/month/year<br>
        Apple - 12 Hour Txt file format should be day/month/year PM<br>
        24 Hour Txt file format should be day/month/year
    </div>
""", unsafe_allow_html=True)




st.title("WhatsApp Chat Analyzer")
os = st.selectbox("Operating System",["Apple", "Android"])
time_format = st.selectbox("Time Format",["12 Hours","24 Hours"])
uploaded_file = st.file_uploader("Upload your WhatsApp chat file (.txt)", type="txt")
if uploaded_file is not None:
    data = uploaded_file.read().decode("utf-8")
    df = PreProcessData(data,os,time_format)
    df=pd.DataFrame(df)
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

    # st.subheader("Word Cloud")
    # all_test = "".join(df["message"].astype(str))
    # tokenizer = word_tokenize(all_test)
    # filtered_words = [word for word in tokenizer if word.isalpha() and word not in stopwords.words('english')]
    # text = Counter(filtered_words)
    # text.pop("Media")
    # text.pop("omitted")
    # word_cloud = WordCloud(height=800, width=1600).generate_from_frequencies(text)
    # plt.figure(figsize=(12, 6))
    # plt.imshow(word_cloud)
    # plt.axis("off")
    # st.pyplot(plt)

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

    import emoji
    st.subheader("Emoji")
    all_test = "".join(df["message"].astype(str))
    emoji_count={}
    for char in all_test:
        if char in emoji.EMOJI_DATA:
            if char in emoji_count:
                emoji_count[char]+=1
            else:
                emoji_count[char]=1

    emoji = Counter(emoji_count)
    max_emoji = max(emoji.items(),key = lambda x:x[1])
    # max_emoji = max_emoji.keys()
    st.subheader(f"Most used emoji is:{max_emoji[0]}")
    st.subheader(f"Total usage:{max_emoji[1]}")


else:

     st.write("Please upload a WhatsApp chat file to analyze.")
