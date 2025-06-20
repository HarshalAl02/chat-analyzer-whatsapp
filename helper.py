from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extractor = URLExtract()

def fetch_stats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    #number of messages
    num_messages = df.shape[0]

    #number of words
    words = []

    for message in df['message']:
        words.extend(message.split())

    #number of media messages
    media_message_count = df[df['message'] == '<Media omitted>\n'].shape[0]

    #links shared
    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))

    return num_messages, len(words), media_message_count, len(links)

#most engaged users
def most_engaged_users(df):
    x = df['user'].value_counts().head()

    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns = {'index':'name', 'user':'percent'})
    return x, df

#wordcloud
def create_wordcloud(selected_user, df):

    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width = 500, height = 500, min_font_size = 10, background_color='#e6f2ff')

    temp['message'] = temp['message'].apply(remove_stop_words)

    df_wc = wc.generate(temp['message'].str.cat(sep=" "))

    return df_wc

def most_common_words(selected_user, df):

    f = open('stop_hinglish.txt','r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_counting(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])
    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time

    return timeline


def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('date_for_timeline').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)

    return user_heatmap


def create_custom_plotly_line(timeline_df, x_col, y_col, title, xlabel, ylabel):
    import plotly.graph_objects as go

    x_vals = timeline_df[x_col]
    xticks = list(x_vals[::3])

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=x_vals,
        y=timeline_df[y_col],
        mode='lines+markers',
        line=dict(color='#9b59b6'),
        marker=dict(symbol='circle', size=8, color='#9b59b6'),
        hovertemplate='%{x}<br>Messages: %{y}<extra></extra>'
    ))

    fig.update_layout(
        width=1200,
        height=600,
        plot_bgcolor='#f4f4f4',
        paper_bgcolor='#f4f4f4',
        title=dict(text=title, font=dict(size=16, color='#2c3e50'), x=0.5, xanchor='center'),
        xaxis=dict(
            title=dict(text=xlabel, font=dict(color='#2c3e50')),
            tickvals=xticks,
            ticktext=[str(x) for x in xticks],
            tickangle=-45,
            tickfont=dict(color='#2c3e50'),
            showgrid=False,
            zeroline=False,
            linecolor='#2c3e50',
            mirror=True,
            automargin=True,
        ),
        yaxis=dict(
            title=dict(text=ylabel, font=dict(color='#2c3e50')),
            tickfont=dict(color='#2c3e50'),
            showgrid=False,
            zeroline=False,
            linecolor='#2c3e50',
            mirror=True,
            automargin=True,
        ),
        margin=dict(l=60, r=40, t=60, b=60)
    )

    return fig

def create_custom_plotly_daily_line(timeline_df, x_col, y_col, title, xlabel, ylabel):
    import plotly.graph_objects as go

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=timeline_df[x_col],
        y=timeline_df[y_col],
        mode='lines',
        line=dict(color='#9b59b6'),
        hovertemplate='%{x}<br>Messages: %{y}<extra></extra>'
    ))

    fig.update_layout(
        width=900,
        height=500,
        plot_bgcolor='#fafafa',
        paper_bgcolor='#fafafa',
        title=dict(
            text=title,
            font=dict(size=16, color='#2c3e50'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            title=dict(text=xlabel, font=dict(color='black')),
            tickangle=90,
            tickfont=dict(color='#2c3e50'),
            showgrid=False,
            zeroline=False,
            linecolor='#2c3e50',
            mirror=True,
        ),
        yaxis=dict(
            title=dict(text=ylabel, font=dict(color='black')),
            tickfont=dict(color='#2c3e50'),
            showgrid=False,
            zeroline=False,
            linecolor='#2c3e50',
            mirror=True,
        ),
        margin=dict(l=60, r=40, t=60, b=80)
    )

    return fig


def create_custom_activity_map(data_series, title, xlabel, ylabel):
    import plotly.graph_objects as go

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=data_series.index,
        y=data_series.values,
        marker=dict(color='#6c5ce7'),
        hovertemplate='%{x}<br>Messages: %{y}<extra></extra>'
    ))

    fig.update_layout(
        width=900,
        height=500,
        plot_bgcolor='#fafafa',
        paper_bgcolor='#fafafa',
        title=dict(text=title, font=dict(size=16, color='#2c3e50'), x=0.5, xanchor='center'),
        xaxis=dict(
            title=dict(text=xlabel, font=dict(color='black')),
            tickangle=45,
            tickfont=dict(color='#2c3e50'),
            showgrid=False,
            zeroline=False,
            linecolor='#2c3e50',
            mirror=True,
        ),
        yaxis=dict(
            title=dict(text=ylabel, font=dict(color='black')),  # Explicit black label
            tickfont=dict(color='#2c3e50'),
            showgrid=False,
            zeroline=False,
            linecolor='#2c3e50',
            mirror=True,
        ),
        margin=dict(l=60, r=40, t=60, b=60)
    )

    return fig

def create_custom_horizontal_bar(data_df, title):
    import plotly.graph_objects as go

    fig = go.Figure()

    fig.add_trace(go.Bar(
        y=data_df[0],
        x=data_df[1],
        orientation='h',
        marker=dict(color='#1f77b4'),
        hovertemplate='%{y}<br>Count: %{x}<extra></extra>'
    ))

    fig.update_layout(
        width=900,
        height=600,
        bargap=0.3,
        plot_bgcolor='#fafafa',
        paper_bgcolor='#fafafa',
        title=dict(text=title, font=dict(size=16, color='#2c3e50'), x=0.5, xanchor='center'),
        xaxis=dict(
            tickfont=dict(color='#2c3e50'),
            showgrid=False,
            zeroline=False,
            linecolor='#2c3e50',
            mirror=True
        ),
        yaxis=dict(
            tickfont=dict(color='#2c3e50', size=14),
            showgrid=False,
            zeroline=False,
            linecolor='#2c3e50',
            mirror=True
        ),
        margin=dict(l=100, r=40, t=60, b=60)
    )

    return fig
