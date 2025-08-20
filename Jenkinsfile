pipeline {
    
    agent any

    environment {
        DOCKER_IMAGE = "judge_sys/judge:latest"
    }

    stages {
        stage('Build') {
            steps {
                script {
                    docker.build(DOCKER_IMAGE)
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    def test_cases = ['test1', 'test2', 'test3']
                    for (test_case in test_cases) {
                        docker.image(DOCKER_IMAGE).inside {
                            sh "python3 judge.py python /path/to/code.py /judge/test_cases/${test_case}/input.txt /judge/test_cases/${test_case}/expected_output.txt"
                        }
                    }
                }
            }
        }
    }
}
