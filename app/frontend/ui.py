import streamlit as st
import requests

from app.config.settings import settings
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

st.set_page_config(
    page_title="Multi AI Agent",
    layout="wide"
)

st.title("🤖 Multi AI Agent")

selected_model = st.selectbox(
    "Select Model",
    settings.ALLOWED_MODEL_NAMES
)

user_query = st.text_area(
    "Enter your query",
    height=180,
    placeholder="Ask anything..."
)

API_URL = "http://127.0.0.1:9999/chat"

if st.button("Ask Agent"):

    if not user_query.strip():
        st.warning("Please enter a query.")
        st.stop()

    payload = {
        "model_name": selected_model,
        "user_query": user_query
    }

    try:

        logger.info("Sending request to backend...")

        response = requests.post(
            API_URL,
            json=payload,
            timeout=120
        )

        if response.status_code != 200:
            st.error(response.text)
            st.stop()

        data = response.json()

        # Final Response
        st.subheader("💬 Final Response")
        st.write(data.get("answer", ""))

        # Supervisor Details
        routing = data.get("routing", {})

        with st.expander("🧠 Supervisor Decision"):

            st.write("**Selected Agents**")
            st.write(routing.get("agents", []))

            st.write("**Reason**")
            st.write(routing.get("reason", ""))

            st.write("**Confidence**")
            st.progress(float(routing.get("confidence", 0)))

        # Individual Agent Outputs
        outputs = data.get("agent_outputs", {})

        if outputs:

            st.subheader("⚙️ Agent Outputs")

            for agent, output in outputs.items():

                with st.expander(agent.capitalize()):

                    st.write(output)

    except Exception as e:

        logger.exception("Backend communication failed.")

        st.error(
            str(
                CustomException(
                    "Failed to communicate with backend",
                    error_detail=e
                )
            )
        )