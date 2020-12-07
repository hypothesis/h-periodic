/**
 * This app's Jenkins Pipeline.
 *
 * This is written in Jenkins Scripted Pipeline language.
 * For docs see:
 * https://jenkins.io/doc/book/pipeline/syntax/#scripted-pipeline
*/

// Import the Hypothesis shared pipeline library, which is defined in this
// repo: https://github.com/hypothesis/pipeline-library
@Library("pipeline-library") _

// The the built hypothesis/h-periodic Docker image.
def img

node {
    // The args that we'll pass to Docker run each time we run the Docker
    // image.
    runArgs = "-u root -e SITE_PACKAGES=true"

    stage("Build") {
        // Checkout the commit that triggered this pipeline run.
        checkout scm
        // Build the Docker image.
        img = buildApp(name: "hypothesis/h-periodic")
    }

    onlyOnMaster {
        stage("release") {
            releaseApp(image: img)
        }
    }
}

onlyOnMaster {
    milestone()
    stage("prod deploy") {
        input(message: "Deploy to prod?")
        milestone()
        deployApp(image: img, app: "h-periodic", env: "prod")
    }
}
