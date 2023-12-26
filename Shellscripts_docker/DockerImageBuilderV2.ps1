# Step 0: Check Azure login
$azureLoggedIn = (az account show --output json | ConvertFrom-Json)
if (-not $azureLoggedIn) {
    Write-Host "Azure is not logged in. Please log in to Azure before running this script."
    exit
}

# Step 1: List Docker Images
Write-Host "Available Docker Images:"
docker images

# Step 2: Ask for User Input (Image Name)
$imageName = Read-Host "Enter the name of the Docker image you want to use (or specify a new image name):"

# Check if the image exists
if (-not (docker images -q $imageName)) {
    # Step 3: Ask for Dockerfile Path
    do {
        $dockerfilePath = Read-Host "Enter the path to the Dockerfile (e.g., 'C:\path\to\Dockerfile'):"
    } until (Test-Path $dockerfilePath)

    # Step 4: Change Current Directory and Build Docker Image
    $currentDir = (Get-Location).Path
    Set-Location (Split-Path -Path $dockerfilePath -Parent)
    docker build --no-cache -t $imageName -f $dockerfilePath .

    # Step 5: Change Back to the Original Directory
    Set-Location $currentDir
}


# Step 4: Azure Container Login (Assuming the user is already logged in)
$registryName = Read-Host "Enter the name of the Azure Container Registry:"
az acr login --name $registryName

# Step 5: Tag, Push, and Run the Container
$taggedImage = "$registryName.azurecr.io/$imageName"
docker tag $imageName $taggedImage
docker push $taggedImage
docker run -d $taggedImage

# Step 6: Print Running Containers and Live Log the New Container
Write-Host "Running Containers:"
docker ps -a

# Get the ID of the newly created container
$containerId = (docker ps --format "{{.ID}}" | Select-Object -First 1)

Write-Host "Live Logging Container ${$containerId}:"
docker logs -f $containerId
