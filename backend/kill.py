from flask import Flask, request, jsonify
import os
import signal

app = Flask(__name__)

@app.route('/kill_process', methods=['POST'])
def kill_process():
    try:
        pid = int(request.form.get('pid'))
        os.kill(pid, signal.SIGTERM)
        response = {'status': 'success', 'message': f'Process {pid} terminated successfully'}
    except Exception as e:
        response = {'status': 'error', 'message': str(e)}
    return jsonify(response)

@app.route('/kill_process/<int:pid>', methods=['GET'])
def kill_process_by_pid(pid):
    try:
        os.kill(pid, signal.SIGTERM)
        response = {'status': 'success', 'message': f'Process {pid} terminated successfully'}
    except Exception as e:
        response = {'status': 'error', 'message': str(e)}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
