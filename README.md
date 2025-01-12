# jamesfishwick.com (fork of simonwillisonblog)

[![GitHub Actions](https://github.com/simonw/simonwillisonblog/actions/workflows/ci.yml/badge.svg)](https://github.com/simonw/simonwillisonblog/actions)

The code that runs my weblog, <https://jamesfishwick.com/>

## Search Engine

This blog includes a built-in search engine. Here's how it works:

1. The search functionality is implemented in the `search` function in `blog/search.py`.
2. It uses a combination of full-text search and tag-based filtering.
3. The search index is built and updated automatically when new content is added to the blog.
4. Users can search for content using keywords, which are matched against the full text of blog entries and blogmarks.
5. The search results are ranked based on relevance and can be further filtered by tags.
6. The search interface is integrated into the blog's user interface, allowing for a seamless user experience.

For more details on the implementation, refer to the `search` function in `blog/search.py`.

### Local Development

Follow these steps to set up and run the project locally:

1. **Clone the Repository**  

   ```bash
   git clone https://github.com/your-repo.git
   cd your-repo
   ```

2. **Set Up Python Environment**  
   - Ensure you have Python 3.12 or the required version installed.  
   - Create a virtual environment and activate it:

     ```bash
     python -m venv env
     source env/bin/activate  # On Windows, use `env\Scripts\activate`
     ```

3. **Install Dependencies**  

   ```bash
   pip install -r requirements.txt
   ```

4. **Database Setup with Docker**  
   Use the provided script `setup_database.sh` to set up PostgreSQL using Docker. This script will:
   - Check if Docker is installed
   - Start a PostgreSQL container (or create one if it doesn't exist)
   - Create a database named `test_db`
   - Export the `DATABASE_URL` environment variable

   To run the script:

   ```bash
   chmod +x setup_database.sh
   ./setup_database.sh
   ```

   If the script has already been run but the container is stopped, you can restart the container manually:

   ```bash
   docker start postgres-dev
   ```

   To confirm that the container is running:

   ```bash
   docker ps | grep postgres-dev
   ```

   If the container is not running, ensure it is started before continuing.

5. **Apply Migrations**  

   ```bash
   python manage.py migrate
   ```

6. **Run the Development Server**  

   ```bash
   python manage.py runserver
   ```

7. **Static Files (Optional)**  
   If required, collect static files:

   ```bash
   python manage.py collectstatic --noinput
   ```

## Local Development Access

### Frontend (Blog)

The blog will be available at:

- <http://localhost:3000>

### Backend API

The backend API can be accessed at:

- <http://localhost:8000>

### API Documentation

View the interactive API documentation at:

- <http://localhost:8000/docs>
- <http://localhost:8000/redoc>

### Testing the API

You can test the API endpoints using:

- cURL commands in your terminal
- The interactive Swagger UI at <http://localhost:8000/docs>
- API testing tools like Postman or Insomnia using the base URL <http://localhost:8000>
