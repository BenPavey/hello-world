import os
import psutil
import subprocess
from django.shortcuts import render


from django.http import HttpResponse
from django.conf import settings
import logging






import os
from django.http import JsonResponse
from django.conf import settings
from django.core.files.storage import default_storage

def debug_static_files(request):
    # Check static files storage backend
    storage_backend = settings.STATICFILES_STORAGE
    
    # Check GCS Bucket Name
    bucket_name = getattr(settings, "GS_BUCKET_NAME", "Not Set")
    
    # Check if environment variables are set
    gcp_key_base64 = os.getenv("GCP_KEY_BASE64", "Not Set")
    google_credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "Not Set")

    # Test file upload
    test_file_path = "test-static-django.txt"
    try:
        with default_storage.open(test_file_path, "w") as f:
            f.write("This is a test file uploaded via Django's storage system.")
        file_exists = default_storage.exists(test_file_path)
    except Exception as e:
        file_exists = f"Error: {str(e)}"

    return JsonResponse({
        "STATICFILES_STORAGE": storage_backend,
        "GS_BUCKET_NAME": bucket_name,
        "GCP_KEY_BASE64_Set": gcp_key_base64 != "Not Set",
        "GOOGLE_APPLICATION_CREDENTIALS": google_credentials_path,
        "Test File Uploaded": file_exists,
    })







def get_running_port(request):
    """Retrieve the port Django is running on."""
    host = request.get_host()
    if ":" in host:
        return host.split(":")[-1]  # Extract the port number
    return "8000"  # Default Django port

def get_server_type():
    """Detect if running on a physical machine, cloud instance, or Kubernetes."""
    if os.path.exists("/.dockerenv"):
        return "Docker Container"
    elif os.getenv("KUBERNETES_SERVICE_HOST"):
        return "Kubernetes Node"
    elif "RENDER" in os.environ:
        return "Render Web Service"
    elif "GCP_PROJECT" in os.environ:
        return "GCP Cloud Instance"
    return "Physical Machine"

def get_system_specs():
    """Fetch high-level system specs (CPU Cores, RAM)."""
    return {
        "cpu_cores": psutil.cpu_count(logical=True),  # Total logical CPU cores
        "total_memory": round(psutil.virtual_memory().total / (1024 ** 2)),  # Convert to MB
    }

def get_app_metrics():
    """Fetch app resource usage with % of total system capacity."""
    process = psutil.Process(os.getpid())  # Get the Django process
    app_cpu_usage = process.cpu_percent(interval=1)  # App CPU usage in %
    app_memory_usage = process.memory_info().rss / (1024 ** 2)  # Convert to MB
    total_memory = psutil.virtual_memory().total / (1024 ** 2)

    # Calculate usage as % of total system resources
    app_memory_percent = (app_memory_usage / total_memory) * 100 if total_memory else 0

    return {
        "app_cpu_usage": f"{app_cpu_usage:.1f}%",
        "app_memory_usage": f"{app_memory_usage:.2f} MB ({app_memory_percent:.2f}%)",
    }
def get_docker_image():
    """Get the Docker image of the running container (only if inside Docker)."""
    try:
        if is_running_in_docker():
            image_id = subprocess.check_output(
                "docker inspect -f '{{.Config.Image}}' $(hostname)", shell=True, text=True
            ).strip()
            return image_id
        return "Not running inside Docker"
    except Exception:
        return "Unknown"

def get_local_docker_containers():
    """List all running Docker container images (even if Django isn't in Docker)."""
    try:
        output = subprocess.check_output(
            "docker ps --format '{{.Image}}'", shell=True, text=True
        ).strip()
        return output if output else "No running containers"
    except Exception:
        return "Docker not installed or not running"

def get_kubernetes_pod_count():
    """Get the number of active Kubernetes pods (if running in Kubernetes)."""
    try:
        pod_count = subprocess.check_output(
            "kubectl get pods --no-headers | wc -l", shell=True, text=True
        ).strip()
        return pod_count
    except Exception:
        return "Not in Kubernetes"

def is_running_in_docker():
    """Detect if the app is running inside a Docker container."""
    return os.path.exists("/.dockerenv")

def is_bare_metal():
    """Detect if running on a physical machine, Docker, or Kubernetes."""
    if os.path.exists("/.dockerenv"):
        return "Running in Docker"
    elif os.getenv("KUBERNETES_SERVICE_HOST"):
        return "Running in Kubernetes"
    return "Physical Server"

def get_deployment_details():
    """Fetch deployment-related details like Docker image and Kubernetes pods."""
    docker_image = "Not running in a container"
    docker_containers = "Not applicable"
    kubernetes_pods = "Not in Kubernetes"

    # Detect if inside Docker
    if os.path.exists("/.dockerenv"):
        docker_image = subprocess.getoutput("docker inspect -f '{{.Config.Image}}' $(hostname)") or "Unknown Docker Image"

    # List running Docker containers (Handle Docker not running error)
    try:
        docker_output = subprocess.getoutput("docker ps --format '{{.Image}}'")
        if "Cannot connect to the Docker daemon" in docker_output:
            docker_containers = "Docker not running or unavailable"
        else:
            docker_containers = docker_output or "No running containers"
    except Exception:
        docker_containers = "Docker not installed"

    # Kubernetes pod count (Handle errors)
    if os.getenv("KUBERNETES_SERVICE_HOST"):
        try:
            kubernetes_pods = subprocess.getoutput("kubectl get pods --no-headers | wc -l").strip() or "0"
        except Exception:
            kubernetes_pods = "Error retrieving pod count"

    return {
        "docker_image": docker_image,
        "local_docker_containers": docker_containers,
        "kubernetes_pods": kubernetes_pods,
    }

def home(request):
    context = {
        "server_type": get_server_type(),
        "running_port": get_running_port(request),  # Add the port to context
        **get_system_specs(),  # CPU Cores & RAM
        **get_app_metrics(),  # App Usage
        **get_deployment_details(),  # Docker image & Kubernetes pods
    }

    return render(request, "hello_app/index.html", context)