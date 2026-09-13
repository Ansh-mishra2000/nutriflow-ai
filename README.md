# 🥗 NutriFlow AI — Cloud-Native AI Nutrition & Food Delivery Platform

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI_0.110+-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB.svg?logo=python&logoColor=white)](https://www.python.org)
[![Docker](https://img.shields.io/badge/Container-Docker-2496ED.svg?logo=docker&logoColor=white)](https://www.docker.com)
[![Kubernetes](https://img.shields.io/badge/Orchestration-Kubernetes_(EKS)-326CE5.svg?logo=kubernetes&logoColor=white)](https://kubernetes.io)
[![Terraform](https://img.shields.io/badge/IaC-Terraform-7B42BC.svg?logo=terraform&logoColor=white)](https://www.terraform.io)
[![Ansible](https://img.shields.io/badge/Automation-Ansible-EE0000.svg?logo=ansible&logoColor=white)](https://www.ansible.com)
[![AWS](https://img.shields.io/badge/Cloud-AWS-232F3E.svg?logo=amazon-aws&logoColor=white)](https://aws.amazon.com)
[![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-2088FF.svg?logo=github-actions&logoColor=white)](https://github.com/features/actions)

> An enterprise-grade, cloud-native nutrition planning and calorie-targeted food delivery platform. NutriFlow AI combines **clinical health algorithms** (BMI, Mifflin-St Jeor BMR, TDEE, macronutrient optimization) and **Generative AI** with a **real-time food delivery lifecycle** and a **production AWS DevOps ecosystem**.

---


## 🔬 Scientific Nutrition & Clinical Health Engine

Unlike basic BMI tools, NutriFlow calculates precise human physiological parameters:

1. **Clinical BMI**: $\text{BMI} = \frac{\text{Weight (kg)}}{(\text{Height (m)})^2}$ classified into Underweight, Normal, Overweight, and Obese categories.
2. **BMR (Mifflin-St Jeor Equation)**:
   $$\text{Men: } (10 \times \text{wt}_{\text{kg}}) + (6.25 \times \text{ht}_{\text{cm}}) - (5 \times \text{age}) + 5$$
   $$\text{Women: } (10 \times \text{wt}_{\text{kg}}) + (6.25 \times \text{ht}_{\text{cm}}) - (5 \times \text{age}) - 161$$
3. **TDEE (Total Daily Energy Expenditure)**: $\text{BMR} \times \text{Activity Multiplier}$ ($1.2$ to $1.9$).
4. **Target Caloric Goal**:
   - **Weight Loss**: $\text{TDEE} - 500\text{ kcal}$ (sustainable $0.5\text{kg/week}$ fat loss).
   - **Muscle Hypertrophy**: $\text{TDEE} + 350\text{ kcal}$ (clean surplus).
   - **Maintenance**: $\text{TDEE}$.
5. **Macro & Meal Distribution**:
   - **Protein**: $1.8\text{--}2.0\text{g per kg}$ to preserve lean mass.
   - **Fats**: $25\%$ of total energy intake ($9\text{ kcal/g}$).
   - **Carbohydrates**: Remaining energy budget ($4\text{ kcal/g}$).
   - **Structured Meals**: Breakfast ($25\%$), Lunch ($35\%$), Dinner ($30\%$), and Snack ($10\%$).

---

## ⚡ Key Features

- 📊 **Interactive Health Dashboard**: Visual gauge meter, BMR/TDEE counters, and macronutrient progress distribution.
- 🍽️ **Algorithmic Meal Recommender**: Intelligent constraint optimization matching delicious recipes to individual caloric goals.
- 🛒 **Calorie-Tracked Ordering**: Direct "Add to Cart" flow that sums total calories and charges accurately.
- 🚚 **Real-Time Delivery Tracker**: Live simulated delivery progression (`PLACED` $\rightarrow$ `PREPARING` $\rightarrow$ `OUT_FOR_DELIVERY` $\rightarrow$ `DELIVERED`).
- 🤖 **AI Nutritionist Assistant**: Integrated Google Gemini API for custom recipe swaps, culinary prep, and personalized macro questions.
- 🏋️ **Goal-Matched Workouts**: Targeted resistance and HIIT exercise routines.

---

## 🛠️ Complete Tech Stack

| Layer | Technologies |
| :--- | :--- |
| **Backend** | Python 3.11+, FastAPI, Pydantic v2, SQLAlchemy, Uvicorn, Pytest |
| **Frontend** | Responsive SPA, HTML5, Tailwind CSS, Lucide Icons, Chart.js |
| **AI / ML** | Google Gemini API (Gemini 2.5 Flash), Scikit-Learn |
| **Database & Cache**| PostgreSQL 16 (Amazon RDS), SQLite (local), Redis 7 |
| **Containers** | Docker (Multi-stage builds), Docker Compose |
| **Orchestration**| Kubernetes (AWS EKS), Ingress ALB, HPA, Deployments, Services |
| **Infrastructure as Code** | Terraform (VPC, EKS, RDS, ECR, S3, IAM) |
| **Configuration Mgmt** | Ansible (Roles for Docker & K8s node bootstrap) |
| **CI / CD Pipeline** | GitHub Actions (Linting, Pytest, ECR Push, EKS Deployment) |

---

## 🚀 Quick Start (Local Execution)

### 1. Run with Python Virtual Environment
```bash
# In project root:
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Start FastAPI server:
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
- Open UI: **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**
- Open Swagger API Docs: **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

### 2. Run Automated Pytest Suite
```bash
PYTHONPATH=backend pytest backend/tests/ -v
```

### 3. Run Full Stack with Docker Compose
```bash
cd devops
docker compose up --build
```

---

## ☁️ Cloud & AWS DevOps Deployment

### 1. Provision Infrastructure with Terraform
```bash
cd devops/terraform
terraform init
terraform plan
terraform apply -auto-approve
```

### 2. Bootstrap Nodes with Ansible
```bash
cd devops/ansible
ansible-playbook -i inventory.ini playbook.yml
```

### 3. Deploy Kubernetes Manifests to AWS EKS
```bash
aws eks update-kubeconfig --name nutriflow-cluster --region us-east-1
kubectl apply -f devops/k8s/namespace.yaml
kubectl apply -f devops/k8s/
kubectl get pods -n nutriflow
```

---

## 📄 CV / Resume Highlights

**Project Title:** Cloud-Native AI Nutrition & Food Delivery Platform  
**Technologies:** Python (FastAPI), React, Tailwind CSS, Google Gemini API, PostgreSQL, Redis, Docker, Kubernetes (EKS), Terraform, Ansible, GitHub Actions, AWS

- Architected a cloud-native microservices platform computing clinical BMI, Mifflin-St Jeor BMR, and TDEE to dynamically prescribe macronutrient-balanced meal plans for Breakfast, Lunch, and Dinner.
- Integrated Google Gemini API for personalized dynamic recipe modifications, dietary constraint validation, and nutritional coaching.
- Built a calorie-tracked food delivery engine featuring real-time order lifecycle tracking, nutrition catalog cards, and automated state transitions.
- Automated 100% of AWS cloud infrastructure (VPC, EKS Cluster, RDS PostgreSQL, ECR, S3) using modular Terraform (IaC) and configured nodes with Ansible.
- Containerized services with Docker and orchestrated high-availability deployments on AWS EKS with Horizontal Pod Autoscaling (HPA) and ALB Ingress.
- Implemented end-to-end CI/CD in GitHub Actions covering automated Pytest execution, container security scanning, Amazon ECR image publishing, and rolling zero-downtime deployments to EKS.
