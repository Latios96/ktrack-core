pipeline {
  agent any
  stages {
    stage('Virtualenv') {
      steps {
        bat 'C:\\Python27\\Scripts\\virtualenv venv'
        bat 'set PATH=%WORKSPACE%/venv/Scripts/;%PATH%'
        bat '%WORKSPACE%/venv/Scripts/python setup.py install'
        bat '%WORKSPACE%/venv/Scripts/pip install -r requirements_ci.txt'
      }
    }
  }
}