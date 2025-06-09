import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
from fpdf import FPDF
import tempfile
import os
import preprocessor, helper
import time
import math
import plotly.express as px

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

#file input or sample checkbox
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

#temporary directory to save plots for PDF
plot_paths = []
temp_dir = tempfile.mkdtemp()

def save_plot(fig, name):
    path = os.path.join(temp_dir, name)
    fig.savefig(path, bbox_inches='tight')
    plot_paths.append(path)
    plt.close(fig)

#PDF report helper class
class PDFReport(FPDF):
    def header(self):
        self.set_font("Arial", 'B', 12)
        self.cell(0, 10, 'WhatsApp Chat Analysis Report', 0, 1, 'C')
        self.ln(5)

    def add_stat(self, title, value):
        self.set_font("Arial", 'B', 11)
        self.cell(40, 10, f"{title}: {value}", ln=1)

    def add_image(self, path, title):
        self.set_font("Arial", 'B', 12)
        self.cell(0, 10, title, ln=1)
        self.image(path, w=180)
        self.ln(10)

#animated stat values display
def display_stats_value(final_value, duration=1.2, steps=60, unit=""):
    placeholder = st.empty()
    increment = max(1,math.ceil(final_value / steps))

    for val in range(0, final_value, increment):
        placeholder.title(f"{val}{unit}")
        time.sleep(duration/steps)
    placeholder.title(f"{final_value}{unit}")

@st.cache_data(show_spinner="🔄 Preprocessing chat...")
def load_and_preprocess(data):
    return preprocessor.preprocess(data)


if data is not None:
    try:
        df = load_and_preprocess(data)

        if df.empty or 'user' not in df.columns or 'message' not in df.columns:
            raise ValueError("Invalid chat format.")

    except Exception as e:
        st.error("❌ Error: The uploaded file doesn't seem to be a valid WhatsApp chat export.")
        st.stop()

    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
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

        pdf = PDFReport()
        pdf.add_page()
        pdf.add_stat("Total Messages", num_messages)
        pdf.add_stat("Total Words", words)
        pdf.add_stat("Shared Media", media_message_count)
        pdf.add_stat("Shared Links", links_count)

        st.title("Top Statistics")
        column1, column2, column3, column4 = st.columns(4)
        with column1:
            st.header("Total Message")
            display_stats_value(num_messages)
        with column2:
            st.header("Total Words")
            display_stats_value(words)
        with column3:
            st.header("Shared Media")
            display_stats_value(media_message_count, unit=" 📷")
        with column4:
            st.header("Shared Links")
            display_stats_value(links_count, unit=" 🔗")

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
        #st.pyplot(fig)
        save_plot(fig, "monthly_timeline.png")
        fig = px.line(timeline, x='time', y='message', markers=True)
        fig = helper.create_custom_plotly_line(timeline, 'time', 'message', 'Messages Over Time', 'Month', 'Message Count')
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

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
        #st.pyplot(fig)
        save_plot(fig, "daily_timeline.png")
        fig = helper.create_custom_plotly_daily_line(daily_timeline, 'date_for_timeline', 'message', 'Messages Over Days', 'Date', 'Message Count')
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})


        #Activity Map
        st.title('Activity Map')
        column1, column2 = st.columns(2)
        with column1:
            st.header("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='#6c5ce7')
            plt.xticks(rotation=45, color='#2c3e50')
            #st.pyplot(fig)
            save_plot(fig, "busy_day.png")
            fig = helper.create_custom_activity_map(busy_day, "Most Busy Day", "Day", "Messages")
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

        with column2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='#6c5ce7')
            plt.xticks(rotation=45, color='#2c3e50')
            #st.pyplot(fig)
            save_plot(fig, "busy_month.png")
            fig = helper.create_custom_activity_map(busy_month, "Most Busy Month", "Month", "Messages")
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

        #Weekly Activity Map
        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)
        save_plot(fig, "weekly_activity_heatmap.png")

        #Most engaged users
        if selected_user == 'Overall':
            st.title("Most Engaged Users")
            x, new_df = helper.most_engaged_users(df)
            fig, ax = plt.subplots()
            column1, column2 = st.columns(2)
            with column1:
                ax.bar(x.index, x.values, color='#6c5ce7')
                plt.xticks(rotation=45)
                #st.pyplot(fig)
                save_plot(fig, "most_engaged_users.png")
                fig = helper.create_custom_activity_map(x, "Most engaged users", "Users", "Messages")
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            with column2:
                st.dataframe(new_df)

        #Wordcloud
        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        #ax.axis('off')
        st.pyplot(fig)
        save_plot(fig, "wordcloud.png")

        #Most common words
        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')
        st.title("Most Common Words")
        #st.pyplot(fig)
        save_plot(fig, "most_common_words.png")
        fig = helper.create_custom_horizontal_bar(most_common_df, "Most Common Words")
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

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
            save_plot(fig, "emoji_analysis.png")

        #adding all saved plots to PDF
        for path in plot_paths:
            title = os.path.splitext(os.path.basename(path))[0].replace('_', ' ').title()
            pdf.add_page()
            pdf.add_image(path, title)

        #save and serve PDF file
        final_pdf_path = os.path.join(temp_dir, "chat_report.pdf")
        pdf.output(final_pdf_path)

        with open(final_pdf_path, "rb") as f:
            st.download_button("📄 Download PDF Report", f, file_name="WhatsApp_Chat_Report.pdf")

        st.success("✅ PDF report generated!")
