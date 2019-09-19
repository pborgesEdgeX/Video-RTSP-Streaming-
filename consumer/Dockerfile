FROM ufoym/deepo:cpu

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . /app

# Expose Ports for TensorBoard (6006), Ipython (8888)
EXPOSE 6006 8888 5000

WORKDIR "/app"
CMD ["python", "main.py"]
