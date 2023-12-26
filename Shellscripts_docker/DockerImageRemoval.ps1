# Step 0: Check Azure login
$azureLoggedIn = (az account show --output json | ConvertFrom-Json)
if (-not $azureLoggedIn) {
    Write-Host "Azure is not logged in. Please log in to Azure before running this script."
    exit
}

# Step 1: Ask for the Azure Container Registry name
Write-Host "Running Azure Registries:"
az acr list --output-table
$registryName = Read-Host "Enter the name of the Azure Container Registry:"
az acr login --name $registryName

# Step 2: Ask for the Repository Name
$repositoryName = Read-Host "Enter the name of the Azure Container Registry repository (image name):"

# Step 3: Delete ACR Repository, Docker Tag, and Docker Image
Write-Host "Deleting ACR Repository and Docker Image..."
az acr repository delete --name $registryName --repository $repositoryName --yes
Write-Host "{$registryName.azurecr.io/$repositoryName}"
docker rm -f $repositoryName | docker rmi $registryName.azurecr.io/$repositoryName

# Step 4: List Running Docker Containers
Write-Host "Running Containers:"
docker ps -a
$containers = docker ps -a

# Step 5: Prompt the user to input the container ID for deletion

$containerIdToDelete = Read-Host "Enter the ID of the container you want to delete:"

# Check if the user provided a container ID
if ($containerIdToDelete -ne "") {
    Write-Host "Deleting Container $containerIdToDelete..."
    docker stop $containerIdToDelete
    docker rm $containerIdToDelete
    Write-Host "Deletion complete."
} else {
    Write-Host "No container ID provided. Deletion aborted."
}

# Note: The repository name and image name are assumed to be the same in this script.
