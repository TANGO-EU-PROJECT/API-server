pipeline {
    agent {
        node {
            label 'Agent01'
        }
    }

    environment {
        APP_NAME = "api"
        DOCKER_IMAGE = 'api-server' 
        ARTIFACTORY_SERVER = "harbor.tango.rid-intrasoft.eu"
        ARTIFACTORY_DOCKER_REGISTRY = "harbor.tango.rid-intrasoft.eu/api-server/"
        BRANCH_NAME = "main"
        DOCKER_IMAGE_TAG = "${APP_NAME}:R${env.BUILD_ID}"
        TAG = 'latest'    
        KUBERNETES_NAMESPACE = 'ips-testing1'
        RELEASE_NAME = 'api-server'
    }

    stages {
        stage('Build image') { // build and tag docker image
            steps {
                dir('API') {
                    echo 'Starting to build docker image'
                    script {
                        def dockerImage = docker.build("${ARTIFACTORY_DOCKER_REGISTRY}${DOCKER_IMAGE_TAG}") 
                    }
                }
            }
        }

        stage("Push_Image") {
            steps {
                withCredentials([usernamePassword(credentialsId: 'harbor-jenkins-creds', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                    echo "***** Push Docker Image *****"
                    sh 'docker login ${ARTIFACTORY_SERVER} -u ${USERNAME} -p ${PASSWORD}'
                    sh 'docker image push ${ARTIFACTORY_DOCKER_REGISTRY}${DOCKER_IMAGE_TAG}'
                    sh 'docker tag ${ARTIFACTORY_DOCKER_REGISTRY}${DOCKER_IMAGE_TAG} ${ARTIFACTORY_DOCKER_REGISTRY}${APP_NAME}:latest'
                    sh 'docker image push ${ARTIFACTORY_DOCKER_REGISTRY}${APP_NAME}:latest'
                }
            }
        }

        stage('Docker Remove Image locally') {
            steps {
                sh 'docker rmi "${ARTIFACTORY_DOCKER_REGISTRY}${DOCKER_IMAGE_TAG}"'
                sh 'docker rmi "${ARTIFACTORY_DOCKER_REGISTRY}${APP_NAME}:latest"'
            }
        }

        stage("Deployment") {
            steps {
                withKubeConfig([credentialsId: 'K8s-config-file', serverUrl: 'https://kubernetes.tango.rid-intrasoft.eu:6443', namespace: 'ips-testing1']) {
                    sh 'kubectl get ingress -n ips-testing1'
                    sh 'helm install api-server ./api-server --namespace ips-testing1 --values ./api-server/values.yaml'
                    sh 'kubectl get pods -n ${KUBERNETES_NAMESPACE}'
                    sh 'kubectl get ingress -n ${KUBERNETES_NAMESPACE}'
                    sh 'kubectl describe certificate api-server-service-cert -n ips'
                    sh 'kubectl get secret api-server-tls-secret -n ips'
                }
            }
        }
    }
}
