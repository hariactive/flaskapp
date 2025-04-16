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
                    nohup python3 app.py > flask.log 2>&1 &
                    sleep 5
                '''
            }
        }



        stage('Test App') {
            steps {
                script {
                    def result = sh(script: "curl -f http://localhost:5000", returnStatus: true)
                    if (result != 0) {
                        error("❌ Flask app not running!")
                    } else {
                        echo "✅ Flask app is running!"
                    }
                }
            }
        }

        stage('View Flask Log') {
            steps {
                sh 'cat flask.log || echo "No log file found."'
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
