FROM python:3.10.8-bullseye

WORKDIR /opt

RUN apt-get update && apt-get upgrade -y
RUN pip install --no-cache -U pip && pip install poetry==1.7.0
# Virtual ENVs are created in the project directory.
RUN poetry config virtualenvs.in-project true
ENV PATH="${PATH}:/opt/.venv/bin"

# First copy & install requirements to speed up the build process in case only the code changes.
COPY ["./pyproject.toml", "./poetry.lock", "README.md", "./"]
# Copy the rest of the files.
COPY ["./", "./"]

RUN poetry install

# Entrypoint
CMD ["poetry", "run", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
