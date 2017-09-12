podTemplate(label: 'cloud-native', containers: [
    containerTemplate(name: 'jnlp', image: '10.250.131.118:5000/jenkinsci/jnlp-slave:2.62', args: '${computer.jnlpmac} ${computer.name}', workingDir: '/home/jenkins'),
    // containerTemplate(name: 'docker', image: '10.250.131.118:5000/docker:1.13.1', command: 'cat', ttyEnabled: true),
    containerTemplate(name: 'ubuntu', image: '10.250.131.118:5000/ubuntu:16.04', command: 'cat', ttyEnabled: true),
    containerTemplate(name: 'kubectl', image: '10.250.131.118:5000/kubectl:1.7.0', command: 'cat', ttyEnabled: true)
],
volumes:[
    hostPathVolume(mountPath: '/var/run/docker.sock', hostPath: '/var/run/docker.sock'),
]){

  node ('cloud-native') {
    checkout scm
    // git(url: 'https://github.com/DanielXiao/cicd-demo.git', branch: 'master', credentialsId: 'github-token', changelog: true, poll: true)

    stage ('Build') {
      container('ubuntu') {
        sh "ls -la /home/jenkins"
        sh "sleep 300"
      }
    }

    stage ('End to end testing') {
      container('kubectl') {
        sh "kubectl version"
        sh "ls -la /home/jenkins"
      }
    }

    stage('Manual approval') {
      steps {
        input 'Approve to production?'
      }
    }

    stage ('Rolling update production') {
      container('kubectl') {
        sh "kubectl version"
        sh "ls -la /home/jenkins"
      }
    }

  }
}