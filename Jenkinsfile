#!groovy

@Library('pipeline-library') _

def img

node {
    stage('build') {
        checkout(scm)
        img = buildApp(name: 'hypothesis/h-periodic')
    }

    onlyOnMaster {
        stage('release') {
            releaseApp(image: img)
        }
    }
}

onlyOnMaster {
    milestone()
    stage('qa deploy') {
        deployApp(image: img, app: 'h-periodic', env: 'qa')
    }

    milestone()
    stage('prod deploy') {
        input(message: "Deploy to prod?")
        milestone()
        deployApp(image: img, app: 'h-periodic', env: 'prod')
    }
}
