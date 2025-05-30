# app.py
import streamlit as st
import requests
import os
from dotenv import load_dotenv
from typing import Dict, List
import datetime
import pandas as pd
import altair as alt

# Load environment variables
load_dotenv()
API_URL = os.getenv("API_URL", "http://localhost:8000")

# Rerun helper for Streamlit
try:
    from streamlit.runtime.scriptrunner import RerunException
except ImportError:
    class RerunException(Exception):
        def __init__(self, rerun_data=None):
            super().__init__()
            self.rerun_data = rerun_data

def rerun():
    raise RerunException(None)

# API wrappers
def fetch_projects():
    r = requests.get(f"{API_URL}/projects/")
    return r.json() if r.ok else []

def fetch_folders(project_id: str):
    r = requests.get(f"{API_URL}/projects/{project_id}/folders/")
    return r.json() if r.ok else []

def create_folder_api(project_id: str, data: Dict):
    requests.post(f"{API_URL}/projects/{project_id}/folders/", json=data)

def fetch_pages(folder_id: str):
    r = requests.get(f"{API_URL}/folders/{folder_id}/pages/")
    return r.json() if r.ok else []

def create_page_api(folder_id: str, data: Dict):
    requests.post(f"{API_URL}/folders/{folder_id}/pages/", json=data)

def get_page_api(page_id: str):
    r = requests.get(f"{API_URL}/pages/{page_id}")
    return r.json() if r.ok else {}

# Sidebar components
def folder_sidebar(project: Dict):
    st.sidebar.markdown("### 📁 Folders & Pages")
    folders = fetch_folders(project["id"])
    names = ["<root>"] + [f["name"] for f in folders]
    sel = st.sidebar.selectbox("Folder", names)
    fid = None if sel == "<root>" else next(f["id"] for f in folders if f["name"] == sel)

    new_name = st.sidebar.text_input("New folder name", key="new_folder")
    if st.sidebar.button("➕ Add Folder"):
        create_folder_api(project["id"], {"name": new_name})
        rerun()
    st.sidebar.markdown("---")

    pages = fetch_pages(fid) if fid else []
    titles = [p["title"] for p in pages]
    sel_page = st.sidebar.selectbox("Pages", titles + ["<new page>"])
    if sel_page == "<new page>":
        title = st.sidebar.text_input("Page Title", key="page_title")
        content = st.sidebar.text_area("Content (Markdown)", key="page_content")
        if st.sidebar.button("💾 Save Page"):
            create_page_api(fid, {"title": title, "content": content})
            rerun()
    else:
        pid = next(p["id"] for p in pages if p["title"] == sel_page)
        page = get_page_api(pid)
        st.sidebar.markdown(f"#### {page['title']}")
        st.sidebar.markdown(page['content'])

# Main sidebar
def sidebar():
    st.sidebar.title("🧠 NeuroProject Manager")
    projects = fetch_projects()
    titles = [p["title"] for p in projects]
    sel = st.sidebar.selectbox("Select Project", ["Create New"] + titles)
    if sel == "Create New":
        title = st.sidebar.text_input("Project Title")
        desc  = st.sidebar.text_area("Description")
        if st.sidebar.button("➕ Create Project"):
            requests.post(f"{API_URL}/projects/", json={"title": title, "description": desc})
            rerun()
    else:
        proj = next(p for p in projects if p["title"] == sel)
        st.session_state.current_project = proj
        if st.sidebar.button("🔄 Refresh Projects"):
            rerun()
        folder_sidebar(proj)

# Main app function
def main():
    sidebar()
    proj = st.session_state.get("current_project")
    if proj:
        st.title(f"Project: {proj['title']}")
        st.write(proj.get("description", ""))
        # Your existing project view (tasks, charts, etc.)
    else:
        st.title("Welcome to NeuroProject Manager")
        st.write("AI-powered project management for AuDHD")

if __name__ == "__main__":
    main()
