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

---

# Implementation

The implementation of this assignment has been divided into two parts, API and Warehouse. The code for both these parts is located within this repository.

## API

The purpose of the API is to abstract away the lower level details of the underlying Postgres database. Any user/machine that needs to interact with the database can simply use the API endpoints to fetch data available in the database.

### Installation

The project has been coded in Python 3.12 and can be run using Docker. To be able to use the API, you need to install:
1. [Docker](https://docs.docker.com/engine/install/).
2. [Docker Compose](https://docs.docker.com/compose/install/).
3. Clone the repository to your local machine.

### Usage

1. From your terminal, navigate to the directory where the files have been cloned.
2. Run the command `docker compose up`.
3. This should create three docker images: postgres, pgadmin4 and api
4. Navigate to `http://0.0.0.0:80/docs` to interactively test the API.
5. To be able to test the endpoints, you need to authenticate yourself. There is a green button called `Authorize` on the top right corner of the docs page.
6. In here you need to provide the following username: `testuser@awesomeinc.com` and password: `testpassword`.
7. Once you are authenticated, you can test the two endpoints.
8. `/all-tables`: This returns a dictionary containing a list of all tables available in the Postgres database.
9. `/{table_name}`: This is a dynamic endpoint that returns records from the database depending on the name of the table provided to the endpoint.

### Additional Information

1. The APIs have been created using the `FastAPI` library.
2. `pytest` has been used to test the APIs.
3. To containerize the application, `Docker` and `Docker Compose` are used.
4. `pre-commit` is used to lint, format, and run tests before any commit operations.
5. The `Pydantic` library is used to do data validation of the records returned from the database. This ensures that data quality issues are captured very early in the data lifecycle.
6. [rye](https://rye.astral.sh/guide/installation/) is used as the package manager.
7. Code versioning can be found in the `pyproject.toml` file.


## Data Warehouse

This is the second part of the assignment where a data warehouse needed to be created so that business users could make informed decisions based on the data generated by the operational database.

### Dimensional Model

Before diving into creating a data warehouse, it was necessary to create a dimensional model to understand the relationships between the different tables. The dimensional model can be found under this link: https://dbdiagram.io/d/awesomeinc_dimensionsal_model-669e55b18b4bb5230e00dabd

1. First, an ERD diagram is shown that maps the table relationships.
2. Then comes the dimensional model suitable for a data warehouse.
3. Finally, you can see individual tables that can be used to generate reports/dashboards for very specific business questions.
4. Note, that extra columns have been added to the dimension tables that can be used to track SCDs.

### Installation

The data warehouse has been created using dbt and the tables are located under a different schema called `warehouse` within the Postgres database.

1. If you are using rye as the package manager, then all you need to do is execute the command `rye sync`. This will install the dependencies (like dbt-core, dbt-postgres).
2. Once dbt is installed you can execute the `dbt deps` command to install dbt-specific dependencies.
3. Finally, you can execute the `dbt build` command that will create all the necessary tables and test them for data quality. Note, you need to have the postgres container running to be able to build the models.

### Usage

1. Execute `docker compose up` to launch the pgadmin4 container.
2. Using pgadmin4, you can explore the different tables that have been created using dbt.
3. You can also execute `dbt docs generate` and `dbt docs serve` to generate and view documentation and lineage graphs.

### Note

1. Since the dbt project is nested under the `src/awesome_inc/warehouse` directory, you need to provide the path to the `dbt_project.yml` and `profiles.yml` files when executing dbt commands especially if you are running the commands from the root directory.

## Future Releases (To-do)

1. Implement CI using GitHub Actions.
2. Add [re_data](https://docs.getre.io/latest/docs/re_data/introduction/whatis_data) to improve data quality within the dbt project.