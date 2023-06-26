import  streamlit as st
import  preprocessor ,helper
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import  WordCloud


st.sidebar.title("Chat Analyser")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data=bytes_data.decode(encoding="utf-8")
    df=preprocessor.preprocessor(data)
    st.dataframe(df)

    # fetch unique users
    user_list=df['users'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show analyser wrt",user_list)

    if st.sidebar.button("Show Analysis"):
        num_msg,words,media_shared, link_shared = helper.fetch_stats(selected_user,df)
        st.title('Top Statistics')
        col1 ,col2 ,col3, col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_msg)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(media_shared)

        with col4:
            st.header("Links Shared")
            st.title(link_shared)

        # monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'],timeline['messages'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily timeline
        st.title("Daily Timeline")

        daily_timeline = helper.daily_timeline(selected_user,df)
        fig ,ax = plt.subplots()
        plt.figure(figsize=(25, 10))
        ax.plot(daily_timeline['only_date'], daily_timeline['messages'],color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # activity map
        busy_day = helper.week_activity_map(selected_user,df)
        st.title('Weekly Activity')
        col1 , col2 = st.columns(2)
        with col1:
            st.header("Most busy day")
            fig ,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            st.pyplot(fig)
        with col2:
            st.dataframe(busy_day)

        busy_month = helper.month_acitivity_map(selected_user,df)
        st.title('Weekly Activity')
        col1 , col2 = st.columns(2)
        with col1:
            st.header("Most busy day")
            fig ,ax = plt.subplots()
            ax.bar(busy_month.index,busy_month.values,color = 'orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.dataframe(busy_month)


        # finding the bussiest  user in the group(Group level)
        if selected_user == "Overall":
            st.title("Most busy User")
            x, df_percent =helper.most_busy_user(df)
            fig, ax = plt.subplots()

            col1 ,col2 = st.columns(2)
            with col1:
                ax.bar(x.index, x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(df_percent)

        # WordCloud
        st.title("WordCloud")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig ,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        most_comm_df=helper.most_used_words(selected_user,df)
        st.title("Most Common Words")
        fig ,ax =plt.subplots()
        ax.barh(most_comm_df[0],most_comm_df[1],color='green')
        plt.xticks(rotation='vertical')
        col1, col2 = st.columns(2)
        with col1:
            st.pyplot(fig)

        with col2:
            st.dataframe(most_comm_df)

        # Emoji analyser
        emoji_df = helper.emoji_analyser(selected_user,df)
        st.title("Emoji Analysis")
        fig, ax = plt.subplots()
        # ax.pie(emoji_df[0],emoji_df[1])
        # ax.set_xlim(0, 60)
        col1, col2 = st.columns(2)
        with col1:
            ax.pie(emoji_df[1],labels=emoji_df[0],autopct="%0.2f")
            st.pyplot(fig)

        with col2:
            st.dataframe(emoji_df)

        # heatmap

        user_heatmap = helper.activity_heatmap(selected_user,df)
        st.title('Heatmap')
        fig ,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        plt.figure(figsize=(20, 6))

        # plt.yticks(rotation='horizontal')
        st.pyplot(fig)
