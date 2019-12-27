pipeline {
  agent any
  stages {
    stage('Tox') {
      steps {
        bat 'C:\\Python27\\Scripts\\tox'
      }
    }
    /*stage('Unit Tests') {
      steps {
        bat '%WORKSPACE%/venv/Scripts/pytest'
      }
    }
    stage('Build Wheel') {
      steps {
        bat '%WORKSPACE%/venv/Scripts/python setup.py bdist_wheel'
      }
    }*/
  }
}