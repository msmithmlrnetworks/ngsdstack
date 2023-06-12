#!/bin/bash
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
#Add ThousandEyes Docker Configurations
curl -Os https://downloads.thousandeyes.com/bbot/configure_docker.sh
chmod +x configure_docker.sh
sudo ./configure_docker.sh
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | \
  sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && \
  echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | \
  sudo tee /etc/apt/sources.list.d/ngrok.list && \
  sudo apt update && sudo apt install ngrok
cp ./config/ngrok/ngrok.yml ~/.config/ngrok/ngrok.yml
sudo ngrok service install --config ./config/ngrok/ngrok.yml
sudo ngrok service start

read -p "Enter the customer name EXACTLY as it appears in Vivantio: " new_value
# Extract the first word before any spaces
clean=$(echo "$new_value" | cut -d' ' -f1)

# Remove special characters
clean=$(echo "$clean" | tr -cd '[:alnum:]')

# Replace value in file
sed "s|old_value|$new_value|g; s|old_engine_value|$clean|g" "docker-compose.yml.template" > "docker-compose.yml"
sed "s|old_value|$new_value|g; s|old_engine_value|$clean|g" "ngrok.yaml.template" > "ngrok.yaml"
sed "s|old_value|$new_value|g; s|old_engine_value|$clean|g" "./config/ngrok/ngrok.yaml.template" > "./config/ngrok/ngrok.yaml"
echo $clean
echo $new_value
echo "Value successfully updated! Now use the following commands to start the stack:"
echo "'sudo apt install docker-compose'"
echo "'sudo docker login registry.checkmk.com' and enter the credentials."
echo "'Then:'"
echo "'sudo docker-compose up -d'"