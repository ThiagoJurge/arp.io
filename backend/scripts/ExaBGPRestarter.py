import subprocess
import time
import requests

class ExaBGPRestarter:
    def __init__(self, session_name="exabgp_session"):
        self.session_name = session_name
        self.success_message = "ExaBGP process restarted successfully."
        self.error_message = "Failed to restart ExaBGP process."

    def check_session_exists(self):
        check_session_cmd = f"screen -ls | grep -q {self.session_name}"
        return subprocess.call(check_session_cmd, shell=True) == 0

    def stop_session(self):
        subprocess.call(f"screen -S {self.session_name} -X quit", shell=True)

    def start_session(self):
        start_session_cmd = (
            f"screen -dmS {self.session_name} bash -c '"
            "env exabgp.daemon.user=root exabgp.daemon.daemonize=true "
            "exabgp.daemon.pid=/var/run/exabgp.pid "
            "exabgp.log.destination=/var/log/exabgp.log "
            "/opt/exabgp4/sbin/exabgp /etc/exabgp.conf'"
        )
        return subprocess.call(start_session_cmd, shell=True) == 0

    def wait_for_start(self, seconds=60):
        time.sleep(seconds)

    def execute_curl_request(self):
        url = 'http://10.33.14.146/wanguard-api/v1/bgp_announcements_actions'
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'text/html'
        }
        auth = ('admin', 'changeme')
        data = '{"batch_action":"Resend"}'

        response = requests.post(url, headers=headers, auth=auth, data=data)
        return response.status_code == 200