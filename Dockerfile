FROM python:3.13-slim
WORKDIR /app
COPY . /app/
RUN pip install -r requirements.txt
EXPOSE 8021
ENV PYTHONPATH="${PYTHONPATH}:/app/src"
CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8021", "--reload"]