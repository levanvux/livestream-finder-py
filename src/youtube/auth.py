import json
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

TOKEN_FILE = Path("token.json")
CLIENT_SECRET_FILE = Path("client_secret.json")


def get_youtube_client():
    creds = None

    try:
        import streamlit as st

        if "GOOGLE_TOKEN" in st.secrets:
            creds = Credentials.from_authorized_user_info(
                json.loads(st.secrets["GOOGLE_TOKEN"]),
                SCOPES,
            )
            is_streamlit = True
        else:
            is_streamlit = False

    except ImportError:
        is_streamlit = False

    if creds is None and TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(
            str(TOKEN_FILE),
            SCOPES,
        )

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        elif is_streamlit:
            raise RuntimeError(
                "GOOGLE_TOKEN is missing or invalid in Streamlit secrets."
            )

        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CLIENT_SECRET_FILE),
                SCOPES,
            )
            creds = flow.run_local_server(port=0)

            TOKEN_FILE.write_text(creds.to_json())

    return build(
        "youtube",
        "v3",
        credentials=creds,
    )
