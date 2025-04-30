pipeline {
    agent any
    
    environment {
        // Docker image details
        BASE_IMAGE = 'vrishin/student-survey-api-micro-python'
        IMAGE_TAG = 'new'
        DEPLOY_PORT = "8081"  // Changed to 8081 to avoid conflict
        CONTAINER_PORT = "8080"  // Original container port
        // Docker Hub credentials
        DOCKER_USERNAME = 'vrishin'
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
                    
                    // Check for existing containers and services
                    sh "sudo netstat -tulpn | grep 8080 || echo 'Port 8080 is in use'"
                    sh "sudo docker ps | grep -i student-survey || echo 'No existing containers found'"
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
                    // Get API host and port for ARG values
                    def apiHost = env.API_HOST ?: "localhost"
                    def apiPort = env.DEPLOY_PORT ?: "8081"
                    
                    // Create a temporary Dockerfile to extend the base image
                    writeFile file: 'CustomDockerfile', text: """
                        FROM ${BASE_IMAGE}:${IMAGE_TAG}
                        
                        # Add environment variables for CORS
                        ENV CORS_ALLOW_ALL_ORIGINS=True
                        ENV CORS_ALLOW_CREDENTIALS=True
                        
                        # Define API URL with hardcoded values
                        ENV API_BASE_URL="https://${apiHost}:${apiPort}"
                        
                        # Expose the port
                        EXPOSE ${CONTAINER_PORT}
                    """
                    
                    // Build the custom image
                    sh "docker build -t ${env.DOCKER_FULL_IMAGE} -f CustomDockerfile ."
                }
            }
        }
        
        stage('Push Docker Image') {
            steps {
                script {
                    // Using direct password (not recommended for production)
                    sh "echo 'ZXcvbnM0981234#' | docker login -u ${DOCKER_USERNAME} --password-stdin"
                    
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
                    
                    // Stop any running containers first
                    sh """
                    # Find any existing containers using the same image pattern
                    EXISTING_CONTAINERS=\$(sudo docker ps -a | grep ${BASE_IMAGE} | awk '{print \$1}' || echo '')
                    
                    # Stop and remove if they exist
                    if [ ! -z "\$EXISTING_CONTAINERS" ]; then
                        sudo docker stop \$EXISTING_CONTAINERS || true
                        sudo docker rm \$EXISTING_CONTAINERS || true
                    fi
                    
                    # Force remove the specific container name if it exists
                    sudo docker rm -f student-survey-container || true
                    """
                    
                    // Run the container with the new port mapping
                    sh """
                    sudo docker run -d --name student-survey-container \
                        -p ${DEPLOY_PORT}:${CONTAINER_PORT} \
                        -e CORS_ALLOW_ALL_ORIGINS=True \
                        -e CORS_ALLOW_CREDENTIALS=True \
                        ${env.DOCKER_FULL_IMAGE}
                    """
                    
                    echo "Container deployed on port ${DEPLOY_PORT}"
                    
                    // Display running containers
                    sh "sudo docker ps | grep student-survey"
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
            echo "Application is available at http://localhost:${DEPLOY_PORT}"
        }
        failure {
            echo "Pipeline failed! Check the logs for details."
            // Add notifications for failures if needed
        }
    }
}