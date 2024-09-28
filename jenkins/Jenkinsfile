pipeline {
    agent any

    options{
        buildDiscarder(logRotator(numToKeepStr: '5', daysToKeepStr: '5'))
        timestamps()
    }

    environment{
        registry = 'minhquan1906/openaichatbot'
        registryCredential = 'dockerhub'
        version = "latest"
    }

    stages {
        stage('Build'){
            steps {
                script{
                    echo 'Building image for deployment...'
                    dockerImage = docker.build registry + ":" + version
                    echo 'Pushing image to dockerhub..'
                    docker.withRegistry( '', registryCredential ) {
                        dockerImage.push()
                    }
                }
            }
        }
        stage('Deploy') {
            agent {
                kubernetes {
                    containerTemplate {
                        name 'helm' // Name of the container to be used for helm upgrade
                        image 'minhquan1906/jenkins:lts-jdk17'// The image containing helm
                        imagePullPolicy 'Always' // Always pull image in case of using the same tag
                    }
                }
            }
            steps {
                script {
                    container('helm') {
                        sh("helm upgrade --install chatbot ./helm/model-serving --namespace model-serving")
                    }
                }
            }
        }
    }
}
