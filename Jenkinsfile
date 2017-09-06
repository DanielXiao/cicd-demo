pipeline {
  agent any
  stages {
    stage('Checkout SCM') {
      steps {
        git(url: 'https://github.com/DanielXiao/cicd-demo.git', branch: 'master', credentialsId: 'github-token', changelog: true, poll: true)
      }
    }
    stage('Compile') {
      steps {
        sh 'echo "Dump step"'
      }
    }
    stage('Integration Test') {
      steps {
        parallel(
          "Integration Test": {
            sh 'echo "Run integration tests"'
            
          },
          "Load Test": {
            sh 'echo "Run Load tests"'
            
          }
        )
      }
    }
    stage('Publish image') {
      steps {
        sh 'echo "Publish image"'
      }
    }
    stage('Manual approve') {
      steps {
        input 'Approve to production'
      }
    }
    stage('Rolling update production') {
      steps {
        sh 'echo "Update production"'
      }
    }
  }
}