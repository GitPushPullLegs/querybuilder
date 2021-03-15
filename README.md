# Query Builder
A package to facilitate the building of dynamic SQL Server queries.

## Installation
`pip install git+https://github.com/GitPushPullLegs/querybuilder.git`

## Quick Demo
```python
import querybuilder

builder = querybuilder.QueryBuilder()
builder.select('P.first_name')
builder.select('OP.last_name')
builder.from_table('people P')
builder.inner_join('other_people OP')
builder.where('P.age >= 29')
print(builder.query)

>> """SELECT P.first_name, OP.last_name
      FROM people P
      INNER JOIN other_people OP ON OP.first_name = P.first_name
      WHERE P.age >= 29"""
```