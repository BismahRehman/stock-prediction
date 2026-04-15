FROM python:3.13.7-slim

# system dependencies (needed for uv install + HTTPS)
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# make uv available globally
ENV PATH="/root/.local/bin:$PATH"

# work directory
WORKDIR /app

# copy dependency files first (important for caching)
COPY pyproject.toml uv.lock ./

# install dependencies using uv
RUN uv sync --frozen

# copy application code
COPY . .

# expose FastAPI port
EXPOSE 8000

# run app
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]