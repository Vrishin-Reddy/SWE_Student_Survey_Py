pipeline {
    agent any
    
    environment {
        // Docker image details
        BASE_IMAGE = 'vrishin/student-survey-api-micro-python'
        IMAGE_TAG = 'new'
        DEPLOY_PORT = "8080"
    }
    
    parameters {
        choice(name: 'DEPLOY_ENV', choices: ['dev', 'staging', 'prod'], description: 'Deployment environment')
        booleanParam(name: 'RUN_TESTS', defaultValue: true, description: 'Run tests')
        booleanParam(name: 'DEPLOY', defaultValue: true, description: 'Deploy after build')
        string(name: 'CUSTOM_TAG', defaultValue: '', description: 'Custom tag for the Docker image (empty for build number)')
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Prepare') {
            steps {
                script {
                    // Define image repository and tag
                    def DOCKER_REPO = "vrishin/student-survey-api-micro-python"
                    def DOCKER_TAG = params.CUSTOM_TAG ? params.CUSTOM_TAG : env.BUILD_NUMBER
                    
                    // Set the full image name as an environment variable
                    env.DOCKER_FULL_IMAGE = "${DOCKER_REPO}:${DOCKER_TAG}"
                    
                    echo "Building custom Docker image: ${env.DOCKER_FULL_IMAGE}"
                    
                    // Set environment-specific variables
                    if (params.DEPLOY_ENV == 'prod') {
                        env.API_HOST = "api.yourdomain.com"  // Replace with your production domain
                    } else if (params.DEPLOY_ENV == 'staging') {
                        env.API_HOST = "api-staging.yourdomain.com"  // Replace with your staging domain
                    } else {
                        env.API_HOST = "localhost"  // Default for development
                    }
                }
            }
        }
        
        stage('Run Tests') {
            when {
                expression { return params.RUN_TESTS }
            }
            steps {
                script {
                    // Check Docker access before running tests
                    sh 'sudo chmod 666 /var/run/docker.sock || true'
                    
                    // Pull the base image first to use for testing
                    sh "docker pull ${BASE_IMAGE}:${IMAGE_TAG}"
                    
                    // Run tests in a temporary container
                    sh """
                    docker run --rm \
                        -v \${WORKSPACE}:/app-test \
                        ${BASE_IMAGE}:${IMAGE_TAG} \
                        bash -c "cd /app-test && python manage.py test"
                    """
                }
            }
        }
        
        stage('Create Custom Docker Image') {
            steps {
                script {
                    // Create a temporary Dockerfile to extend the base image
                    writeFile file: 'CustomDockerfile', text: """
                        FROM ${BASE_IMAGE}:${IMAGE_TAG}
                        
                        # Add environment variables for CORS
                        ENV CORS_ALLOW_ALL_ORIGINS=True
                        ENV CORS_ALLOW_CREDENTIALS=True
                        
                        # Update API_BASE_URL for HTTPS if needed
                        ENV API_BASE_URL="https://\${env.API_HOST}:\${DEPLOY_PORT}"
                        
                        # Expose the port
                        EXPOSE ${DEPLOY_PORT}
                    """
                    
                    // Build the custom image
                    sh "docker build -t ${env.DOCKER_FULL_IMAGE} -f CustomDockerfile ."
                }
            }
        }
        
        stage('Push Docker Image') {
            steps {
                script {
                    // Login to Docker Hub
                    withCredentials([string(credentialsId: 'docker-hub-credentials', variable: 'DOCKER_AUTH')]) {
                        sh "echo ${DOCKER_AUTH} | docker login -u vrishin --password-stdin"
                    }
                    
                    // Push Docker image
                    sh "docker push ${env.DOCKER_FULL_IMAGE}"
                }
            }
        }
        
        stage('Deploy') {
            when {
                expression { return params.DEPLOY }
            }
            steps {
                script {
                    def deployEnv = "${params.DEPLOY_ENV}"
                    def deployCommand = ""
                    
                    if (deployEnv == 'prod') {
                        // Production deployment - using Docker directly
                        deployCommand = """
                        sudo docker stop student-survey-container || true
                        sudo docker rm student-survey-container || true
                        sudo docker run -d --name student-survey-container \
                            -p ${DEPLOY_PORT}:${DEPLOY_PORT} \
                            ${env.DOCKER_FULL_IMAGE}
                        """
                    } else if (deployEnv == 'staging') {
                        // Staging deployment
                        deployCommand = """
                        sudo docker stop student-survey-container || true
                        sudo docker rm student-survey-container || true
                        sudo docker run -d --name student-survey-container \
                            -p ${DEPLOY_PORT}:${DEPLOY_PORT} \
                            ${env.DOCKER_FULL_IMAGE}
                        """
                    } else {
                        // Development deployment - local or dev server
                        deployCommand = """
                        sudo docker stop student-survey-container || true
                        sudo docker rm student-survey-container || true
                        sudo docker run -d --name student-survey-container \
                            -p ${DEPLOY_PORT}:${DEPLOY_PORT} \
                            ${env.DOCKER_FULL_IMAGE}
                        """
                    }
                    
                    echo "Executing deployment command for ${deployEnv} environment"
                    sh deployCommand
                }
            }
        }
    }
    
    post {
        always {
            // Clean up with sudo permissions
            sh "rm -f CustomDockerfile || true"
            sh "sudo docker system prune -f || true"
        }
        success {
            echo "Pipeline completed successfully!"
            echo "Deployed image: ${env.DOCKER_FULL_IMAGE}"
        }
        failure {
            echo "Pipeline failed! Check the logs for details."
            // Add notifications for failures if needed
        }
    }
}