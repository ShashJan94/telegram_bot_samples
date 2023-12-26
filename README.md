
### Download Docker Desktop:

1. **Windows:**
   - Visit the [Docker Desktop for Windows](https://hub.docker.com/editions/community/docker-ce-desktop-windows) page.
   - Click on "Get Docker Desktop for Windows" to download the installer.
   - Run the installer and follow the on-screen instructions to complete the installation.

2. **Mac:**
   - Visit the [Docker Desktop for Mac](https://hub.docker.com/editions/community/docker-ce-desktop-mac) page.
   - Click on "Get Docker Desktop for Mac" to download the installer.
   - Open the downloaded `.dmg` file, drag the Docker icon to the Applications folder, and follow any additional instructions.

3. **Linux:**
   - For Linux, Docker Desktop is available for various distributions. Refer to the official Docker documentation for instructions specific to your distribution: [Install Docker Engine](https://docs.docker.com/engine/install/).


1. **Create a Project Folder:**
   - Create a folder for your project. This folder will contain your Dockerfile, scripts, and any other project-related files.

2. **Place Your Scripts in the Project Folder:**
   - Place your two scripts (`script1.py` and `script2.py`) directly in the project folder. The Dockerfile we previously created assumes that the scripts are in the same directory.

3. **Organize Dependencies:**
   - If your scripts have dependencies, create a `requirements.txt` file in the project folder. List the dependencies in this file.

   Example `requirements.txt`:
   ```
   requests
   pandas
   ```

   Make sure to adjust the `RUN pip install --no-cache-dir -r requirements.txt` line in the Dockerfile accordingly.


4. ### Write the Dockerfile

   ```Dockerfile
   # Use an official Python runtime as a parent image
   FROM python:3.9-slim-bullseye
   
   # Set the working directory in the container
   WORKDIR /app
   
   # Copy the current directory contents into the container
   COPY . /app
   
   # Install any needed packages specified in requirements.txt
   RUN pip install --no-cache-dir -r requirements.txt
   
   # Make port 80 available to the world outside this container
   EXPOSE 80
   
   # Define environment variable
   ENV NAME World
   
   # Run app.py when the container launches
   CMD ["python", "scriptName.py"]
   ```

5. **Build and Run Docker Container:**

   - Open a terminal in the project folder and run the following commands:
     ```bash
     # Build Docker image
     docker build -t <image_name> .

     # Run Docker container
     docker run -it <image_name>
     ```
   Adjust these commands based on your specific requirements and configuration.

Now, you should have Docker Desktop installed on your machine, your scripts in the project folder, and a Dockerfile to define your container.

If you are using Azure for the first time and want to take advantage of the Azure free subscription, follow these steps:

### Azure Free Subscription:

1. **Create a Microsoft Azure Account:**
   - If you don't have an Azure account, you can sign up for a free account by visiting the [Azure free account](https://azure.microsoft.com/en-us/free/) page.

2. **Sign Up for Azure:**
   - Click on the "Start free" button.
   - Follow the instructions to create a Microsoft account or sign in if you already have one.

3. **Fill in the Required Information:**
   - Provide the necessary information, including contact details and payment information. Note that Azure requires a credit card for identity verification, but it won't be charged during the free trial unless you upgrade to a paid account.

4. **Verify Your Identity:**
   - Verify your identity by entering the security code sent to your email or phone number.

5. **Activate Azure Free Account:**
   - Once your identity is verified, your Azure account will be activated with a free subscription, which includes a limited amount of resources and services for 12 months.

### Configure Azure CLI:

After creating your Azure account, you need to configure the Azure Command-Line Interface (Azure CLI) on your local machine. Follow these steps:

1. **Install Azure CLI:**
   - Install the Azure CLI by following the instructions provided in the [Azure CLI installation guide](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli).

2. **Log in to Azure CLI:**
   - Open a terminal and run the following command to log in to your Azure account:

     ```bash
     az login
     ```

   - Follow the on-screen instructions to complete the login process.

3. **Select Your Subscription (if necessary):**
   - If you have multiple subscriptions, you can select the one you want to use by running:

     ```bash
     az account set --subscription <subscription-id>
     ```

     Replace `<subscription-id>` with the ID of the desired subscription.

### Use Azure Free Subscription for Resources:

Once you have an Azure free subscription and Azure CLI configured, you can use it to deploy resources, including Azure Container Registry (ACR) and Azure Container Instances (ACI), without incurring additional charges within the limits of the free subscription.

Follow the earlier instructions to push your Docker image to ACR and deploy it to ACI using the Azure CLI. The resources you create will be part of your free subscription, and you can monitor your usage through the [Azure Portal](https://portal.azure.com/).

Keep in mind the specific limitations and offerings of the Azure free subscription, and consider upgrading to a paid subscription if you require additional resources beyond the free tier limits. Always be mindful of your resource usage to avoid unexpected charges.

I hope this helps you set up and leverage the Azure free subscription for your Dockerized scripts!


4. **Push Image to Azure Container Registry:**
   - Push your Docker image to Azure Container Registry (ACR) using the following commands:

     ```bash
     # Log in to your Azure account
     az login

     # Set your ACR login server and resource group name
     ACR_NAME=<your-acr-name>
     ACR_RESOURCE_GROUP=<your-acr-resource-group>

     # Log in to the ACR
     az acr login --name $ACR_NAME

     # Tag your local image with the ACR login server
     docker tag $IMAGE_NAME $ACR_NAME.azurecr.io/$IMAGE_NAME

     # Push the image to ACR
     docker push $ACR_NAME.azurecr.io/$IMAGE_NAME

     # Run Docker container
     docker run -it $ACR_NAME.azurecr.io/$IMAGE_NAME
     ```
P.S: You can also follow the same instructions with the Azure Portal UI.

6. **Troubleshooting:**
   - If you encounter issues during the build or deployment process, consider checking the following:
     - Dockerfile syntax errors.
     - Proper installation of dependencies in `requirements.txt`.
     - Azure credentials and permissions.
     - Azure Container Registry and Container Instances configurations.
     - Log files generated by your scripts or Docker container.

7. **Access Logs and Output:**
   - Use Docker logs to access the output and logs of your running container:

     ```bash
     docker logs <container-id>
     ```

   - Replace `<container-id>` with the actual ID of your running container.

Remember to customize the Dockerfile, instructions, and scripts based on your project structure and requirements. This guide provides a general outline, and you may need to adapt it according to your specific use case.

P.S: If you find the all above a bit complicated, two docker automation script you will find inside the repository. 
