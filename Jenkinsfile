pipeline {
  agent any
  stages {
    stage('Checkout Code') {
      steps {
        git(url: 'https://github.com/dev-hack95/Consignment-Pricing', branch: 'dev')
      }
    }

    stage('Log') {
      steps {
        sh 'ls -la'
      }
    }

    stage('Build') {
      steps {
        sh 'docker build -f ./Dockerfile . -t myapp:latest'
      }
    }
    stage('Run') {
      steps {
        sh 'docker-compose up'
      }
    }

  }
}
