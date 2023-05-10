
read -p "Enter the customer name EXACTLY as it appears in Vivantio: " new_value

# Remove spaces and special characters
clean=$(echo "$new_value" | tr -cd '[:alnum:]-')

# Replace remaining spaces with hyphens
clean=$(echo "$clean" | tr ' ' '-')

clean=${clean:0:16}

# # Remove leading/trailing spaces
# new_value="$(echo -e "${new_value}" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')"

# # Validate input (no spaces or special characters)
# if [[ "$new_value" =~ [^a-zA-Z0-9] ]]; then
#   echo "Error: Input contains invalid characters or spaces."
#   exit 1
# fi

# Replace value in file
sed "s|old_value|$new_value|g; s|old_engine_value|$clean_string|g" "docker-compose.yml.template" > "docker-compose.yml"
sed "s|old_value|$new_value|g; s|old_engine_value|$clean_string|g" "ngrok.yaml.template" > "ngrok.yaml"
echo $clean
echo $new_value
echo "Value successfully updated! Now use the following commands to start the stack:"
echo "'sudo apt install docker-compose'"
echo "'sudo docker login registry.checkmk.com' and enter the credentials. Then:"
echo "'sudo docker-compose up -d'"