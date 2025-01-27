# WhatsApp-Chat-Analyzer

This project allows you to analyze your WhatsApp chat data by uploading a .txt file exported from WhatsApp. It offers several insights such as message statistics, word clouds, emoji usage, and more. The project uses Python libraries like Streamlit, Pandas, Matplotlib, NLTK, and others to perform these analyses.

Features
Preprocess WhatsApp Chat Data
The uploaded chat data is preprocessed to extract:

Date and time of each message
User (sender of the message)
The message itself
Additional components like year, month, day, hour, minute
Operating System and Time Format Selection
You can specify the operating system (Apple or Android) and the time format (12 Hours or 24 Hours) of your WhatsApp export to correctly process the data.

Message Count Over Time
The total number of messages is shown. Additionally, a plot of the number of messages sent over time is provided.

Top 10 Users by Number of Messages
A bar chart displays the top 10 users based on the number of messages they sent.

Word Cloud
A word cloud is generated based on the most common words used in the chat, excluding common English stopwords.

Heatmap of Messages by Day of the Week and Hour
A heatmap shows the distribution of messages sent across different hours of the day and days of the week.

Abbreviation Expansion
Common abbreviations (like ASAP, LOL, etc.) are identified in the chat and expanded with their full forms.

Emoji Analysis
The most frequently used emoji in the chat is identified, along with its total count.

Media Links
All the URLs shared in the chat are extracted and displayed.

Requirements
Python 3.x
Streamlit
Pandas
Matplotlib
NLTK
WordCloud
Seaborn
Emoji
You can install the necessary libraries using the following command:
