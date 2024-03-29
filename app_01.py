import streamlit as st
import openai
import markdown

# Set OpenAI API key
openai.api_key = st.secrets["openai"]["api_key"]


# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

session_state = st.session_state


# Define homepage layout
def home_page():

        st.title("解惑学院")
        st.write("欢迎来到解惑学院！")

        # Add navigation options
        st.write("导航：")
        if st.button("个人简历"):
            # Check if user is logged in
            if not session_state["logged_in"]:
                st.warning("请先登录")
                st.experimental_set_query_params(page="login")
                
            else:
                st.experimental_set_query_params(page="resume")
                

        if st.button("代码编写"):
            st.experimental_set_query_params(page="code")
        if st.button("检查代码Bug"):
            st.experimental_set_query_params(page="bug")
        if st.button("作业解答"):
            st.experimental_set_query_params(page="homework")
        if st.button("看医生"):
            st.experimental_set_query_params(page="doctor")


def login_page():
        st.title("Login")
        # Add login form
        with st.form(key="login_form"):
            username = st.text_input("用户名")
            password = st.text_input("密码", type="password")
            submit = st.form_submit_button("登录")

            # Verify user credentials and set session state
            if submit:
                st.warning(session_state["logged_in"])
                # return
                if username == "admin" and password == "admin":
                    session_state["logged_in"] = True
                    st.experimental_set_query_params(page="home")



def resume_page():
        st.title("个人简历")
        st.write("在这里输入您的个人信息、教育经历、工作经历、个人优势/技能等信息，并点击 '生成简历'。")

        # Add resume form
        with st.form(key="resume_form"):
            personal_info = st.text_area("个人信息")
            education = st.text_area("教育经历")
            work_experience = st.text_area("工作经历")
            skills = st.text_area("个人优势/技能")
            submit = st.form_submit_button("生成简历")

            # Generate resume using OpenAI API and show it as Markdown


            if submit:
                prompt = f"Generate a resume based on the following information:\n\n{personal_info}\n\n{education}\n\n{work_experience}\n\n{skills}\n\n"
                response = openai.Completion.create(
                    engine="text-davinci-002",
                    prompt=prompt,
                    max_tokens=1024,
                    n=1,
                    stop=None,
                    temperature=0.5,
                )
                resume = response.choices[0].text
                st.write(markdown.markdown(resume))
                st.markdown(f"[Download Markdown](data:text/plain,{resume})", unsafe_allow_html=True)

# def code_page():
# def bug_page():
# def homework_page():
# def doctor_page():

# Define app
def app():

    page = st.experimental_get_query_params().get("page")
    # not logged in
    if not session_state["logged_in"] and page != "login":
        st.experimental_set_query_params(page="login")
        # login_page()
    elif session_state["logged_in"] and page == "resume":
        st.experimental_set_query_params(page="home")
        # resume_page()
    else:
        home_page()

    if page == "login":
        login_page()
    elif page == "resume":
        resume_page()
    # elif page == "code":
    #     code_page()
    # elif page == "bug":
    #     bug_page()
    # elif page == "homework":
    #     homework_page()
    # elif page == "doctor":
    #     doctor_page()
    else:
        home_page()



if __name__ == '__main__':

    app()

