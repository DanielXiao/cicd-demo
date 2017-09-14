podTemplate(label: 'cloud-native', containers: [
    containerTemplate(name: 'jnlp', image: '10.250.131.118:5000/jenkinsci/jnlp-slave:2.62', args: '${computer.jnlpmac} ${computer.name}', workingDir: '/home/jenkins'),
    containerTemplate(name: 'docker', image: '10.250.131.118:5000/docker:1.13.1', command: 'cat', ttyEnabled: true),
    containerTemplate(name: 'kubectl', image: '10.250.131.118:5000/kubectl:1.7.0', command: 'cat', ttyEnabled: true)
],
volumes:[
    hostPathVolume(mountPath: '/var/run/docker.sock', hostPath: '/var/run/docker.sock'),
    configMapVolume(mountPath: '/home/jenkins/.kube', configMapName: 'kube-config')
]){

  def image = "gb-frontend"
  def imageURL = "10.250.131.118:5000/${image}:0.1.${env.BUILD_NUMBER}"
  def engine = new groovy.text.SimpleTemplateEngine()
  def binding1 = ["suffix":"e2e-1", "imageURL":"${imageURL}"]
  def binding2 = ["suffix":"e2e-2", "imageURL":"${imageURL}"]
  node ('cloud-native') {
    git(url: 'https://github.com/DanielXiao/cicd-demo.git', branch: 'master', credentialsId: 'github-token', changelog: true, poll: true)

    stage ('Build image') {
      container('docker') {
        sh "docker build -t ${image}:0.1.${env.BUILD_NUMBER} php-redis"
        sh "docker images"
      }
    }

    stage ('Push image to registry') {
      container('docker') {
        sh "docker images"
        sh "docker tag ${image}:0.1.${env.BUILD_NUMBER} ${imageURL}"
        sh "docker push ${imageURL}"
      }
    }

    stage ('End to end testing') {
      String k8sGuestBook = new File("${env.WORKSPACE}/k8s-config/guestbook-template.yaml").text
      testbed1 = engine.createTemplate(k8sGuestBook).make(binding1).toString()
      configFile1 = new File("${env.WORKSPACE}/guestbook-e2e-1.yaml")
      configFile1 << testbed1
      testbed2 = engine.createTemplate(k8sGuestBook).make(binding2).toString()
      configFile2 = new File("${env.WORKSPACE}/guestbook-e2e-2.yaml")
      configFile2 << testbed2
      parallel (
        'End to End test 1': {
          container('kubectl') {
            println "Deploy testbed 1"
            sh "kubectl create -f guestbook-e2e-1.yaml"
            sh "sleep 300"
            println "Do some testing"
            sh "wget -qO- http://frontend-e2e-1"
          }
        },
        'End to End test 2': {
          container('kubectl') {
            println "Deploy testbed 2"
            sh "kubectl create -f guestbook-e2e-2.yaml"
            sh "sleep 300"
            println "Do some testing"
            sh "wget -qO- http://frontend-e2e-2"
          }
        }
      )
    }

    stage('Manual promotion') {
        input 'Do you approve to promote build to production?'
    }

    stage ('Rolling update production') {
      container('kubectl') {
        sh "kubectl version"
        sh "ls -la /home/jenkins"
      }
    }

  }
}