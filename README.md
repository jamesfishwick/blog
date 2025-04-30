# Minimal Wave Blog

A Django-based personal blog inspired by Simon Willison's website (simonwillison.net), featuring a dark mode minimal wave aesthetic.

## Features

* **Blog Posts:** Create and manage blog posts with title, summary, body, publication date, and draft/live status.
* **Link Blog (Blogmarks):** Share and comment on external links, similar to Simon Willison's "blogmarks".
* **TIL (Today I Learned):** A dedicated section for short-form content, organized by topic.
* **Tagging:** Organize all content (posts, links, TILs) using tags.
* **Markdown Support:** Write content using Markdown with syntax highlighting.
* **Search:** Full-text search across blog posts, links, and TILs.
* **Archives:** Browse content by year and month.
* **Atom Feeds:** Separate Atom feeds for the main blog and the TIL section.
* **Social Media Cards:** Automatic generation of social media card metadata (Open Graph and Twitter Cards) for enhanced link sharing.
* **Dark Mode:** A visually appealing dark mode theme with minimal wave aesthetics (neon text, grid patterns).
* **Responsive Design:** Adapts to different screen sizes (desktop, mobile).
* **Reading Time:** Estimated reading time displayed for blog posts and TILs.
* **Related Posts:** Suggests related blog posts based on shared tags.
* **Pagination:** Paginated index and archive pages.

## Local Development Setup

There are two ways to run the blog locally: using a Python virtual environment or using Docker.

### Option 1: Using Python Virtual Environment (venv)

1. **Clone the repository:**

    ```bash
    git clone <repository-url>
    cd fishwick-blog
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Apply database migrations:**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. **Create a superuser account:**

    ```bash
    python manage.py createsuperuser
    ```

    (Follow the prompts to set up your admin username and password)

6. **Run the development server:**

    ```bash
    python manage.py runserver
    ```

7. **Access the blog:** Open your web browser and go to `http://127.0.0.1:8000/`
8. **Access the admin interface:** Go to `http://127.0.0.1:8000/admin/` and log in with your superuser credentials to create content.

### Option 2: Using Docker

1. **Ensure Docker is installed and running.**
2. **Clone the repository:**

    ```bash
    git clone <repository-url>
    cd fishwick-blog
    ```

3. **Build the Docker image:**

    ```bash
    docker build -t fishwick-blog .
    ```

4. **Run the Docker container:**

    ```bash
    docker run -p 8000:8000 --name fishwick-blog-container fishwick-blog
    ```

    *Note: This runs the container in the foreground. Use `-d` for detached mode.*

5. **Apply database migrations and create superuser (first time only):**
    * Open another terminal window.
    * Execute the following commands inside the running container:

        ```bash
        docker exec -it fishwick-blog-container python manage.py makemigrations
        docker exec -it fishwick-blog-container python manage.py migrate
        docker exec -it fishwick-blog-container python manage.py createsuperuser
        ```

        (Follow the prompts to set up your admin username and password)

6. **Access the blog:** Open your web browser and go to `http://localhost:8000/` or `http://127.0.0.1:8000/`
7. **Access the admin interface:** Go to `http://localhost:8000/admin/` and log in with your superuser credentials.

8. **To stop the container (if running in detached mode):**

    ```bash
    docker stop fishwick-blog-container
    ```

9. **To remove the container:**

    ```bash
    docker rm fishwick-blog-container
    ```

## Deployment

This project is configured for deployment to Azure App Service. See the `azure_deployment_guide.md` file for detailed instructions.

## Project Structure

* `minimalwave_blog/`: Main Django project directory.
  * `settings/`: Contains development and production settings.
  * `static/`: Static files (CSS, images).
  * `templates/`: Base HTML templates.
* `blog/`: Django app for core blog posts and blogmarks.
* `til/`: Django app for the "Today I Learned" section.
* `manage.py`: Django management script.
* `requirements.txt`: Python dependencies.
* `Dockerfile`: For building the Docker image.
* `azure_deployment_guide.md`: Instructions for Azure deployment.
* `README.md`: This file.
