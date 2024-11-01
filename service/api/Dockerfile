FROM python:3.8-slim
WORKDIR /api
COPY . /api/
RUN pip3 install --upgrade pip && pip install --no-cache-dir -r requirements.txt
EXPOSE 9898
CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]