FROM golang:1.24-alpine

WORKDIR /app

COPY go.mod go.sum ./

RUN go mod download

COPY . .

RUN go build -tags lambda.norpc -o bootstrap main.go
EXPOSE 8080

CMD ["./main"]