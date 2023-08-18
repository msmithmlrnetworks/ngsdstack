# NGSD Satellite config tool
This repo is used to configure the satellite service stack for the ngsd platform.

There are two scripts that configure the template service descriptions contained for Docker-Compose and ngrok. 

Using the scripts will create the correct configuration of the documents automatically.

Detailed instructions are below.


# Step 1: Install Ubuntu 22.04 LTS


### Download ISO and use to install according to screenshots



# Step 2: Download the repo and configure.

 Pull the repo using git pull and then change directory into the new folder that has been created called ngsdstack.
 

    git clone https://github.com/msmithmlrnetworks/ngsdstack.git
    cd ngsdstack

Once in the folder excute the setup script by using the following command.

    sh setup.sh
 
 You will be prompted to enter the customer name once Docker has been installed.
 
 NOTE: Ensure that this matches the customer name in vivantio exactly.

    Enter the customer name EXACTLY as it appears in Vivantio:
Then login to the Check MK repository.

    sudo docker login registry.checkmk.com
That is everything complete and you are now ready to start the stack.

If you have made a mistake and need to change the customer name for any reason after having run the setup.sh script then use the following command to update the configuration.

    sh update.sh
You will only be prompted for the customer name again and not to install Docker.

# Step 3: Start the application stack.
Start the stack the first time by using the following command.
    **sudo sh first-start.sh

Start the stack after the first time by using the following command.

    sudo docker-compose up -d
If you need to stop the stack for any reason then the following command shuts it down again

    sudo docker-compose down




