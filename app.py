import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import preprocessor, helper
import time

st.set_page_config(
    page_title="WhatsApp Chat Analyzer",
    page_icon="favicon.jpg",
    layout="wide"
)

logo = Image.open("logo.png")
col1, col2 = st.sidebar.columns([1, 4])
with col1:
    st.image(logo, width=40)
with col2:
    st.markdown("### Whatsapp Chat Analyzer")

#File input or sample checkbox
use_sample = st.sidebar.checkbox("Use Sample Chat")
uploaded_file = None if use_sample else st.sidebar.file_uploader("Choose a file")

data = None
if use_sample:
    try:
        with open("sample_chat.txt", "r", encoding="utf-8") as f:
            data = f.read()
    except FileNotFoundError:
        st.error("Sample chat file not found. Please ensure 'sample_chat.txt' exists.")
elif uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")

#proceeding only if data is available
if data is not None:
    df = preprocessor.preprocess(data)

    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show Analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):
        progress = st.progress(0, text="🚀 Starting analysis...")
        status_text = st.empty()

        with st.spinner("📂 Reading file... Please wait."):
            status_text.markdown("📂 **Reading uploaded file...**")
            time.sleep(0.8)
            progress.progress(25)

        with st.spinner("🧹 Cleaning up messages..."):
            status_text.markdown("🧹 **Preprocessing chat data...**")
            time.sleep(0.8)
            progress.progress(60)

        with st.spinner("📊 Crunching numbers..."):
            status_text.markdown("📊 **Generating insights and stats...**")
            time.sleep(1.2)
            progress.progress(100)

        status_text.empty()
        st.success("✅ Analysis complete! Your chat is ready to explore.")
        progress.empty()

        num_messages, words, media_message_count, links_count = helper.fetch_stats(selected_user, df)

        st.title("Top Statistics")
        column1, column2, column3, column4 = st.columns(4)
        with column1:
            st.header("Total Message")
            st.title(num_messages)
        with column2:
            st.header("Total Words")
            st.title(words)
        with column3:
            st.header("Shared Media")
            st.title(media_message_count)
        with column4:
            st.header("Shared Links")
            st.title(links_count)

        #Monthly Timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots(figsize=(12, 6))
        fig.patch.set_facecolor('#f4f4f4')
        ax.set_facecolor('#f4f4f4')
        ax.plot(timeline['time'], timeline['message'], color='#9b59b6', marker='o')
        ax.set_xticks(timeline['time'][::3])
        plt.xticks(rotation=45, color='#2c3e50')
        plt.yticks(color='#2c3e50')
        ax.tick_params(colors='#2c3e50')
        ax.set_title('Messages Over Time', color='#2c3e50', fontsize=16)
        ax.set_xlabel('Month', color='#2c3e50')
        ax.set_ylabel('Message Count', color='#2c3e50')
        plt.tight_layout()
        st.pyplot(fig)

        #Daily Timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['date_for_timeline'], daily_timeline['message'], color='#9b59b6')
        plt.xticks(rotation='vertical', color='#2c3e50')
        plt.yticks(color='#2c3e50')
        fig.patch.set_facecolor('#fafafa')
        ax.set_facecolor('#fafafa')
        plt.tight_layout()
        st.pyplot(fig)

        #Activity Map
        st.title('Activity Map')
        column1, column2 = st.columns(2)
        with column1:
            st.header("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            plt.xticks(rotation=45, color='#2c3e50')
            st.pyplot(fig)
        with column2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='#6c5ce7')
            plt.xticks(rotation=45, color='#2c3e50')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        #Most engaged users
        if selected_user == 'Overall':
            st.title("Most Engaged Users")
            x, new_df = helper.most_engaged_users(df)
            fig, ax = plt.subplots()
            column1, column2 = st.columns(2)
            with column1:
                ax.bar(x.index, x.values, color='#4a90e2')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with column2:
                st.dataframe(new_df)

        #Wordcloud
        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #Most common words
        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')
        st.title("Most Common Words")
        st.pyplot(fig)

        #Emoji analysis
        emoji_df = helper.emoji_counting(selected_user, df)
        st.title("Emoji Analysis")
        column1, column2 = st.columns(2)
        with column1:
            st.dataframe(emoji_df)
        with column2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
            st.pyplot(fig)
