# WilliamOtto_T2A2

## Index  
- [R1 - Identification of the problem you are trying to solve by building this particular app](#r1)  
- [R2 - Why is it a problem that needs solving](#r2)  
- [R3 - Why have you chosen this database system. What are the drawbacks compared to others?](#r3)  
- [R4 - Identify and discuss the key functionalities and benefits of an ORM](#r4)  
- [R5 - Document all endpoints for your API](#r5)
- [R6 - Make an ERD for the app](#r6)
- [R7 - Detail any third party services that your app will use](#r7)
- [R8 - Describe your projects models in terms of the relationships they have with each other](#r8)
- [R9 - Discuss the database relations to be implemented in your application](#r9)
- [R10 - Describe the way tasks are allocated and tracked in your project](#r10)

# R1
The purpose of this project is to provide people a way to catalogue their person vinyl collections. Users can add friends to see what they have in their collections, comment/like on these posts, and access a database of artists in the catalogue. The users will be able to search by artist, genre or album.

# R2
As vinyl collections are purely physical, for some people, there is a desire to be able to catalogue their vinyl collections and share it with others, making it a more social experience.

# R3
My database system of choise is PostgreSQL. The main reasons for using PostgreSQL are as follows:

Pros:

- Open sourced.
- Free and accessible to everyone.
- Customisable with access to a multitude of plugins.
- Used by many large companies such as Apple and Cisco.
- Many resources for troubleshooting due to its popularity.

Cons:

- Being open sourced can cause problems with compatibility between different companies that use different plugins.
- Being a relational database system means that search queries are read sequentially which is detrimental to performance.

# R4
ORM is a technique that lets you manipulate data from a database using an object oriented programming language. Because the ORM is written in your language of choice, it circumnavigates the need for SQL queries. This means that the output can be more easily understood than if it were displayed as SQL. Consequently, it becomes more efficient in speed of production, and error mitigation.

ORM can improve security of the database. This is because any queries must go through the ORM, and, as a feature of the ORM technique is to provide authentication and validation whenever necessary, this provides an additional layer of security.

Accessing data in an ORM system is easier thanks to the fact that it is able to control how certain objects relate to different schema within a database. The CRUD operations form the basis for this communication between schema.

The disadvantages of an ORM system is that it is inherently slower than direct SQL queries as it has a higher level of abstraction. It also takes time to learn and understand how to implement it.

# R5

## Authorization Endpoints:
### auth/login
Method: POST
Identifier: Email
Authentication: Email and password
Token: JWT
Description: User can log, generating a JWT which is used for authentication.

### auth/register
Method: POST
Identifier: None
Authentication: None
Token: None
Description: Creates a new user.

### auth/users
Method: GET
Identifier: None
Authentication: None
Authorization: None
Token: None
Description: Shows a list of all users, with vinyls that have been posted.

### auth/users/id
Method: GET
Identifier: None
Authentication: None
Token: None
Description: displays all vinyls of one user including comments and likes.

## Vinyls Endpoints:
### vinyl/
Method: GET
Identifier: None
Authentication: None
Token: None
Description: Displays all vinyls with genre, album and user information for the user(s) that made the post.

### vinyl/
Method: POST
Identifier: None
Authentication: @jwt_required()
Token: JWT bearer token
Description: Creates a new vinyl.

### vinyl/
Method: PUT, PATCH
Identifier: None
Authentication: @jwt_required()
Token: JWT bearer token
Description: Updates a specific vinyl.

### vinyl/
Method: DELETE
Identifier: None
Authentication: @jwt_required()
Token: JWT bearer token
Description: Deletes a specific vinyl.

## Artist Endpoints:
### artist/
Method: GET
Identifier: None
Authentication: None
Token: None
Description: Get all artists.

### artist/<int:id>
Method: GET
Identifier: None
Authentication: None
Token: None
Description: Get one artist.

### artist/<int:id>
Method: PUT, PATCH
Identifier: None
Authentication: None
Token: None
Description: Update one artist.

### artist/<int:id>
Method: DELETE
Identifier: None
Authentication: @jwt_required()
Token: JWT bearer token
Description: Delete an artist.

## Comments Endpoints:
### comments/<int:vinyl_id>
Method: POST
Identifier: None
Authentication: None
Token: None
Description: Creates a comment.

### comments/<int:vinyl_id>
Method: DELETE
Identifier: None
Authentication: None
Token: None
Description: Deletes a comment.

## Likes Endpoints:
### likess/<int:vinyl_id>
Method: POST
Identifier: None
Authentication: None
Token: None
Description: Creates a like.

### likes/<int:vinyl_id>
Method: DELETE
Identifier: None
Authentication: None
Token: None
Description: Deletes a like.

# R6
![ERD](docs/Vinyl_ERD.png)

# R7
- Flask:
- Marshmallow:
- Flask-Marshmallow
- SQLAlchemy
- BCrypt
- Psycopg
- PostreSQL

# R8
## User Model:
### Attributes:
- id (integer, primary key)
- first_name (String(50), not empty)
- last_name (String(50))
- email (string, not empty, unique)
- password (string, not empty)
- is_admin (boolean, default to false)

### Relationships:
- Comments:
  - Comments model is linked to user model to allow sharing of attributes from comments to user entities.
  - Cascade delete means if a user is deleted, all related comments are deleted too.
- Likes:
  - Likes model is linked to user model to allow sharing of attributes from likes to user entities.
  - Cascade delete means if a user is deleted, all related comments are deleted too.
- Vinyls:
  - Vinyls model is linked to user model to allow sharing of attributes from vinyls to user entities.
  - Cascade delete means if a user is deleted, all related comments are deleted too.

### Validation:
- first_name:
  - The first name must be longer that 1 letter, and contain only letters.
- last_name:
  - The last name must be longer than 1 letter, and contain only letters.
- email:
  - The email address requires at least 2 characters and must be a valid email address.
- password:
  - The password requires at least one uppercase letter, at least one lowercase letter, at least one digit, at least one special character and be at least 8 characters long.

## Vinyl Model:
### Attributes:
- id (integer, primary key)
- date (date, not empty)

### Foreign Keys:
- user_id (integer, not empty) - using id attribute from user model.
- artist_id (integer, not empty) - using artist attribute from artist model.

### Relationships:
- artist:
  - artist model is linked to vinyl model to allow sharing of attributes from artists to vinyl entities.
- user:
  - user model is linked to vinyl model to allow sharing of attributes from users to vinyl entities.
- comments:
  - comments model is linked to vinyl model to allow sharing of attributes from comments to vinyl entities.
  - only include the 'user', 'message' and 'date' attributes.
- likes:
  - likes model is linked to vinyl model to allow sharing of attributes from likes to vinyl entities.
  - only include the 'like_author' and 'date' attributes.

## Artist Model:
### Attributes:
- id (integer, primary key)
- artist (string, not empty)
- album (string, not empty)
- genre (string, not empty)

### Relationships:
- Vinyl:
  - Vinyls model is linked to artist model to allow sharing of attributes from vinyls to artist entities.
  - Cascade delete means if an artist is deleted, all related vinyls are deleted too.

## Comment Model:
### Attributes:
- id (integer, primary key)
- message (text, not empty)
- date (date, not empty)

### Foreign Keys:
- vinyl_post_id (integer, not empty) - using id attribute from vinyls.
- comment_author (integer, not empty) - using id attribute from comments.

### Relationships:
- User:
  - user model is linked to comment model to allow sharing of attributes from users to comment entities.
  - include only the 'id' and 'name' attributes.
- Vinyl:
  - vinyl model is linked to comment model to allow sharing of attributes from vinyl to comment entities.
  - include only the 'id', 'artist' and 'album' attributes.

## Like Model:
### Attributes:
- id (integer, primary key)
- date (date, not empty)

### Foreign Keys:
- vinyl_post_id (integer, not empty) - using id attribute from vinyls.
- like_author (integer, not empty) - using id attribute from likes.

### Relationships:
- User:
  - user model is linked to comment model to allow sharing of attributes from users to comment entities.
  - include only the 'id' and 'name' attributes.
- Vinyl:
  - vinyl model is linked to comment model to allow sharing of attributes from vinyl to comment entities.
  - include only the 'id', 'artist' and 'album' attributes.

# R9
This API features 5 tables, one for users, vinyls, artists, comments and likes. 

# R10
I used Trello to allocate and track the tasks in this project.