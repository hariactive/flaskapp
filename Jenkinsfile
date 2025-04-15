pipeline {
    agent any

    environment {
        FLASK_ENV = "development"
    }

    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/hariactive/flaskapp.git'
            }
        }

        stage('Set Up Virtual Env and Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Flask App') {
            steps {
                sh '''
                    source venv/bin/activate
                    export FLASK_APP=app.py
                    export FLASK_RUN_PORT=5000
                    flask run --host=0.0.0.0 --port=5000 &
                '''
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                    sleep 5
                    curl -f http://localhost:5000 || echo "Flask app not running!"
                '''
            }
        }
    }
}
