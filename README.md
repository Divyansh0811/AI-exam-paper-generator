
# Sample Exam Paper Backend API

## Overview
This is a backend API application that allows users to create, read, update, and delete (CRUD) sample exam papers. The application integrates AI capabilities using **Google Gemini**, allowing users to convert natural language inputs into structured JSON schemas that can be passed to the APIs. Additionally, the application can extract data from PDF files and generate JSON structures for easier integration with other systems.

### Key Features:
- **CRUD Operations**: Perform basic create, read, update, and delete operations on exam papers.
- **AI Integration**: Uses Google Gemini (LLM) to convert natural language inputs into JSON schemas.
- **PDF Data Extraction**: Extracts structured data from PDFs and converts it into a JSON schema.
- **Asynchronous Task Handling**: Async tasks are managed using **Celery** to ensure smooth and non-blocking execution of long-running tasks.
- **Data Validation**: Inputs are validated using **Pydantic**, ensuring proper data structures before interacting with the system.
- **Reverse Proxy**: The application uses **NGINX** as a reverse proxy to handle load balancing and rate limiting.

## Security
Security has been a key consideration throughout the application. Several layers of protection are implemented, both at the application and cloud infrastructure levels.

- **Rate Limiting**: Implemented at the reverse proxy level (NGINX) to protect the application from denial-of-service (DoS) attacks.
- **Server Version Hiding**: The NGINX server version is hidden to prevent potential attackers from gaining information about the server.
- **Data Sanitization**: All inputs are sanitized before being stored in the database to prevent injection attacks like **Stored XSS**.
- **CORS (Cross-Origin Resource Sharing)**: APIs are restricted to known origins, preventing unauthorized domains from accessing the API.
- **Protection Against Attacks**: The system is designed to defend against common vulnerabilities, such as **Stored XSS** and **DDoS**.

## Cloud Architecture (AWS EKS)
The API is designed to be deployed on cloud platforms like **AWS** using **Kubernetes (EKS)**. The potential cloud architecture includes the following elements:

- **Private Subnets**: Both the application and the database are hosted in private subnets, ensuring they are not exposed directly to the internet.
- **Security Groups & NACLs**: Security groups and NACLs (Network Access Control Lists) are used to restrict access at both the instance and subnet levels, allowing only necessary traffic.
- **High Availability & reliability**: Multiple NAT Gateways are deployed in multiple AZs to make our service highly available and autoscaling can also be implemented.
- **SSH Access**: Ports such as **SSH** (port 22) are opened only for internal network access.
- **Daily Backups**: Regular daily database backups are essential to ensure data availability in case of failure.
- **Auto-Scaling**: Autoscaling is configured based on CPU and memory metrics to handle varying loads effectively.
- **Tools**: Use tools like eksctl, kubectl to communicate with the K8s API server and create the architecture in AWS EKS
- and much more...
### Cloud Architecture Diagram: [View here](https://drive.google.com/file/d/1HTe5B4Gr8l7xsGgyGVsuVfaPfxqyu-PK/view?usp=sharing)
![K8s_architecture_Template](https://github.com/user-attachments/assets/71c74c48-75b4-4b0b-a1c0-e2d34f55a8ea)


## Running the Application Locally (Using Docker Compose)

### Prerequisites
- Docker
- Docker Compose

### Steps to Run Locally

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-repository.git
   cd your-repository
   ```

2. **Generate Google Gemini API Key**:
   To integrate the AI functionality, you need to generate an API key from **Google Gemini**.

   - Go to [https://gemini.google.com/](https://gemini.google.com/).
   - Click on **For Developers** from the top navbar, and you will be redirected to [Google AI Developer](https://ai.google.dev/).
   - Click on **Get API Key** in the Google AI Studio.
   - Then, click on **Create API Key**, and your API key will be generated.
   - Store this key safely as you'll need to set it in the environment variables.

3. **Build and Run Using Docker Compose**:
   - Use `docker-compose` to build and start all the necessary services, including FastAPI, MongoDB, Redis, Celery, and NGINX.

   Run the following command to build and start the containers:
   ```bash
   docker-compose up --build
   ```

4. **Access the API**:
   Once the services are up and running, you can access the API at:
   ```
   http://localhost
   ```

5. **Celery Workers**:
   Celery workers will automatically be started by the `docker-compose` setup to handle async tasks.

6. **NGINX Reverse Proxy**:
   NGINX is configured to handle all incoming requests and proxy them to the FastAPI application running on port 8000.

7. **Tear Down**:
   To stop and remove all running containers:
   ```bash
   docker-compose down
   ```

## Testing
Use **pytest** to run your tests. Note that while the tests cover core functionalities, they are not fully comprehensive at this point. However, the application has been manually tested.

```bash
pytest
```

## Deployment
If deploying on AWS EKS:
- Ensure the cluster is set up with the necessary **autoscaling** based on CPU and memory using a metrics server.
- Use **CloudWatch or self-hosted Kube Prometheus monitoring stack** to monitor the system and set up alerts for CPU, memory, and disk space metrics.
- Make sure that **daily backups** are enabled for MongoDB.
- Manage security groups and NACLs to ensure minimal exposure to the public internet.

## Limitations & Future Work
- **Testing**: The current test coverage is limited, and not all edge cases are covered. Manual testing has been performed to ensure core functionality.
- **Further Security Enhancements**: In the future, additional security features like IP whitelisting, detailed audit logging, and role-based access control (RBAC) could be implemented.

## Conclusion
This backend API application is designed to create and manage sample exam papers, leveraging AI to simplify input generation. Security and scalability have been prioritized in the architecture, ensuring the application is ready for deployment in a production environment with cloud-native technologies.
```
