# SQL Cheatsheet (Beginner-Friendly)

This file collects simple SQL patterns you will use in this project.

You can update it as you learn more.

## Basic SELECT

```sql
SELECT *
FROM books
LIMIT 10;
```

## Filtering Rows

```sql
SELECT title, average_rating
FROM books
WHERE average_rating >= 4.0;
```

## Aggregations and GROUP BY

```sql
SELECT author, AVG(average_rating) AS avg_rating
FROM books
GROUP BY author
ORDER BY avg_rating DESC;
```

## Counting Rows

```sql
SELECT publisher, COUNT(*) AS book_count
FROM books
GROUP BY publisher
ORDER BY book_count DESC;
```

## Simple JOIN (example)

```sql
SELECT b.title, a.name AS author_name
FROM books b
JOIN authors a ON b.author_id = a.id;
```

You do not have to use all of these patterns at once. Start with `SELECT`, `WHERE`, and `GROUP BY`, and then come back here when you need more.
