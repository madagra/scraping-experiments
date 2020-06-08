# Yahoo Finance Scraper

Simple python scraper to extract stock information from the Yahoo Finance website. This is used as base exercise
for a course in Test Driven Development.

## Outline of the TDD course

* Test-driven development introduction
* Software development lifecycle
	* problem definition
	* high-level requirements
* Phases of TDD:
	* design: break-down each requirement in different function
	* write function signatures
	* write one or more tests for each function
	* refactor the function
	* run the tests
	* if fail, go back to refactoring
* In-depth topics to cover during the course:
	* how to design and test HTTP request functions
	* how to design and test SDK interface functions

## High-level Requirements

* requesting valid HTML from Yahoo Finance
* deserialize HTML structure
* extract full name of the company, symbol, close value and EPS value
* return all results as a dictionary or equivalent data structure
