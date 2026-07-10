import  streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt 
import plotly.express as px

st.title("Student result analysis")
st.write("welcome to the App")

with st.sidebar:
    selected=option_menu(
        menu_title="Menu",
        options=["Raw Data","Student Result","Topper","Search Student","Subject Analysis"],
        icons=["table","bar-chart","trophy","search","book"],
        menu_icon="menu-button-wide",
        default_index=0)

df=pd.read_csv("student_data.csv")
if selected=="Raw Data":
    st.subheader("Raw Data")
    st.dataframe(df)

elif selected =="Student Result":
    st.subheader("student performance summery")

    total_marks = df.groupby("Name")["Marks"].sum()
    average_marks = df.groupby("Name")["Marks"].mean()

    result = pd.DataFrame({"Total Marks":total_marks,"Average Marks":average_marks}).reset_index()
    st.dataframe(result)

    fig = px.bar(result,x="Name",y="Total Marks",color="Total Marks",title="Total Marks of Students")
    st.plotly_chart(fig)

    #Stacked Bar Chart for Subject-wise Marks
    st.subheader("Subject Wise Marks Of Students")
    pivot_df = df.pivot_table(index = "Name",columns ="Subject",values = "Marks",aggfunc = "sum").reset_index()

    fig,ax = plt.subplots(figsize =(8,5))

    pivot_df.plot(x ="Name", kind="bar", stacked=True, ax=ax)

    ax.set_title("Student Marks By Subject")
    ax.set_xlabel("Student Name")
    ax.set_ylabel("Marks")
    st.pyplot(fig)


elif selected == "Topper":
    total = df.groupby("Name")["Marks"].sum().sort_values(ascending=False)
    num = st.number_input("How many topper do you want?",min_value =1,max_value=len(total),value=3)

    st.subheader(f"🏆 Top {num} Students")
    st.dataframe(total.head(num))

#line chart for Topper
    fig,ax = plt.subplots(figsize = (8,5))
    ax.plot(total.index,total.values,marker = 'o')

    ax.set_title(f"Top{num} students")
    ax.set_xlabel("Students Name")
    ax.set_ylabel("Total Marks")

    st.pyplot(fig)

elif selected =="Search Student":

    st.subheader("🔍 Search Student")
    name=st.text_input("Enter Student Name")
    if name:
        filtered_df = df[df["Name"].str.contains(name,case = False)]

        if not filtered_df.empty:
            st.success(f"Showing results for `{name}`")
            st.dataframe(filtered_df)

            total_marks = filtered_df["Marks"].sum()
            average_marks = filtered_df["Marks"].mean()

            #st.write(total_marks)
            st.write("Total Marks:",{total_marks})
            st.write("Average Marks:",{average_marks})
        
        else:
            st.error(f"No results found for `{name}`")

elif  selected =="Subject Analysis":
    st.subheader("📚Subject Analysis")
    subject_avg=df.groupby("Subject")["Marks"].mean().reset_index()

    st.subheader("📘Subject wise-Average Marks")
    st.dataframe(subject_avg)

    fig=px.bar(subject_avg,x="Subject",y="Marks",color="Marks",title="Average Mark by Subject",text="Marks",color_continuous_scale="Cividis")
    st.plotly_chart(fig)






            
