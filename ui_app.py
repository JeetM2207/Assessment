import streamlit as st
import requests

st.title("AI Educator: Agent Pipeline")

grade = st.number_input("Target Grade", min_value=1, max_value=12, value=4)
topic = st.text_input("Topic", "Types of Angles")

if st.button("Generate Content"):
    with st.spinner("Agents are working..."):
        response = requests.post(
            "http://0.0.0.0:8000/generate-lesson", 
            json={"grade": grade, "topic": topic}
        ).json()
        
        st.subheader("Step 1: Generator Output")
        st.write(response["initial_draft"]["explanation"])
        
        st.subheader("Step 2: Reviewer Feedback")
        status = response["reviewer_feedback"]["status"]
        color = "green" if status == "pass" else "red"
        st.markdown(f"Status: **:{color}[{status.upper()}]**")
        st.write(response["reviewer_feedback"]["feedback"])
        
        if status == "fail" or response["final_content"] != response["initial_draft"]:
            st.subheader("Step 3: Refined Content")
            st.write(response["final_content"]["explanation"])