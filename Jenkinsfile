pipeline {
    agent any
    options {
        skipDefaultCheckout(true)
        disableConcurrentBuilds()
        timeout(time: 10, unit: 'MINUTES')
    }
    environment {
        STUDENT_NAME = 'Eduard'
        STUDENT_SURNAME = 'Kim'
        STUDENT_GROUP = 'IT2-2313'
        STUDENT_ID = '37324'
        IMAGE_NAME = 'kim-eduard-devops'
        CONTAINER_NAME = 'kim-eduard-container'
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
                sh '''
                    echo "Student: $STUDENT_NAME $STUDENT_SURNAME"
                    echo "Group: $STUDENT_GROUP"
                    echo "Student ID: $STUDENT_ID"
                    git rev-parse HEAD
                '''
            }
        }
        stage('Build') {
            steps {
                sh 'python3 -m compileall -q app tests'
            }
        }
        stage('Test') {
            steps {
                sh 'python3 -m unittest discover -s tests -v'
            }
        }
        stage('Docker Build') {
            steps {
                sh 'docker build -t "$IMAGE_NAME" .'
            }
        }
        stage('Docker Run') {
            steps {
                sh '''
                    if docker container inspect "$CONTAINER_NAME" >/dev/null 2>&1; then
                        docker rm -f "$CONTAINER_NAME"
                    fi
                    docker run -d --name "$CONTAINER_NAME" \\
                        -p 127.0.0.1:8000:8000 \\
                        -e STUDENT_NAME -e STUDENT_SURNAME \\
                        -e STUDENT_GROUP -e STUDENT_ID "$IMAGE_NAME"
                    docker exec "$CONTAINER_NAME" python -c '
import os
import time
from urllib.request import urlopen
for attempt in range(20):
    try:
        response = urlopen("http://127.0.0.1:8000/", timeout=2)
        break
    except OSError:
        if attempt == 19:
            raise
        time.sleep(0.5)
text = response.read().decode()
for label, variable in [("Name", "STUDENT_NAME"), ("Surname", "STUDENT_SURNAME"),
                        ("Group", "STUDENT_GROUP"), ("Student ID", "STUDENT_ID")]:
    assert label + ": " + os.environ[variable] in text
print(text)
'
                    docker logs "$CONTAINER_NAME"
                    docker ps --filter "name=^/$CONTAINER_NAME$"
                '''
            }
        }
    }
}
