FROM tensorflow/tensorflow:nightly

# install Python modules needed by the Python app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r ./requirements.txt

# copy files required for the app to run
COPY app.py ./
COPY hate_speech_model ./hate_speech_model
COPY templates/index.html ./templates/

# tell the port number the container should expose
EXPOSE 5000

# run the application
CMD ["flask", "run", "--host", "0.0.0.0"]
