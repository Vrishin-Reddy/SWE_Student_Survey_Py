pipeline {
    agent any
    
    environment {
        // Docker image details
        BASE_IMAGE = 'vrishin/student-survey-api-micro-python'
        IMAGE_TAG = 'new'
        CUSTOM_IMAGE_NAME = 'vrishin/student-survey-api-micro-python'
        CUSTOM_IMAGE_TAG = "${env.BUILD_NUMBER}"
        
        // Deployment details
        DEPLOYMENT_ENV = "${params.DEPLOY_ENV ?: 'dev'}"
        DEPLOY_PORT = "8080"
        
        // AWS credentials for deployment (if using AWS)
        AWS_CREDENTIALS = 'aws-credentials-id'  // Replace with your Jenkins credential ID
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
                    // Use custom tag if provided, otherwise use build number
                    if (params.CUSTOM_TAG) {
                        CUSTOM_IMAGE_TAG = params.CUSTOM_TAG
                    }
                    
                    // Set the full image name
                    FULL_CUSTOM_IMAGE = "${CUSTOM_IMAGE_NAME}:${CUSTOM_IMAGE_TAG}"
                    
                    echo "Building image: ${FULL_CUSTOM_IMAGE}"
                }
            }
        }
        
        stage('Run Tests') {
            when {
                expression { return params.RUN_TESTS }
            }
            steps {
                script {
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
                        ENV API_BASE_URL="https://\${params.API_HOST}:\${DEPLOY_PORT}"
                        
                        # Expose the port
                        EXPOSE ${DEPLOY_PORT}
                    """
                    
                    // Build the custom image
                    sh "docker build -t ${FULL_CUSTOM_IMAGE} -f CustomDockerfile ."
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
                    sh "docker push ${FULL_CUSTOM_IMAGE}"
                }
            }
        }
        
        stage('Deploy') {
            when {
                expression { return params.DEPLOY }
            }
            steps {
                script {
                    def deployEnv = "${DEPLOYMENT_ENV}"
                    def deployCommand = ""
                    
                    if (deployEnv == 'prod') {
                        // Production deployment - for example using AWS ECS
                        withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', 
                                        accessKeyVariable: 'AWS_ACCESS_KEY_ID', 
                                        credentialsId: AWS_CREDENTIALS, 
                                        secretKeyVariable: 'AWS_SECRET_ACCESS_KEY']]) {
                            // Example: Update ECS service
                            deployCommand = """
                            aws ecs update-service \
                                --cluster production-cluster \
                                --service student-survey-service \
                                --force-new-deployment
                            """
                        }
                    } else if (deployEnv == 'staging') {
                        // Staging deployment
                        deployCommand = """
                        ssh user@staging-server 'docker pull ${FULL_CUSTOM_IMAGE} && \
                        docker stop student-survey-container || true && \
                        docker rm student-survey-container || true && \
                        docker run -d --name student-survey-container \
                            -p ${DEPLOY_PORT}:${DEPLOY_PORT} \
                            ${FULL_CUSTOM_IMAGE}'
                        """
                    } else {
                        // Development deployment - local or dev server
                        deployCommand = """
                        docker stop student-survey-container || true
                        docker rm student-survey-container || true
                        docker run -d --name student-survey-container \
                            -p ${DEPLOY_PORT}:${DEPLOY_PORT} \
                            ${FULL_CUSTOM_IMAGE}
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
            // Clean up
            sh "rm -f CustomDockerfile"
            sh "docker system prune -f"
        }
        success {
            echo "Pipeline completed successfully!"
            echo "Deployed image: ${FULL_CUSTOM_IMAGE}"
        }
        failure {
            echo "Pipeline failed! Check the logs for details."
            // Add notifications for failures (email, Slack, etc.)
            // mail to: 'team@example.com', subject: 'Pipeline failed', body: "Build failed: ${env.BUILD_URL}"
        }
    }
}