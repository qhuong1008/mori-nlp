## Prerequisites:

Python 3.11

## Install dependencies:

```
pip install -r requirements.txt
```

## Before run project:

Create the virtual environment:

```
python -m venv venv
```

Install dependencies:

```
pip install -r requirements.txt
```

## Run project:

```
uvicorn main:app --reload
```

## Test API:

GET request: http://127.0.0.1:8000/nlp/comment/hi

POST request: http://127.0.0.1:8000/nlp/comment/classify

payload:

```
{
  "text":"bạn thật xấu xí hahahahaha"
}
```
