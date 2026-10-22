# CCA 2 CI/CD — Student Task Manager

A small Flask web application prepared as a learning starter for a Jenkins → Docker Hub → Kubernetes/Minikube pipeline.

**Academic note:** Your CCA 2 guide asks for an existing academic project. This starter was newly prepared; confirm with your faculty that it is acceptable before submitting it as an existing project.

## Files
- `app.py`: task manager with add/complete/delete actions and `/health`
- `tests/`: pytest tests
- `Dockerfile`: container build
- `Jenkinsfile`: checkout, test, build, push and deploy stages
- `k8s/deployment.yaml`, `k8s/service.yaml`: Kubernetes manifests

## 1. Run locally on Windows
Install Python 3.11+ and Git. Open PowerShell in this folder:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
pytest -q
python app.py
```

Open `http://localhost:5000`. Health endpoint: `http://localhost:5000/health`.

If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in that terminal and retry.

## 2. Push to GitHub
Create an empty GitHub repository named `cca2-student-task-manager`, then run in this folder:

```powershell
git init
git add .
git commit -m "Initial CCA 2 task manager project"
git branch -M main
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/cca2-student-task-manager.git
git push -u origin main
```

Replace `YOUR_GITHUB_USERNAME`. If the remote already exists, use `git remote set-url origin https://github.com/YOUR_GITHUB_USERNAME/cca2-student-task-manager.git`.

## 3. Test with Docker
Install and start Docker Desktop:

```powershell
docker build -t YOUR_DOCKERHUB_USERNAME/cca2-student-task-manager:latest .
docker run --rm -p 5000:5000 YOUR_DOCKERHUB_USERNAME/cca2-student-task-manager:latest
```

Open `http://localhost:5000`; stop the container with Ctrl+C. Replace the Docker Hub placeholder with your username.

## 4. Docker Hub
Create a Docker Hub account and repository named `cca2-student-task-manager`. Create an access token. Never commit passwords or tokens to GitHub.

## 5. Jenkins and Minikube prerequisites
The Jenkinsfile expects a Linux Jenkins agent with `git`, `python3`, `python3-venv`, `pip`, `docker`, `kubectl`, and a working Minikube context. Docker and Kubernetes access must work as the Jenkins service account.

The CCA 2 guide describes Jenkins hosted on AWS. Install Jenkins on an AWS Linux EC2 instance according to your lab instructions, restrict access to its web UI, and ensure the agent has Docker and the intended Minikube cluster configured. Minikube in a cloud VM may require a compatible driver and sufficient CPU/RAM; this ZIP cannot create AWS resources or configure your account automatically.

### Jenkins configuration
1. Install Jenkins plugins: Pipeline, Git, and Credentials Binding.
2. In **Manage Jenkins → Credentials**, add **Username with password**:
   - ID: `dockerhub-credentials`
   - Username: your Docker Hub username
   - Password: your Docker Hub access token
3. Edit `Jenkinsfile` and replace `YOUR_DOCKERHUB_USERNAME` in `IMAGE_NAME`.
4. Commit and push that change.
5. Create a Jenkins **Pipeline** job → **Pipeline script from SCM** → Git → repository URL → branch `*/main` → script path `Jenkinsfile`.
6. Click **Build Now** and inspect Console Output.

The deploy stage runs `kubectl` on the Jenkins agent. A Minikube cluster on your Windows PC is not automatically accessible to Jenkins on AWS.

## 6. Verify deployment
On a terminal configured for the target cluster:

```bash
kubectl get pods
kubectl get deployments
kubectl get services
kubectl rollout status deployment/cca2-student-task-manager
kubectl port-forward service/cca2-student-task-manager 8080:80
```

Keep port-forward running and open `http://localhost:8080`. Health check: `http://localhost:8080/health`.

## 7. Mandatory second-run demonstration
After the first successful pipeline, change the visible banner in `app.py`, for example from `CCA 2 • CI/CD Demonstration Application` to `CCA 2 • CI/CD Demonstration Application — Version 2`. Then:

```powershell
git add app.py
git commit -m "Update app for redeployment demo"
git push
```

Run the Jenkins job again (or configure a GitHub webhook if required by your lab). Verify the changed text in the deployed app and capture screenshots from both runs.

## Screenshots to submit
1. GitHub repository with source and required files.
2. Jenkins pipeline stages successful.
3. Console output showing tests and Docker push.
4. Docker Hub repository and image tags.
5. `kubectl get pods`, deployments and services.
6. Running app in browser.
7. Source change and successful second pipeline run.

## Troubleshooting
- **Docker permission denied:** grant the Jenkins service account appropriate Docker daemon access and restart Jenkins.
- **pytest not found:** ensure the pipeline activates `.venv` and installs `requirements-dev.txt`.
- **Docker push denied:** confirm repository exists, token is valid, and credential ID is exactly `dockerhub-credentials`.
- **ImagePullBackOff:** check image name/tag, successful push, and public repository or pull credentials.
- **kubectl cannot connect:** check `kubectl config current-context` and configure the Jenkins agent for the intended Minikube cluster.
- **Rollout timeout:** run `kubectl describe pods` and `kubectl logs deployment/cca2-student-task-manager`.

## Pipeline flow
GitHub checkout → dependencies and pytest → Docker build → push versioned image → apply Kubernetes manifests → rollout check.

## Viva points
- **CI:** automated integration checks and tests.
- **CD:** packaging and deploying tested changes.
- **Jenkinsfile:** pipeline-as-code stored with the project.
- **Docker image:** portable package with application and dependencies.
- **Deployment:** maintains the desired number of Pods.
- **Service:** stable network endpoint for Pods.
- **Minikube:** Kubernetes cluster for lab/local deployment.
- **Second run:** demonstrates a code change passing through the pipeline.

## Submission checklist
- [ ] GitHub repository URL
- [ ] Jenkinsfile
- [ ] Dockerfile
- [ ] Kubernetes Deployment and Service YAML
- [ ] Screenshots
- [ ] README/report explaining setup, stages, image push, app access and second run
