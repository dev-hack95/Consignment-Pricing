pipeline {
  agent {
    docker {
      image 'python:3.10'
    }
  }
  stages {
    stage('Checkout Code') {
      steps {
        git(url: 'https://github.com/dev-hack95/Consignment-Pricing/', branch: 'dvc')
      }
    }

    stage('Log') {
      steps {
        sh 'ls -la'
      }
    
    stage('Deploy') {
      steps {
        sh 'docker build -f ./Dockerfile . -t myapp:latest'
      }
    }
    stage('Run') {
      steps {
        sh 'docker-compose up -d'
      }
    }
  }
}
