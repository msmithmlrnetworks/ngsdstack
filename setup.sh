#!/bin/bash

read -p "Enter the customer name: " new_value

# # Remove leading/trailing spaces
# new_value="$(echo -e "${new_value}" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')"

# # Validate input (no spaces or special characters)
# if [[ "$new_value" =~ [^a-zA-Z0-9] ]]; then
#   echo "Error: Input contains invalid characters or spaces."
#   exit 1
# fi

# Replace value in file
sed "s|old_value|$new_value|g" "docker-compose.yml.template" > "docker-compose.yml"
sed "s|old_value|$new_value|g" "ngrok.yaml.template" > "ngrok.yaml"


echo "Value successfully updated! Now use the following command to start the container: sudo docker-compose up -d"
