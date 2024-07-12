Running terraform module without real cloud services
---
<img width="1729" alt="image" src="https://github.com/user-attachments/assets/da03b474-4294-4e68-badc-18a8476fdd3c">

Mock services
---
add more services in cloud_services, azure/aws/gcp etc

Test
---
````
export https_proxy=http://localhost:8081  
cd test/terraform  
terraform init   
terraform apply --auto-approve
````



