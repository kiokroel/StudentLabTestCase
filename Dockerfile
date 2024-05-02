# 
FROM python:3.10

RUN mkdir /src

WORKDIR /src

#ENV PYTHONDONTWRITEBYTECODE 1
#ENV PYTHONUNBUFFERED 1

# 
COPY requirements.txt .

# 
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# 
COPY . .

RUN chmod a+x docker/*.sh


#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
