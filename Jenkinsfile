pipeline {
  agent any
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
    }

  }
}