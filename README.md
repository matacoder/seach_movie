# Utelly REST API Client

<img src="https://raw.githubusercontent.com/matacoder/matacoder/main/utelly.png">

## Description

This is a REST Client to access Utelly search movies endpoint.

To use this functionality you need to set up `.env` file with `SERVER` and `TOKEN`

## How to obtain token and server endpoint?

Please contact Vincent Carbonie at [Utelly](https://utelly.com)

## Usage

```python
# create client object
client = RestClient(server=SERVER, token=TOKEN)
# get movie objects using search term (default = Star Trek)
movies = client.lookup_movies(term)
```