FROM python:alpine

WORKDIR /usr/src/app

COPY ./ /usr/src/app/

RUN apk add --no-cache gcc musl-dev libffi-dev && \
    pip install --no-cache-dir -r requirements.txt



ENV DATABASE_URL=mongodb://localhost:27017/YOUDB
ENV ENTERPRISE=YOUENTERPRISE


EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]