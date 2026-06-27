
import os
import posthog
import uuid
import wmi

# Initialize PostHog
posthog.project_api_key = os.environ.get('POSTHOG_API_KEY', '')
posthog.host = 'https://app.posthog.com'

def get_machine_id():
    c = wmi.WMI()
    return c.Win32_BaseBoard()[0].SerialNumber

def track_installation():
    machine_id = get_machine_id()
    posthog.capture(machine_id, 'app_installed', {
        'os': 'windows',
        'version': '1.0.0'
    })
