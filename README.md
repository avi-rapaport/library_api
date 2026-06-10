# library_api

## system description
The system is built on an API server built using FastAPI that connects to a MySQL database. 
The system creates tables for managing book data, library members, and report data.

## docker
docker run --name library -e MYSQL_ROOT_PASSWORD=root -p 3306:3306 -d dhi.io/mysql:8

## folder structure
```
library-api/
├── main.py
├── database/
│   ├── db_connection.py
│   ├── book_db.py
│   └── member_db.py
├── routes/
│   ├── book_routes.py
│   ├── member_routes.py
│   └── report_routes.py
├── logs/
│   ├── app.log
│   └── logger_config.py
├── README.md
├── requirements.txt
└── .gitignore
```

## table structure

### books
id: int
title: varchar
author: varchar
genre: enum(Fiction | Non-Fiction | Science | History | Other)
is_available: boolean
borrowed_by_member_id: int | null

### members
id: int
name: varchar
email: unique
is_active: boolean
total_borrows: int  #incremented by 1 on each borrow

## system rules
1. When creating a book, the system automatically adds two default columns: is_available=TRUE, borrowed_by=NULL.

2. Genre must be Fiction / Non-Fiction / Science / History / Other - any other value returns an error 
This must be verified both when adding and updating

3. When creating a member, the system adds two deprecated columns: is_active=True, total_borrows=0

4. Email must be unique - if it already exists it returns an error.

5. Inactive member - is_active=False cannot borrow a book.

6. A book that is not available - is_available=False cannot be borrowed.

7. A member cannot hold more than 3 books at a time.

8. A book can only be returned if it is lent to the same friend who is returning it.

## API endpoints

### books
- 'POST /books'
- 'GET /books'
- 'GET /books/{id}'
- 'PUT /books/{id}'
- 'PUT /books/{id}/borrow/{member_id}'
- 'PUT /books/{id}/return/{member_id}'

### Members
- 'POST /members'
- 'GET /members'
- 'GET /members/{id}'
- `PUT /members/{id}'
- 'PUT /members/{id}/deactivate'
- 'PUT /members/{id}/activate'

### Reports
- 'GET /reports/summary'
- 'GET /reports/top-member'

## system flow
                client
                  |
                / | \
               /  |  \
              /   |   \
             /    |    \
        books   reports  members
        router  router   router
        \        /  \         /
         \      /    \       /
          \    /      \     /
          BookDb     MemberDb
            \            /
             \          /
              \        /
                  SQL

## running instructions
uvicorn main:app

