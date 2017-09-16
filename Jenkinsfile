podTemplate(label: 'cloud-native', containers: [
    containerTemplate(name: 'jnlp', image: '10.250.131.118:5000/jenkinsci/jnlp-slave:2.62', args: '${computer.jnlpmac} ${computer.name}', workingDir: '/home/jenkins'),
    containerTemplate(name: 'docker', image: '10.250.131.118:5000/docker:1.13.1', command: 'cat', ttyEnabled: true),
    containerTemplate(name: 'kubectl', image: '10.250.131.118:5000/kubectl-python:1.7.0', command: 'cat', ttyEnabled: true)
],
volumes:[
    hostPathVolume(mountPath: '/var/run/docker.sock', hostPath: '/var/run/docker.sock'),
    configMapVolume(mountPath: '/home/jenkins/.kube', configMapName: 'kube-config')
]){

  def image = "guestbook/frontend"
  def tag = "${image}:0.1.${env.BUILD_NUMBER}"
  def imageURL = "10.250.131.118:5000/${tag}"
  node ('cloud-native') {
    git(url: 'https://github.com/DanielXiao/cicd-demo.git', branch: 'master', credentialsId: 'github-token', changelog: true, poll: true)

    stage ('Build image') {
      container('docker') {
        sh "docker build -t ${tag} php-redis"
        sh "docker images"
      }
    }

    stage ('Push image to registry') {
      container('docker') {
        sh "docker tag ${tag} ${imageURL}"
        sh "docker push ${imageURL}"
      }
    }

    stage ('End to end testing') {
      parallel (
        'End to End test 1': {
          container('kubectl') {
            println "Deploy testbed 1"
            sh "python deploy_gb.py 'k8s-config/guestbook-template.yaml' 'e2e-1' '${imageURL}'"
            println "Do some testing"
            sh "wget -qO- http://frontend-e2e-1"
          }
        },
        'End to End test 2': {
          container('kubectl') {
            println "Deploy testbed 2"
            sh "python deploy_gb.py 'k8s-config/guestbook-template.yaml' 'e2e-2' '${imageURL}'"
            println "Do some testing"
            sh "wget -qO- http://frontend-e2e-2"
          }
        }
      )
    }

    stage('Manual promotion') {
        input 'Do you approve to promote build to production?'
        container('kubectl') {
          println "Clean up test environments"
          sh "kubectl delete -f guestbook-e2e-1.yaml"
          sh "kubectl delete -f guestbook-e2e-2.yaml"
        }
    }

    stage ('Rolling update production') {
      container('kubectl') {
        sh "kubectl set image deployment frontend-production php-redis=${imageURL} --record"
        sh "kubectl get svc,deploy,rs,pod -o wide -l app=guestbook-production"
        sh "kubectl rollout history deployment frontend-production"
      }
    }

  }
}