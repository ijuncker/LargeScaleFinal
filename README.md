# Scalica Scourer 

Whenever, a user posts a message, it will be sent to our service for indexing. Our service will tokenize the message and create a search index. OUr service will reply to search queries with a pointer to the relevant posts. It also scores and displays sorted results based on TF-IDF scores.

## Scalica

The only change to Scalica that was made was the addition of our gRPC code. 

## TextSearch

The TextSearch directory contains all our code for gRPC, building a search indexing, scoring, sorting, and our web app. 

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds


## Authors

* **Edward Paik** 
* **Ian Junker** 
* **Robert Lei** 
* **Sadman Fahmid** 
