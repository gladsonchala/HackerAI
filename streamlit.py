import streamlit as st
import logging

from hack import HackAI

class StreamlitApp:
    def __init__(self, hacker_ai):
        self.hacker_ai = hacker_ai

    def run(self):
        st.title("HackerAI Chatbot")
        st.markdown("This chatbot can generate responses based on the provided prompt.")

        # Prompt input
        prompt = st.text_area("Enter your question:", """e.g. Code python script...""")

        # Generate text button
        if st.button("Generate Text"):
            with st.spinner("Generating..."):
                response_text = self.hacker_ai.generate_text(prompt)
                if response_text is not None:
                    log_message = f"Response displayed successfully: {response_text}"
                    logging.info(log_message)
                    st.markdown(response_text)
                else:
                    st.error("Something is wrong. Please try again later.")
                    logging.error("Failed to generate text.")

if __name__ == "__main__":
    hacker_ai = HackAI()
    streamlit_app = StreamlitApp(hacker_ai)
    streamlit_app.run()


