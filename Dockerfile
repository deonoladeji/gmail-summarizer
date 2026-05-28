# Start with official Python
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir streamlit openai google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client python-dotenv
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]