# 🧩 **ShikshaGPT - AI Chat Bot for Science-Related Questions**

# Introduction
Welcome to the documentation of the customized chat bot developed for science-related questions aka the science bot. This document outlines the journey and key components of the project, from requirements to implementation. The outcome of this project developed is to handle scientific questions intelligibly by a bot and provide the best possible answer to it.

# How to run?
**Download and install all the dependencies –**

•	I have provided the requirement.txt file

•	Download the Llama quantized model from https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML/blob/main/llama-2-7b-chat.ggmlv3.q8_0.bin 

•	We can run the server on port 5500 locally by using the start.sh script or within a Docker container using the Dockerfile. (Backend setup - users can access the bot through backend at port 5500)

•	To run the UI interface built with the help of Chainlit go to ur environment terminal and type - "chainlit run test,py -w". (Frontend setup - users can access the bot through this instruction)

# Directory Structure
The project structure is organized as follows:

* main.py: The main application file handling the Flask server (introduced by me), request processing, and response generation.
* simple_text.py: Defines the SimpleText class and its schema using Marshmallow.
* ignite.py: Launches the Flask server.
* datastore/: Contains state information (state.json) and individual query data (query_id.json) in a structured format.
* vectorstore/: (additional directory) Contains the generated embeddings of the texts in vector format.
* preprocessing.py: This file was introduced by me (additional file) for document loading and text splitting contributing towards overall text preprocessing of data.
* test.py: This file was introduced by me (additional file). This file contains the logic behind our large language model in which the input query is processed to obtain the desired results through our model.

# Implementation Steps

**1. Understanding the Test**

