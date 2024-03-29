# Consignment-Pricing

![Python Version](https://img.shields.io/badge/Python-3.8.10-lightgrey)

## Authors

- [@dev-hack95](https://www.github.com/dev-hack95)

## Project Status
- Completed

## Table of Contents

  - [Problem Statement](#Problem-Statement)
  - [Methods](#methods)
  - [Tech Stack](#tech-stack)
  - [Quick glance at the results](#quick-glance-at-the-results)
  - [Run Locally](#run-locally)
  - [Explore the notebook](#explore-the-notebook)
  - [Deployment](#Deployment)
  - [Docker](#Docker)
  - [Kubernetes](#Kubernetes)
  - [Repository structure](#repository-structure)
  - [Results](#Results)
  
## Problem Statement
  - The market for logistics analytics is expected to develop at a CAGR of 17.3 percent
from 2019 to 2024, more than doubling in size. This data demonstrates how logistics
organizations are understanding the advantages of being able to predict what will
happen in the future with a decent degree of certainty. Logistics leaders may use this
data to address supply chain difficulties, cut costs, and enhance service levels all at the
same time. The main goal is to predict the consignment pricing based on the available factors in the
dataset.

## Methods

- Exploratory data analysis
- Bivariate analysis
- Multivariate correlation
- Explainable AI
- Model Comparison
- Model deployment

## Tech Stack

- Python (refer to requirement.txt for the packages used in this project)
- MLflow
- DVC
- Docker
- Kubernetes
- Devops

## Quick glance at the results
Correlation between the features.

## Run Locally

1) Initialize git

```bash
git init
```


2) Clone the project

```bash
git clone -b dvc https://github.com/dev-hack95/Consignment-Pricing
```

3) enter the project directory

```bash
cd Consigmrnt-Pricing
```

4) install the requriments

```bash
pip install -r requirements.txt
```

5) run application

```bash
streamlit run app.py
```

## RUN on docker


1) Clone the project

```bash
git clone -b dvc https://github.com/dev-hack95/Consignment-Pricing
```

2) enter the project directory

```bash
cd Consigmrnt-Pricing
```

3) Build Docker image

```bash
docker build -f ./Dockerfile . -t myapp:latest
```

4) Run docker-compose
```bash
docker-compose up -d
```

5) Stop container
```bash
docker-compose down
```
