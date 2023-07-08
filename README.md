<a name="readme-top"></a>

<!-- project shields -->
[![Watchers][watchers-shield]][watchers-url]
[![Stargazers][stars-shield]][stars-url]
[![License][license-shield]][license-url]


<!-- title -->
<br />
<div align="center">
    <h2>Music API</h2>
    <p>
        Discover artists, albums, and songs with our API!
    </p>
</div>

<!-- table of contents-->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation-with-pip">Installation with Pip</a></li>
        <li><a href="#installation-with-docker">Installation with Docker</a></li>
        <ul><li><a href="#configuration-variables">Configuration Variables</a></li></ul>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <ul><li><a href="#endpoints">Endpoints</a></li></ul>
    <li><a href="#usage-example">Usage Example</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<!-- about the project-->
## About the project

This API allows you to search for information about artists, albums, and songs. You can retrieve details such as the name, duration, description, and more for these entities. Additionally, this API provides a user authentication system using JWT for authorization.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

This is a web application built using Flask, Python, and SQLAlchemy. By default, the application is configured to use PostgreSQL as the database backend. However, if you prefer to use a different database, you can easily switch to SQLite by updating the configuration settings in the config.py file.

* [![Python][python-shield]][python-url]
* [![Flask][flask-shield]][flask-url]
* [![PostgreSQL][postgresql-shield]][postgresql-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started

### Prerequisites

Before you start, you'll need to make sure you have the following installed:

* Python (3.11 or higher)
* PostgreSQL (10 or higher)
* Pip
* Docker and Docker Compose (optional)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Installation with Pip

1. Clone the repository and change to the clones directory:

   ```shell
   git clone https://github.com/SSleimann/music-flask-api.git
   cd music-flask-api
   ```

2. Create a virtual enviroment for the project

   ```shell
   python -m venv venv
   ```

3. Activate the virtual enviroment:

   ```shell
   source venv/bin/activate
   ```

4. Install the project and its dependencies using pip:

   ```shell
   pip install .
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Installation with Docker

1. Clone the repository and change to the clones directory:

   ```shell
   git clone https://github.com/SSleimann/music-flask-api.git
   cd music-flask-api
   ```

2. Run the following command to build and run the containers:

   ```shell
   docker compose up -d
   ```

3. You can stop the containers at any time with the following command:

   ```shell
   docker compose down
   ```

#### Configuration Variables

The following variables can be configured. These configuration variables are located in the `.envs/.local` dir and the `docker-compose.yml` file.

| Variable | Description |
| --- | --- |
| `SECRET_KEY` | The secret key of the application. |
| `JWT_SECRET_KEY` | The secret key used to sign JWT tokens. |
| `DATABASE_URL` | The URL of the PostgreSQL database used by the application. |
| `POSTGRES_USER` | The username used to authenticate with the PostgreSQL database. |
| `POSTGRES_PASSWORD` | The password used to authenticate with the PostgreSQL database. |
| `POSTGRES_DB` | The name of the PostgreSQL database used by the application. |

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Usage

To use this API, make an HTTP request to one of the endpoints using the appropriate HTTP method.

### Endpoints

| Method | Endpoint | Description | Request body | Request Header
| --- | --- | --- | --- | --- |
| POST   | `user/register` | Register a new user. | `username`, `email`, `password`, `password_confirmation` | `Content-Type: application/json` |
| POST   | `user/login` | Logs a user. | `email`, `password` | `Content-Type: application/json` |
| GET   | `user/profile` | Retrieves the user information. | `N/A` | `Authorization: Bearer <jwt_access_token>` |
| GET   | `music/artist`,  `music/artist/<id>` | Retrieves artist information. | `N/A` | `Authorization: Bearer <jwt_access_token>` |
| POST, PUT, PATCH   | `music/artist`, `music/artist/<id>` | Create/update a artist. (Need to be admin) | `name`, `description`, `year_of_birth` | `Authorization: Bearer <jwt_access_token>` |
| GET   | `music/album`, `music/album/<id>` | Retrieves album information. | `N/A` | `Authorization: Bearer <jwt_access_token>` |
| POST, PUT, PATCH   | `music/album`, `music/album/<id>` | Create/update a album. (Need to be admin) |  `name`, `artist_id`, `description`, `release_date` | `Authorization: Bearer <jwt_access_token>` |
| GET   | `music/songs`, `music/song/<id>` | Retrieves song information. | `N/A` | `Authorization: Bearer <jwt_access_token>` |
| POST, PUT | `music/song`, `music/song/<id>` | Create/update a song. (Need to be admin) | `name`, `artist_id`, `album_id`, `duration`, `release_date` | `Authorization: Bearer <jwt_access_token>` |
| DELETE | `music/artist/<id>`, `music/album/<id>`, `music/song/<id>` | Delete a artist/song/album. (Need to be admin) | `N/A` | `Authorization: Bearer <jwt_access_token>` |

#### Pagination

| Endpoint | Description |
| --- | --- |
| `music/artist?page=<int>` | Return 10 artists |
| `music/album?page=<int>` | Return 10 albums |
| `music/song?page=<int>` | Return 10 songs |

#### Search

| Endpoint | Description |
| --- | --- |
| `music/artist?search=<string>` | Search Artist records for search term in name field of Artist and related Song or Album |
| `music/album?search=<string>` | Search Album records for search term in name field of Album and related Artist or Song |
| `music/song?search=<string>` | Search Song records for search term in name field of Song, related Album or Artist tables. |

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Usage Example

### Create a user admin

Run `flask shell` in the console. Then execute this:

```python
from musicapi.models import User
from musicapi.app import db

user = User(username='adminuser', email='adminuser@mail.com')
user.set_password('password')
user.set_admin()

db.session.add(user)
db.session.commit()
```

### Login a user

Request

```http
POST {{API}}/user/login
content-type: application/json

{
    "email": "email@email.com",
    "password": "12345678"
}
```

Response

```json
{
    "token": "<jwt_access_token>"
}
```

### Creating a Artist

Request

```http
POST {{API}}/music/artist
content-type: application/json
Authorization: Bearer <jwt_access_token>

{
    "name": "artist",
    "description": "hello",
    "year_of_birth": "1999-01-24"
}
```

Response

```json
{
  "message": "Artist have been created successfully!",
  "artist": {
    "name": "artist",
    "description": "hello",
    "year_of_birth": "1999-01-24",
    "num_albums": 0,
    "num_songs": 0,
    "total_duration": 0
  }
}
```

### Find Artist by Name and Paginate

Request

```http
GET {{API}}/music/artist?search=weeknd&page=1
content-type: application/json
Authorization: Bearer <jwt_access_token>
```

Response

```json
[
  {
    "name": "the weeknd",
    "description": "hello",
    "year_of_birth": "1999-01-24",
    "num_albums": 5,
    "num_songs": 6,
    "total_duration": 12121212
  },
  {
    "name": "2 weeknd",
    "description": "hello2",
    "year_of_birth": "1939-01-24",
    "num_albums": 1,
    "num_songs": 10,
    "total_duration": 150
  }
  ... (only 10 results per page)
]
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## License

This project is licensed under the GNU General Public License (GPL) version 3. See the [LICENSE](LICENSE) file for more details.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contact

If you have any questions, comments, or issues related to the project, feel free to contact me. [Sleiman Orocua.](mailto:sleimanjose23@hotmail.com?subject=[Github]%20music%20flask%20api)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- badges -->
[stars-shield]: https://img.shields.io/github/stars/SSleimann/music-flask-api?style=for-the-badge&logo=github
[watchers-shield]: https://img.shields.io/github/watchers/SSleimann/music-flask-api?style=for-the-badge&logo=github
[license-shield]: https://img.shields.io/github/license/SSleimann/music-flask-api?style=for-the-badge&logo=github
[python-shield]: https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue
[postgresql-shield]: https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white
[flask-shield]: https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white

<!-- urls -->
[watchers-url]: https://github.com/SSleimann/music-flask-api/watchers
[stars-url]: https://github.com/SSleimann/music-flask-api/stargazers
[license-url]: https://www.gnu.org/licenses/gpl-3.0
[python-url]: https://www.python.org/
[flask-url]: https://flask.palletsprojects.com/en/2.3.x/
[postgresql-url]: https://www.postgresql.org/
