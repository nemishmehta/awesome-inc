FROM python:3.12

# Create app directory
WORKDIR /app

# Copy environment variables
COPY .env .

# Install app dependencies
COPY requirements.lock ./

# Issue: https://github.com/astral-sh/rye/discussions/239#discussioncomment-6032595
RUN sed '/^-e/d' requirements.lock > requirements.txt
RUN PYTHONDONTWRITEBYTECODE=1 pip install --no-cache-dir -r requirements.txt

# Bundle app source
COPY src /app

# Expose the port the app runs on
EXPOSE 80

CMD ["fastapi", "run", "awesome_inc/api/main.py", "--port", "80"]