The initial step involved thoroughly understanding the provided test description, including mission, ground rules, and deployment options. I had to first go through openfabric documentation (https://docs.openfabric.ai/developer-tools/index/) to understand the underlying data structures, classes and functions inside the project directory.

**2. Framework Selection**

The project utilizes the Openfabric PySDK for interacting with the Openfabric platform and handling execution context.

**3. Text Preprocessing**

For this step I have introduced a new file known as preprocessing.py. In this file, I have leveraged the might of Langchain. Firstly, we load the data that is stored in the data/ folder in pdf format using PyPDFLoader and DirectoryLoader. Next, we use RecursiveCharacterTextSplitter from langchain to split the text into chunks. Next, after splitting the text we pass it into the sentence-transformer model from the HuggingFaceEmbeddings dependency which generates embeddings for our text data.
To store these embeddings in text format I used FAISS module.

Code snippet – 

![image](https://github.com/prajwalnayak17/Shiksha_GPT/assets/87718913/74cbe6d0-15af-4718-a2a0-c99e4fc81d6f)

   
To generate these vector stores before executing our script we need to run this preprocessing.py file to generate the vector stores.
Output - 

![image](https://github.com/prajwalnayak17/Shiksha_GPT/assets/87718913/df8b240b-5761-4d1f-aaa8-1ffcf4f8567b)


These files must be generated.

**4. Coding the execute Function**

The core of the application is the execute function in main.py. This function processes incoming requests, handles each query, and generates appropriate responses. 
To design this function firstly I introduced another function called handle_request(). Using flask I developed this function to handle incoming request to the server and pass it onto the execute function to collect the response.
 
Code snippet -  

![image](https://github.com/prajwalnayak17/Shiksha_GPT/assets/87718913/240395eb-bfef-4875-8c8b-e2e45df74e88)


Here we can see when we pass data into the execute function we declare a none ray class and an empty state class with default values being empty.
Next, I wrote a function to generate 32-character length of random alphanumeric data for our session and query ids.

Code snippet – 

![image](https://github.com/prajwalnayak17/Shiksha_GPT/assets/87718913/afe1d175-c87e-47a7-90c0-e6146323c38c)


Finally, I dove into the execute function in which I setup ray class for each query having unique query and session ids. Then I iterated through each query in the request consisting of a list of queries. For each query processing is done and response is collected by passing it onto the final_result function.

Code snippet – 

![image](https://github.com/prajwalnayak17/Shiksha_GPT/assets/87718913/f809fcf0-6b02-48c6-8ccf-5c6d3f166daa)

 
The datastore also gets updated in this function in which a unique query_id.json file is stored and the state.json file is updated.
Finally the function returns the output in a dictionary format of the SchemaUtilclass through simpleText function.

Code snippet – 

![image](https://github.com/prajwalnayak17/Shiksha_GPT/assets/87718913/8f9a3590-45ba-4de5-9ab9-13887ab72859)

 
**5. Integration with Custom Model (test.py)**

The model.py file contains the implementation of the custom chat bot model. It leverages language models for question answering, embeddings, and a vector store for efficient retrieval.
So, when the final_result() function in execute function of main.py file is run we come to this file, the test.py file.

**Step 1 – Defining a custom prompt template and a function to set it up**

![image](https://github.com/prajwalnayak17/Shiksha_GPT/assets/87718913/9a7aac3b-d54b-4646-a003-633ab7005160)

 
**Step 2 – Defining the retrieval QA chain function**

In this function a chain of events is run in order to retrieve the correct information for our response. This can be better explained with the diagram given below
Diagram – 

![image](https://github.com/prajwalnayak17/Shiksha_GPT/assets/87718913/3fb28224-367f-4bde-96a5-2fd2b46ef183)


Here you can see that on passing the query the qa retrieval function gets activated. It goes into our docs or data that we have provided. Then after getting multiple sources. It uses LLMChain model to retrieve the useful information to form the response and finally using ctransformers we load the answer.

**Step 3 – Loading the model**

For this project I have used the quantized version of the Llama 2, 7 billion bytes quantization model. This quantized version was downloaded from “TheBloke/Llama-2-7B-Chat-GGML”.  

Code snippet – 

![image](https://github.com/prajwalnayak17/Shiksha_GPT/assets/87718913/2c557752-3f01-4e56-a36d-4b660672f52c)


Defining the Question Answer model function

Code snippet – 

![image](https://github.com/prajwalnayak17/Shiksha_GPT/assets/87718913/adf9d4db-4f36-4c0a-bf9a-cb5adfddf79e)


Combining everything to form the output function

![image](https://github.com/prajwalnayak17/Shiksha_GPT/assets/87718913/bb44c599-3659-4d15-a5aa-38aa638c07f7)


**6. Error Handling**
Error handling was implemented within the execute function to gracefully manage errors during query processing. The messages attribute in the ray class was updated with error details.

Code snippet – 

![image](https://github.com/prajwalnayak17/Shiksha_GPT/assets/87718913/d7c5e3f5-f230-492d-baa9-f569190842e3)


**7. State Management**

The state.json file in the datastore/ directory is used to track the status of each query, including queued, requested, and completed queries. The state is updated at various stages of query processing.

**8. Output Storage**

The output of each query, along with relevant information, is stored in a separate file (query_id.json) within the datastore/queries/ directory.

**9. Output**

Output – 

![image](https://github.com/prajwalnayak17/Shiksha_GPT/assets/87718913/e53b909d-8e86-4956-b2f0-33fba37e553c)


In this snippet you can see we have used postman to generate the response for 3 queries passed into the request body in json format.
 
**10. UI Interface**

By leveraging the functionalities of chainlit I have developed a custom code for our bot’s user interface. 
To see a working UI through chainlit go to ur environment terminal and type - "chainlit run test,py -w"

Code snippet – 

![image](https://github.com/prajwalnayak17/Shiksha_GPT/assets/87718913/609d417b-4687-410c-a4d6-6c5f3ae44925)


![image](https://github.com/prajwalnayak17/Shiksha_GPT/assets/87718913/e2ae329d-1f91-45c9-a084-1c109c963100)


![image](https://github.com/prajwalnayak17/Shiksha_GPT/assets/87718913/b48922f5-1721-4207-964f-408de95e625d)


![image](https://github.com/prajwalnayak17/Shiksha_GPT/assets/87718913/fd68b6b3-a036-4dcc-a24b-42c49ab64a3c)




# Important links:
Docs of openfabric_pysdk - https://docs.openfabric.ai/developer-tools/index/

Langchain docs - https://python.langchain.com/docs/get_started/introduction

Chainlit docs – 
https://github.com/Chainlit/chainlit

Ctransformers docs – 
https://github.com/marella/ctransformers
