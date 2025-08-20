import requests
from flask import Flask, render_template, request, jsonify, redirect, url_for
import json
import os
import urllib.parse
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

DATA_FILE = 'problems.json'

# Jenkins server configuration
JENKINS_URL = os.getenv("JENKINS_URL")
JENKINS_USERNAME = os.getenv("JENKINS_USERNAME")
JENKINS_API_TOKEN = os.getenv("JENKINS_API_TOKEN")

def read_problems():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def write_problems(problems):
    with open(DATA_FILE, 'w') as f:
        json.dump(problems, f, indent=4)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/problems')
def problems():
    problems = read_problems()
    return render_template('problems.html', problems=problems)

@app.route('/problems/<int:problem_id>')
def problem(problem_id):
    problems = read_problems()
    problem = next((p for p in problems if p['id'] == problem_id), None)
    if problem is None:
        return "Problem not found", 404
    return render_template('problem.html', problem=problem, zip=zip)

@app.route('/rankings')
def rankings():
    return render_template('rankings.html')

@app.route('/submit', methods=['POST'])
def submit():
    code = request.form.get('code')
    language = request.form.get('language')
    problem_id = request.form.get('problem_id')
    
    if not code or not language or not problem_id:
        print(f"Missing form field: code={code}, language={language}, problem_id={problem_id}")
        return "Missing form field", 400
    
    print(f"Received submission: code={code}, language={language}, problem_id={problem_id}")
    
    
    


    def get_jenkins_crumb(jenkins_url, username, api_token):
        response = requests.get(f'{jenkins_url}/crumbIssuer/api/json', auth=(username, api_token))
        response.raise_for_status()  # Raise an error for bad status codes
        crumb_data = response.json()
        crumb_value = crumb_data['crumb']
        crumb_field = crumb_data['crumbRequestField']
        return crumb_field, crumb_value
    
    try:
        # Get Jenkins crumb
        crumb_field, crumb_value = get_jenkins_crumb(JENKINS_URL, JENKINS_USERNAME, JENKINS_API_TOKEN)
        
        # Trigger Jenkins job
        job_name = 'CodeJudgePipeline'
        params = {
            'LANGUAGE': language,
            'CODE': code,
            'PROBLEM_ID': problem_id
        }
        headers = {crumb_field: crumb_value}
        
        # Encode parameters
        encoded_params = urllib.parse.urlencode(params)
        
        # Build URL for job with parameters
        build_url = f'{JENKINS_URL}/job/{job_name}/buildWithParameters'
        
        response = requests.post(build_url, headers=headers, auth=(JENKINS_USERNAME, JENKINS_API_TOKEN), data=params)
        response.raise_for_status()  # Raise an error for bad status codes
        
        # Poll for the build result
        queue_url = response.headers['Location'] + 'api/json'
        build_number = None
        while build_number is None:
            queue_response = requests.get(queue_url, auth=(JENKINS_USERNAME, JENKINS_API_TOKEN))
            queue_response.raise_for_status()
            queue_item = queue_response.json()
            if 'executable' in queue_item:
                build_number = queue_item['executable']['number']
        
        # Get build result
        build_info_url = f'{JENKINS_URL}/job/{job_name}/{build_number}/api/json'
        build_info = requests.get(build_info_url, auth=(JENKINS_USERNAME, JENKINS_API_TOKEN)).json()
        console_output_url = f'{JENKINS_URL}/job/{job_name}/{build_number}/consoleText'
        console_output = requests.get(console_output_url, auth=(JENKINS_USERNAME, JENKINS_API_TOKEN)).text
        
        if build_info['result'] == 'SUCCESS':
            result = console_output.splitlines()[-1]
        else:
            result = 'Error'
    except requests.exceptions.RequestException as e:
        print(f"Request exception: {e}")
        result = 'Error'
    except Exception as e:
        print(f"General exception: {e}")
        result = 'Error'
    
    return jsonify({'status': result})

@app.route('/admin')
def admin():
    problems = read_problems()
    return render_template('admin.html', problems=problems)

@app.route('/admin/add', methods=['POST'])
def add_problem():
    problems = read_problems()
    problem_id = max([p['id'] for p in problems], default=0) + 1
    new_problem = {
        'id': problem_id,
        'name': request.form['name'],
        'description': request.form['description'],
        'time_limit': request.form['time_limit'],
        'memory_limit': request.form['memory_limit'],
        'input_examples': request.form.getlist('input_examples'),
        'output_examples': request.form.getlist('output_examples'),
        'test_cases': [{'input': i, 'output': o} for i, o in zip(request.form.getlist('test_inputs'), request.form.getlist('test_outputs'))]
    }
    problems.append(new_problem)
    write_problems(problems)
    
    return redirect(url_for('admin'))

@app.route('/admin/delete/<int:problem_id>', methods=['POST'])
def delete_problem(problem_id):
    problems = read_problems()
    problems = [p for p in problems if p['id'] != problem_id]
    write_problems(problems)
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)

