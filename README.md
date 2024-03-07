# Chatbot for Mexico City Traffic Regulations with OpenAI LLM, RAG, and LangChain.

This repository contains code to create a chatbot specialized in Mexico City traffic regulations using OpenAI's Large Language Model (LLM), Retrieval Augmented Generation (RAG), and LangChain. The chatbot is designed to process information from PDF files, specifically the Official Traffic Regulations of Mexico City and websites of the Secretary of Mobility of Mexico City (JSON files).

To use this repository, you will need an OpenAI secret key, which you can create in the following link with your OpenAI account: [OpenAI Platform](https://platform.openai.com/account/api-keys)


## Setup instructions:

Clone the repository:
```
git clone git@github.com:TeresitaJG/Chatbot-gpt.git
```

Create a new environment:
```
pyenv virtualenv chatbot
```

In the project directory, specify the virtual environment for the project:
```
pyenv local chatbot
```

Install the required libraries:

```
pip install -r requirements.txt
```

### Setting up Raw Data
Download the `raw_data` folder containing the required PDF and JSON files from [this link](https://drive.google.com/drive/folders/1kESy-hniU9WLsiiAB3aBNHBvWp3bNsq4?usp=sharing). Place the `raw_data` folder into the root directory of the project.

Run the `urls_vectorstore.py` file within the `model` folder. This script creates and populates a FAISS vector store with documents from the downloaded PDF file and a JSON file, returning a FAISS vector store containing embeddings of the documents.

## Running the Application Locally

### Endpoints
The `api_chat.py` file within the `api` folder contains three endpoints:

- `/responseChatbot`: Runs the chatbot.
- `/clearHistory`: Clears the message history and avoids exceeding the token limit.
- `/`: Root endpoint for testing purposes.

### Testing the Application Locally

To test the application locally, first, run the uvicorn server:
```
make run_api
```````

Then, visit [http://localhost:8000/](http://localhost:8000/) in your browser to test the root endpoint.

If the application is working correctly, it should show the following response:

```
{
    'greeting': 'Hello'
}
```

Once the server is running, go to the `v2_api_test.py` file within the `tests` folder and run it. You can start writing questions for the chatbot in the terminal when prompted.

To stop the application, use `Ctrl + C` in the terminal where the application is running.

## Deployment with Docker

Create the `.env` file and use the `.env.sample` as a template.

Build the Docker image:
```
docker build --tag=$IMAGE:dev .
```
Run the API in Docker:
```
docker run -it -e PORT=8000 -p 8000:8000 --env-file .env $IMAGE:dev
```
The API should respond in your browser, go visit it. Also, you can check if the image runs with `docker ps` in a new Terminal tab or window.

You can stop the Docker container using docker container `stop <CONTAINER_ID>`.


## Pushing the Docker Image to Google Container Registry

Enable the [Google Cloud Container Registry API](https://console.cloud.google.com/flows/enableapi?apiid=containerregistry.googleapis.com&redirect=https://cloud.google.com/container-registry/docs/quickstart) for your project in GCP.

Configure `docker` to push the image to GCP:
```
gcloud auth configure-docker
```
Build the image again:
```
docker build -t  $GCR_REGION/$GCP_PROJECT/$IMAGE:prod .
```

Run the image to ensure it works correctly:
```
docker run -e PORT=8000 -p 8000:8000 --env-file .env $GCR_REGION/$GCP_PROJECT/$IMAGE:prod
```
Push the image to Google Container Registry:
```
docker push $GCR_REGION/$GCP_PROJECT/$IMAGE:prod
```
The image should be visible in the [GCP console](https://console.cloud.google.com/gcr/).


## Deploying the Container Registry Image to Google Cloud Run

Create a `.env.yaml` file containing all the necessary environment variables in the YAML format.
Use the `.env.yaml.sample` file as an example.

Run the deployment command:'
``````
gcloud run deploy --image $GCR_REGION/$GCP_PROJECT/$IMAGE:prod --memory $GCR_MEMORY --region $GCP_REGION --env-vars-file .env.yaml
``````
After confirmation, the service should be live, and you can access it at the provided URL.

Keep in mind that you pay for the service as long as it is up.



## Front-end Repository

For the front-end interface of this chatbot, please refer to the [Justice4EveryoneProject](https://github.com/TfRocio/Justice4EveryoneProject) repository. It provides the user interface to interact with the chatbot and complements the functionality provided by this back-end.
