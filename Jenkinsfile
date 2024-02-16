pipeline {
    agent {
        docker {
            image "docker:24.0.6-git" // Set docker image
        }
    }

    stages {
        stage('Build') {
            steps {
                // This stage builds PanelAppDB Project.
                sh 'echo "Building the project..."'

                // Create Conda env
                conda env create -n PanelAppDB_Jenkins --file environment.yml

            }
        }

        stage('Test') {
            steps {
                // This stage, runs the tests.
                
                if (exitCode == 0) { //check if connections working
                    connectionSuccessful = true
                    echo "Connected successfully! Running pytest..."
                
                    // Run pytest and Codecov
                    sh 'docker exec PanelAppDB_Jenkins pytest -n 3 --cov=PanelAppDB --cov=PanelAppDB --cov-report=term tests/'

                    // Send coverage report to Codecov
                    sh 'docker exec PanelAppDB_Jenkins codecov -t $CODECOV_TOKEN -b ${BRANCH_NAME}'

                    // Check for test failures
                    if (currentBuild.rawBuild.getLog(2000).join('\n').contains("test summary info") && currentBuild.rawBuild.getLog(2000).join('\n').contains("FAILED")) {
                        failure(message:"Pytest completed with failures")
                    }

                    // Check the Jenkins console log for pytest exit code
                    def pytestExitCode = currentBuild.rawBuild.getLog(2000).find { line -> line =~ /.*Pytest exit code: (\d+).*/ }
                    if (pytestExitCode) {
                        pytestExitCode = Integer.parseInt(pytestExitCode.replaceAll(/.*Pytest exit code: (\d+).*/, '$1'))
                        if (pytestExitCode != 0) {
                            failure(message:"Pytest failed with exit code $pytestExitCode")
                        }
                    }

                if (!connectionSuccessful) {
                    failure(message:"All connection attempts failed. Exiting...")
                }

            }
        }
    }

    post {
        success {
            // This block is executed if the pipeline runs successfully.
            echo 'Pipeline succeeded! Your project is built and tested.'
        }
        failure {
            // This block is executed if the pipeline fails.
            echo 'Pipeline failed. Please check the logs for details.'
        }
    }
}