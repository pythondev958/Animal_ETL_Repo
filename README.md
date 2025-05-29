# Animal ETL Pipeline

This project implements an ETL (Extract Transform Load) pipeline that interacts with a paginated animal API It retrieves animal data transforms specific fields and posts the data back in batches to a target endpoint The project is designed to handle server-side latency and transient errors gracefully

## Features

Fetches animal summaries and full details using asynchronous HTTP requests

Transforms data to conform to required schema

Converts the friends field from a comma-delimited string to a list

Converts the born_at field from a millisecond timestamp to an ISO8601 UTC string

Posts transformed data in batches of up to 100 records

Includes error handling and retry logic for intermittent server issues

## Project Structure

src/

main.py — Entry point that coordinates fetching transforming and posting animal data

api.py — Contains asynchronous functions for making GET and POST requests to the API

transform.py — Handles transformation logic for animal records

utils.py — Reserved for reusable helper functions if needed

__init__.py — Package initializer

tests/

test_etl.py — Unit tests for transformation logic using unittest

.flake8 — Flake8 configuration file for linting

env.env — Environment variable file for API base URL

requirements.txt — List of required Python packages

## Getting Started

## Prerequisites

Python 3.8 or higher

Docker (for running the provided API container)

A modern Python environment manager like venv or virtualenv

## Setup

Clone the repository
git clone <your-repo-url>
cd <your-repo-folder>
Create and activate a virtual environment

python -m venv venv  
source venv/bin/activate   # On Windows use venv\Scripts\activate  

## Install dependencies

pip install -r requirements.txt  
Start the API server using Docker

docker load -i lp-programming-challenge-1-1625758668.tar.gz  
docker run --rm -p 3123:3123 -ti lp-programming-challenge-1  
Verify the server is running by visiting http://localhost:3123/docs in your browser

Running the ETL Script
Ensure the environment variable API_BASE_URL is set in env.env or in your shell

Then run 

python -m src.main  

## Running Tests

python -m unittest discover tests  

## Design Notes

Uses aiohttp for efficient asynchronous HTTP communication

Includes exponential backoff for retryable errors like 500 502 503 and 504

Uses batch size of 100 for posting as per API constraints

The code is modular and testable with unit tests covering the core transformation logic

# Linting
To run flake8 for code quality checks

## Environment Variables
Configure environment variables in env.env

API_BASE_URL — Base URL of the animal API default is http://localhost:3123

## Author/Contact Details

Thank you for the Code Review. If you have any query, feedback or suggestion then please contact me on Pythondev958@Gmail.com.

## Best Regards
