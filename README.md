# WhatsApp Chat Analyzer

## Overview
The **WhatsApp Chat Analyzer** is a Python application that analyzes and visualizes WhatsApp chat data in a variety of formats. Users can upload their WhatsApp chat text files, and the application will process the data to provide insights such as message count over time, word frequency, top users, emoji usage, and more.

The project uses libraries like `Streamlit`, `pandas`, `matplotlib`, `seaborn`, and `nltk` to extract and display useful information from WhatsApp chats.

## Features
- **Message Count Over Time**: Displays a plot of the number of messages over time.
- **Top Users by Messages**: Shows the top 10 users by the number of messages sent.
- **Word Cloud**: Generates a word cloud from the chat messages.
- **Heatmap**: Visualizes the frequency of messages over the days of the week and hours of the day.
- **Abbreviation Expansion**: Lists common abbreviations used in the chat and their full forms.
- **Emoji Usage**: Shows the most used emoji and their frequency.
- **Media Links**: Extracts and displays all media links shared in the chat.

## Requirements
- Python 3.x
- Libraries:
  - `pandas`
  - `matplotlib`
  - `seaborn`
  - `nltk`
  - `streamlit`
  - `wordcloud`
  - `emoji`

Install the required libraries using the following command:
```bash
pip install -r requirements.txt

