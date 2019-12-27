pipeline {
  agent any
  stages {
    stage('Tox') {
      steps {
        bat 'C:\\Python27\\Scripts\\tox'
      }
    }
    stage('deploy') {
      steps {
        bat 'C:\\Python27\\Scripts\\python deploy.py'
      }
    }
  }
}