FROM python:3.9-slim-buster AS base
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

FROM base AS compile-image
RUN apt-get -y update && apt-get install -y --no-install-recommends\
    build-essential \
    python3-dev \
    cmake \
    libssl-dev libffi-dev libsm6 libxext6 libxrender-dev
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt


FROM base as build-image

RUN apt-get -y update && apt-get install -y --no-install-recommends libpq-dev libsm6 libxext6 make


COPY --from=compile-image /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

WORKDIR /app
COPY . /app/
RUN python manage.py makemigrations
RUN python manage.py migrate


EXPOSE 8000



CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]