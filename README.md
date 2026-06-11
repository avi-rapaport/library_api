# library_api

## system description
The system is built on an API server built using FastAPI that connects to a MySQL database. 
The system creates tables for managing book data, library members, and report data.

## docker
docker run --name library -e MYSQL_ROOT_PASSWORD=<> -e MYSQL_DATABASE=library_db -p 3306:3306 -d dhi.io/mysql:8

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
- 'GET /reports/books-by-genre'

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

### borrow flow: 
When borrowing a book, the member enters the identification number of the desired book into the system, as well as his/her ID card. The system checks whether the book with that identification number exists and whether it is available for borrowing. And whether that member exists in the system and is active. If so, it transfers the book to him/her and makes it unavailable. It increases the total number of books that the member borrowed and also enters that member's identification number for that book.

### return flow: 
When returning a book, the member enters his ID card into the system as well as the ID card of the returned book, and the system checks whether that member exists and is active and whether that book is indeed loaned to him, and if so, takes the book from him and makes the book available.


## running instructions
uvicorn main:app

