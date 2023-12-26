Download Docker Desktop:
Windows:

Visit the Docker Desktop for Windows page.
Click on "Get Docker Desktop for Windows" to download the installer.
Run the installer and follow the on-screen instructions to complete the installation.

Mac:

Visit the Docker Desktop for Mac page.
Click on "Get Docker Desktop for Mac" to download the installer.
Open the downloaded .dmg file, drag the Docker icon to the Applications folder, and follow any additional instructions.

Linux:

For Linux, Docker Desktop is available for various distributions. Refer to the official Docker documentation for instructions specific to your distribution: Install Docker Engine.
### Dockerfile

```Dockerfile
# Use an official Python runtime as a parent image
FROM python:3.8-slim

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
CMD ["python", "./app.py"]
```

### Instructions

1. **Organize Your Project:**
   - Create a folder for your project.
   - Place your two scripts (`script1.py` and `script2.py`) in this folder.
   - Create a `requirements.txt` file if your scripts have dependencies. List them there.

2. **Create Dockerfile:**
   - Create a file named `Dockerfile` in your project folder.
   - Copy and paste the above Dockerfile code into `Dockerfile`.

3. **Build Docker Image:**
   - Open a terminal and navigate to your project folder.
   - Run the following command to build the Docker image:

     ```bash
     docker build -t youtube-notifications .
     ```

   - This assumes your Dockerfile is in the current directory. Adjust the command if needed.

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
     docker tag youtube-notifications $ACR_NAME.azurecr.io/youtube-notifications

     # Push the image to ACR
     docker push $ACR_NAME.azurecr.io/youtube-notifications
     ```

5. **Run Docker Container in Azure Container Instances (ACI):**
   - Use the Azure Portal or Azure CLI to create an ACI instance and deploy your Docker container. Make sure to specify the image from your ACR.

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
