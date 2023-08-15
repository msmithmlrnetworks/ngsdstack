#!/usr/bin/env python3
# Vivantio Integration Script for NGSD.

import os
import sys
import requests
import re
import time

# Read environment variables from CheckMK
context = dict([
    (var[7:], value)
    for (var, value)
    in os.environ.items()
    if var.startswith("NOTIFY_")
])

# Set the exit codes
EXIT_SUCCESS = 0
EXIT_FAILURE = 2

# Add additional variables
context.update({"timestamp": int(time.time())})

tmpl_host_subject = 'NGSD: $HOSTNAME$ - $EVENT_TXT$'
tmpl_service_subject = 'NGSD: $HOSTNAME$/$SERVICEDESC$ $EVENT_TXT$'
tmpl_common_body = """Host:     $HOSTNAME$
Alias:    $HOSTALIAS$
Address:  $HOSTADDRESS$
"""
tmpl_host_body = """Event:    $EVENT_TXT$
Output:   $HOSTOUTPUT$
Perfdata: $HOSTPERFDATA$
$LONGHOSTOUTPUT$
"""
tmpl_service_body = """Service:  $SERVICEDESC$
Event:    $EVENT_TXT$
Output:   $SERVICEOUTPUT$
Perfdata: $SERVICEPERFDATA$
$LONGSERVICEOUTPUT$
"""

def substitute_context(template, context):
    # First replace all known variables
    for varname, value in context.items():
        template = template.replace('$'+varname+'$', str(value))

    # Remove the rest of the variables and make them empty
    template = re.sub(r"\$[A-Z_][A-Z_0-9]*\$", "", template)
    return template

def construct_content(context):
    # Create a notification summary in a new context variable
    # Note: This code could maybe move to cmk --notify in order to
    # make it available every in all notification scripts
    # We have the following types of notifications:

    # - Alerts                OK -> CRIT
    #   NOTIFICATIONTYPE is "PROBLEM" or "RECOVERY"

    # - Flapping              Started, Ended
    #   NOTIFICATIONTYPE is "FLAPPINGSTART" or "FLAPPINGSTOP"

    # - Downtimes             Started, Ended, Cancelled
    #   NOTIFICATIONTYPE is "DOWNTIMESTART", "DOWNTIMECANCELLED", or "DOWNTIMEEND"

    # - Acknowledgements
    #   NOTIFICATIONTYPE is "ACKNOWLEDGEMENT"

    # - Custom notifications
    #   NOTIFICATIONTYPE is "CUSTOM"

    notification_type = context["NOTIFICATIONTYPE"]
    if notification_type in ["PROBLEM", "RECOVERY"]:
        txt_info = "WAS $PREVIOUS@HARDSHORTSTATE$ IS NOW $@SHORTSTATE$"

    elif notification_type.startswith("FLAP"):
        if "START" in notification_type:
            txt_info = "Started Flapping"
        else:
            txt_info = "Stopped Flapping ($@SHORTSTATE$)"

    elif notification_type.startswith("DOWNTIME"):
        what = notification_type[8:].title()
        txt_info = "Downtime " + what + " ($@SHORTSTATE$)"

    elif notification_type == "ACKNOWLEDGEMENT":
        txt_info = "Acknowledged ($@SHORTSTATE$)"

    elif notification_type == "CUSTOM":
        txt_info = "Custom Notification ($@SHORTSTATE$)"

    else:
        txt_info = notification_type  # Should never happen

    txt_info = substitute_context(txt_info.replace("@", context["WHAT"]), context)

    context["EVENT_TXT"] = txt_info

    # Prepare the mail contents
    if "PARAMETER_COMMON_BODY" in context:
        tmpl_body = context['PARAMETER_COMMON_BODY']
    else:
        tmpl_body = tmpl_common_body

    # Compute the subject and body of the mail
    if context['WHAT'] == 'HOST':
        tmpl = context.get('PARAMETER_HOST_SUBJECT') or tmpl_host_subject
        if "PARAMETER_HOST_BODY" in context:
            tmpl_body += context["PARAMETER_HOST_BODY"]
        else:
            tmpl_body += tmpl_host_body
    else:
        tmpl = context.get('PARAMETER_SERVICE_SUBJECT') or tmpl_service_subject
        if "PARAMETER_SERVICE_BODY" in context:
            tmpl_body += context["PARAMETER_SERVICE_BODY"]
        else:
            tmpl_body += tmpl_service_body

    context['SUBJECT'] = substitute_context(tmpl, context)
    body = substitute_context(tmpl_body, context)

    return body


# Define the API endpoint URL
api_endpoint = 'https://europe-west2-ngsd-ea53b.cloudfunctions.net/httpsAlertsTrigger'
api_key = 'b4kyj96W3vW1vn7Hg0OimUctSTBoBqsA'  # Replace with your actual API key
max_retries = 3  # Define the maximum number of retries

# Create the query parameters
params = {
    'apiKey': api_key,
    'assetTag': context['HOSTNAME'],
}

# Add content to dictionary
context.update({'CONTENT': construct_content(context)})

# Send the API request with retry mechanism
for attempt in range(1, max_retries + 1):
    try:
        response = requests.post(api_endpoint, json=context, params=params)
        response.raise_for_status()
        jsonResp = response.json()  # Parse the JSON response into a Python dictionary

        if response.status_code >= 200 and response.status_code < 300:
            print('API request sent successfully.')
            sys.exit(EXIT_SUCCESS)  # Exit with success code
        else:
            print(f'Error sending API request (attempt {attempt}/{max_retries}): Unexpected status code {response.status_code}')
    except requests.exceptions.RequestException as e:
        print(f'Error sending API request (attempt {attempt}/{max_retries}): {e}')
        if attempt < max_retries:
            print('Retrying in 5 seconds...')
            time.sleep(5)
        else:
            print(f'Retry limit reached. Unable to send API request.')
            sys.exit(EXIT_FAILURE)  # Exit with failure code

