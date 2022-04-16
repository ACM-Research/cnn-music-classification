# Getting Started
First make sure Docker is installed and properly set up on your system. Note: Not sure if this will work on non-Debian-based Linux (it uses apt-get but Docker may handle this?)

1. Navigate to the `website` directory. Build the Docker image: `docker build --tag python-docker .`. 
2. Run a Docker container: `docker run python-docker`
3. Use the link in the console to go to the website.

This uses a development server that is not suitable for deployment. In a real deployment we would use Gunicorn and NGINX.

When deploying on Heroku, for example, response times are limited to 30 seconds which can be longer than the time to upload/download the file, process it, and use the model to predict it. In this case, retry using the same file/link until it works (yes it's scuffed).