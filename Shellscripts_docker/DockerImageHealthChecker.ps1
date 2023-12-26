# Specify the Docker image name and tag
$DOCKER_IMAGE = READ-HOST "your-docker-image:latest"

# Run Trivy to scan the Docker image for vulnerabilities
Write-Host "Running security scan for vulnerabilities in $DOCKER_IMAGE..."
trivy --ignore-unfixed --severity HIGH,MEDIUM --no-progress $DOCKER_IMAGE

# Check Trivy exit code to determine if vulnerabilities were found
$TRIVY_EXIT_CODE = $LASTEXITCODE

# Display results based on Trivy exit code
if ($TRIVY_EXIT_CODE -eq 0) {
    Write-Host "No vulnerabilities found."
}
elseif ($TRIVY_EXIT_CODE -eq 1) {
    Write-Host "Vulnerabilities found. Please review the report above."
}
else {
    Write-Host "Trivy encountered an error during the scan."
}
# Save the severity report as a table in a file
trivy image --format table your-docker-image:tag > trivy_report.txt

# Exit with Trivy exit code
exit $TRIVY_EXIT_CODE
