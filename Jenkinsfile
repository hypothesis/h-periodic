#!groovy

def dockerTag = null
def dockerImage = null

def pushMaster(image) {
    if (env.BRANCH_NAME == 'master') {
        docker.withRegistry('', 'docker-hub-build') {
            image.push()
            image.push('latest')
        }
    }
}

pipeline {
    agent any

    stages {
        stage('setup') {
            steps {
                script {
                    buildVersion = sh(
                        script: 'python -c "import version; print(version.get_version())"',
                        returnStdout: true
                    ).trim()
                    dockerTag = buildVersion.replace('+', '-')
                    currentBuild.displayName = buildVersion
                }
            }
        }

        stage('build') {
            steps {
                sh "make docker DOCKER_TAG=${dockerTag}"
                script {
                    dockerImage = docker.image "hypothesis/h-periodic:${dockerTag}"
                }
            }
        }
    }

    post {
        success { pushMaster(dockerImage) }
    }
}
