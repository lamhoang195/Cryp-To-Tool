
## Getting Started 🚀

### Prerequisites
- Install Docker: [Download and Install Docker](https://docs.docker.com/get-docker/)

---

### Pull the Docker Image and run

Run the following command to pull the image from Docker Hub:
```bash
docker pull tuanjhg/crytotool

After pulling the image, run the container using:
docker run -d -p 5000:5000 tuanjhg/crytotool
Open your browser and navigate to:
http://localhost:5000
###If you want to run the application locally instead of using Docker:

git clone https://github.com/lamhoang195/Cryp-To-Tool.git
cd Cryp-To-Tool

Install dependencies:
pip install -r requirements.txt
Run the app:
flask run


| Student ID |     Full Name     |
|:----------:|:------------------|
|  22028150  | Lê Bá Hoàng       |
|  22028167  | Khổng Mạnh Tuấn   |


|    # | Name                           | Description                                           | Key length (bits) (\*) | 
|:----:|:-------------------------------|:------------------------------------------------------|:-----------------------|
|    1 | CryptoRSA                      | RSA Cipher                                            |          4096          | 
|    2 | CryptoElGamal                  | ElGamal Cipher                                        |          4096          | 
|    3 | CryptoECElGamal                | EC-ElGamal Cipher                                     |          29            |   
|    4 | CryptoRSA_SignatureRSA         | RSA Cipher and Signature System combined              |          4096          |     
|    5 | CryptoElGamal_SignatureElGamal | ElGamal Cipher and ElGamal Signature System combined  |          1024          |   
|    6 | CryptoECElGamal_SignatureECDSA | EC-ElGamal Cipher and ECDSA Signature System combined |          29            |   
      


