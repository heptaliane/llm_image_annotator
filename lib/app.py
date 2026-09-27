import streamlit as st

from .runner import Runner


def start(runner: Runner):
    st.set_page_config(page_title="Annotated Image Viewer", layout="wide")
    st.title("🏷️ Annotated Image Viewer")
