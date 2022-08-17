# 🦾Exercise

Awesome Inc is proud to deliver and install high-quality products at customer's locations. As part of the Analytics team, your current job is to help us with the following topics.

## 📃 API

We would like to develop an API that abstracts away the internals of the Awesome Inc database. This API will be used downstream by [Azure Data Factory](https://docs.microsoft.com/en-us/azure/data-factory/), the integration service used by the company.

### 👓 Requirements

* Implement a REST API on top of Awesome Inc database (e.g. using [FastAPI](https://fastapi.tiangolo.com/));
* Test the API (e.g. with [pytest](https://docs.pytest.org/en/7.1.x/));
* Containerize the application (e.g. using [Docker](https://docs.docker.com/));
* Version your code.

## 📈 Data Warehouse

We would like to give our business users the ability to answer questions such as:
* What is the number of installations that the company is doing every month?
* Which product category brings us more revenues?
* Which region of the world is our best market?

For that, we would like to create a data warehouse.

### 👓 Requirements

* Design a [dimensional](https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/) model capable of answering those questions, and possibly more;
* Implement this dimensional model (e.g. using [dbt](https://docs.getdbt.com/));
* Version your code.

# 🐱‍🏍 Getting started

The repository contains a `docker-compose` file that starts a Postgres database containing Awesome Inc data. It also starts PgAdmin in order to manage the Postgres instance. By default, the interface is accessible at `http://localhost:8080`.

# 📏 Expectations

This exercise is designed to evaluate both your software development and data engineering skills.

We expect you to demonstrate your ability to write high-quality code. By that we mean code that is easy to maintain, test, configure and deploy. We'll not only assess the end result but also ask you about the design decisions you made.

We also expect you to demonstrate your ability to transform data for analytics needs. The data model you provide must be dimensional and data quality checks must exist.

The tools mentioned in the exercises are part of our stack. We don't expect you to know or use them. If you prefer to use Spring Boot and Spark, well, go for it. We value know-how over tool mastery.

# 👀 How to share your solution?

Create a private Github repository, publish your solution, and [invite](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-personal-account-on-github/managing-access-to-your-personal-repositories/inviting-collaborators-to-a-personal-repository) `flvndh` as a contributor.
