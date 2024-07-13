FROM python:3.11.6

WORKDIR /back

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5001

ENV FLASK_APP=back/app.py
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["python", "-m", "flask", "run", "--port=5001"]
