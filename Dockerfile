FROM golang:1.24-alpine

WORKDIR /app

ARG SPOTIFY_ID
ARG SPOTIFY_SECRET

ENV SPOTIFY_ID $SPOTIFY_ID
ENV SPOTIFY_SECRET $SPOTIFY_SECRET

COPY go.mod go.sum ./

RUN go mod download

COPY . .

RUN go build -tags lambda.norpc -o bootstrap main.go 
EXPOSE 8080

CMD ["./bootstrap"]