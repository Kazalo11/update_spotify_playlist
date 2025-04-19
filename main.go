package main

import (
	"fmt"
	"net/http"

	"github.com/aws/aws-lambda-go/events"
	"github.com/aws/aws-lambda-go/lambda"
	spotifyauth "github.com/zmb3/spotify/v2/auth"
)

var (
	success_response = events.LambdaFunctionURLResponse{
		Body:       "Successfully updated files",
		StatusCode: http.StatusCreated,
	}
	not_modified_response = events.LambdaFunctionURLResponse{
		Body:       "Not modified",
		StatusCode: http.StatusNotModified,
	}
	redirectURL = "http://localhost:8080/callback"
	state       = "abc123"
)

func main() {
	lambda.Start(handler)
}

func handler(request events.LambdaFunctionURLRequest) (events.LambdaFunctionURLResponse, error) {
	auth := spotifyauth.New(spotifyauth.WithRedirectURL(redirectURL), spotifyauth.WithScopes(spotifyauth.ScopeUserLibraryRead, spotifyauth.ScopePlaylistModifyPrivate, spotifyauth.ScopePlaylistModifyPublic))
	url := auth.AuthURL(state)
	fmt.Println(url)

	return success_response, nil
}
