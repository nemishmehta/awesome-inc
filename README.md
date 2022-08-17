# 🦾Exercise

Awesome Inc is proud to deliver and install high-quality products at customer's location. As part of the Analytics team, your current job is to help us with the following topics.

## 📈 Data Warehouse

We would like to report on the number of installations that the company is doing every month in order to see if the business is growing.

We would also like to see which product category brings us more revenues, and which region of the world is our best market.

### 👓 Requirements

* Design a dimensional model capable of answering those questions, and possibly more;
* Implement this dimensional model using `dbt`;
* Version your code;
* Create the associated Power BI report (bonus)

## 📃Data API

We would like to give access to Awesome Inc data using an API.

### 👓 Requirements

* Implement a Python REST or GraphQL API on top of Awesome Inc database;
* Test the API;
* Containerize the application;
* Version your code;
* Create an Helm chart to deploy the application on Kubernetes (bonus);
* Create a CI/CD pipeline (bonus)

# 🐱‍🏍 Getting started

The repository contains a `docker-compose` file that starts a Postgres database containing Awesome Inc data. It also starts PgAdmin in order to manage the Postgres instance. By default, the interface is accesible at `http://localhost:8080`.

