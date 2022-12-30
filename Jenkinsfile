pipeline {
  agent none
  stages {
    agent any
    stage('Checkout Code') {
      steps {
        git(url: 'https://github.com/dev-hack95/Consignment-Pricing', branch: 'dev')
      }
    }

    stage('Log') {
      agent any
      steps {
        sh 'ls -la'
      }
    }
    
    stage('Docker Image') {
    	agent {
      	docker {
        	image 'python:3.10'
        }
      }

    stage('Build') {
      agent any
      steps {
        sh 'docker build -f ./Dockerfile . -t myapp:latest'
      }
    }
    stage('Run') {
      agent any
      steps {
        sh 'docker-compose up'
      }
    }

  }
}
