# test.py [You can upload data (uvicorn main:app --reload)--post]

from agent import add_document, ask_question

# Sample documents
docs = [
     {
        "title": "Resume",
        "content": "https://1drv.ms/b/c/88e7258f0d58e796/ET0IaVPIYwVBq9wqwvGkdWUBhOp7dHxhM_t9GOPgeakUjg?e=d8EZn8",
        "query": "give me aryan resume ?"
    },
    {
        "title": "College Name",
        "content": "My College Name is Indian Institue Of technology Madras",
        "query": "What youe College name ?"
    },
    {
        "title": "name",
        "content": "My name is Aryan Gautam.",
        "query": "What youe name ?"
    },
    {
        "title": "Batch_year and Current_year",
        "content": "My batch is 2023 and current year is 3rd.",
        "query": "What is your batch and current year?"
    },
    {
        "title": "Roll Number",
        "content": "My Roll Number is be23b025",
        "query": "What is your Roll Number?"
    }
]

# Add documents to FAISS
for doc in docs:
    add_document(doc['title'], doc['content'])

# Test queries
for doc in docs:
    answer = ask_question(doc['query'])
    print(f"Q: {doc['query']}\nA: {answer}\n{'-'*50}")
