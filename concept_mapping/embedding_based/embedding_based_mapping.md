# Embedding Based Mapping

Here, we leverage the topic models to identify topics from different domains. We also assume the topics in academic domain to be much larger than the finance domain. So, topics from academic domain are mapped to the finance domain. The steps are mentioned below :
- Each topic is a collection of words. We leveraged GPT-3.5-turbo to get human interpretable label for each topic from both finance and academic domains.
- For every topic we use the collection of its words to get the vector representation using **text-embedding-ada-002** model from OpenAI. 
- The mapping is created using the below steps:
    1. For every Finance topic, we calculate the cosine similarity with every Academic Topic.
    2. Sort the Academic Topics according to the cosine similarity scores with the Finance Topic.
    3. All academic topics which have
        - cosine similarity greater than 0.8
        - a difference of less than 0.03 with previously mapped academic topic.
4. The above process is repeated for every finance topic, resulting in a list of academic topics for every finance topic. 

For example : one of the topics identified in Finance data is **Artificial Intelligence** and using the embedding based mapping we get the mapped academic topics as : **Spiking Neural Networks, Artificial Intelligence, Automation and Human Factors, Business Intelligence, Intelligent Tutoring Systems, Brain Connectivity, Robotics, Brain-Computer Interfaces, Chatbot and Conversational Agents**.


The provided script gets the phrase label for each topic in academic and finance documents and then using heuristics with cosine similarity map research topics to topics in finance.