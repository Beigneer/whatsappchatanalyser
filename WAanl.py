import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt 
import seaborn as sns

plt.style.use('dark_background')

st.sidebar.title("Whatsapp Chat analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()  
    data = bytes_data.decode("utf-8")
    # st.text(data)  
    df = preprocessor.preprocess(data)

    # st.dataframe(df)\\

    user_list = df['user'].unique().tolist()
    user_list.remove('Group notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)

    if st.sidebar.button("Show Analysis"):
        num_message,total_word,num_media = helper.fetch_stats(selected_user,df)
        st.columns(4)
        st.title('Top Statistics')
        # st.dataframe(df)


        col1,col2,col3,col4 =st.columns(4)

        

        with col1:
            st.header("Total Messsage")
            st.title(num_message)
        with col2:
            st.header("Total words")
            st.title(total_word)
        with col3:
            st.header("Total Media")
            st.title(num_media)
        col1,col2 = st.columns(2)

        with col1:
            fig,ax = plt.subplots()
            st.title('Monthly message')
            monthly,daily = helper.dailymonthly_stats(selected_user,df)
            sns.lineplot(x=monthly['time'],y=monthly['message'])
            plt.xticks(rotation='vertical')
            st.pyplot(fig)        
        with col2:
            fig2,ax = plt.subplots()
            st.title('Daily Message')
            sns.lineplot(x=daily['date'],y=daily['message'])
            plt.xticks(rotation='vertical')
            st.pyplot(fig2) 
        # FINDING THE BUSIEST USER IN GROUP

        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x,percent = helper.fetch_mostbusyuser(df)
            fig, ax = plt.subplots()
            # plt.style.use('dark_background')

            col1,col2 =st.columns(2)

            with col1:
                sns.barplot(y=x.values, x=x.index, alpha=0.8)
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(percent)

        # col1,col2 = st.columns(2)
        # activity map
        col1,col2 =st.columns(2)
        
        with col1:
            st.title('Days Activity')
            fig,ax = plt.subplots()
            day_activity = helper.day_activeness(selected_user,df)
            sns.barplot(x=day_activity['days'],y=day_activity['times'])
            plt.xticks(rotation='vertical')
            st.pyplot(fig) 
        with col2:
            st.title('Months Activity')
            fig,ax = plt.subplots()
            month_activity = helper.month_activeness(selected_user,df)
            sns.barplot(x=month_activity['months'],y=month_activity['message'])
            plt.xticks(rotation='vertical')
            st.pyplot(fig) 
                
        # wordcloud
        st.title('Wordclouds')
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        plt.axis("off")
        st.pyplot(fig)

        # with col2:
        st.title('Most Frequent words')
        mostcommon_df = helper.most_common_words(selected_user,df)
        # st.dataframe(mostcommon_df)
        fig,ax = plt.subplots()
        sns.barplot(y=mostcommon_df[0],x=mostcommon_df[1])
        plt.xticks(rotation='vertical')
        plt.xlabel("Keyword")
        plt.ylabel('Frequency')
        st.pyplot(fig)

        # heatmap
        user_heatmap = helper.activity_heatmap(selected_user,df)
        st.title('Weekly activity map')
        fig,ax = plt.subplots()
        sns.heatmap(user_heatmap)
        plt.yticks(rotation='horizontal')
        st.pyplot(fig)




