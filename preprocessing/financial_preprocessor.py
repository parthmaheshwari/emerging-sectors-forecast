import nltk
import re
import spacy
from nltk.corpus import stopwords


# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

nltk.download('punkt')
nltk.download('stopwords')

def preprocess_descriptions(text):
    """
    Preprocesses a given text description by performing various text cleaning operations.

    Args:
        text (str): The input text description to be preprocessed.

    Returns:
        str: The preprocessed and cleaned text description.

    The function performs the following preprocessing steps:
    1. Tokenizes the input text using a spaCy model (nlp).
    2. Removes tokens with entity types "PERSON" or "ORG" and tokens with part-of-speech "VERB."
    3. Joins the cleaned tokens back into a text string.
    4. Removes HTML tags and URLs from the text using regular expressions.
    5. Removes non-alphabetic characters and converts the text to lowercase.
    6. Removes specific strings (e.g., common company-related terms) from the text.

    Note: Stopword removal is commented out because BERTopic performs a similar operation.

    Example:
    >> input_text = "ABC Inc. is a technology company providing solutions. Visit www.abc.com for more info."
    >> preprocessed_text = preprocess_descriptions(input_text)
    >> print(preprocessed_text)
    "abc is a providing for more info"
    """
    nlp.max_length = 5_000_000  # Set the maximum document length for spaCy processing.
    doc = nlp(text)
    cleaned_text = []

    for token in doc:
        if token.ent_type_ not in ["PERSON", "ORG"] and token.pos_ != "VERB":
            cleaned_text.append(token.text)

    description = ' '.join(cleaned_text)

    description = re.sub(r'<.*?>', '', description)  # Remove HTML tags.
    description = re.sub(r'http\S+|www\S+|https\S+', '', description, flags=re.MULTILINE)  # Remove URLs.
    description = re.sub(r'[^a-zA-Z\s]', '', description)  # Remove non-alphabetic characters.

    description = description.lower()  # Convert text to lowercase.

    # Remove specific strings commonly found in company descriptions.
    strings_to_remove = ["inc", "llc", "group", "holdings", "co", "inc.", "holding", "partners", "ltd",
                         "united states", "based", "technology", "solutions", "provider", "company", "platform"]
    description = re.sub(r"\b(" + "|".join(strings_to_remove) + r")\b", "", description)

    # Stopword removal (disabled, as BERTopic performs a similar operation)
    # tokens = nltk.word_tokenize(description)
    # stop_words = set(stopwords.words('english'))
    # tokens = [token for token in tokens if token not in stop_words]
    # description = ' '.join(tokens)

    return description



def preprocess_abstracts(abstract):
    """
    Preprocesses an abstract by applying various text cleaning and normalization steps.

    Args:
        abstract (str): The input abstract text to be preprocessed.

    Returns:
        str: The preprocessed abstract text after applying cleaning and normalization.

    The preprocessing steps include:
    1. Removing HTML tags and content enclosed within angle brackets.
    2. Removing URLs and web links (starting with 'http', 'www', or 'https').
    3. Removing non-alphabetic characters and keeping only letters and spaces.
    4. Converting the text to lowercase.
    5. Tokenizing the text into words.
    6. Removing common English stopwords.
    7. Rejoining the tokens to form a cleaned and normalized abstract.

    Example:
    >> input_abstract = "This is a <p>sample</p> abstract with a URL http://example.com."
    >> preprocessed_abstract = preprocess_abstracts(input_abstract)
    >> print(preprocessed_abstract)
    "sample abstract url"
    """
    # Step 1: Remove HTML tags and content within angle brackets
    abstract = re.sub(r'<.*?>', '', abstract)
    
    # Step 2: Remove URLs and web links
    abstract = re.sub(r'http\S+|www\S+|https\S+', '', abstract, flags=re.MULTILINE)
    
    # Step 3: Remove non-alphabetic characters and keep letters and spaces
    abstract = re.sub(r'[^a-zA-Z\s]', '', abstract)
    
    # Step 4: Convert the text to lowercase
    abstract = abstract.lower()
    
    # Step 5: Tokenize the text into words
    tokens = nltk.word_tokenize(abstract)
    
    # Step 6: Remove common English stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    
    # Step 7: Rejoin the tokens to form a cleaned and normalized abstract
    abstract = ' '.join(tokens)
    
    return abstract



def remove_names_and_organizations(text):
    """
    Remove named entities (PERSON and ORGANIZATION) and verbs from the input text.

    This function takes an input text, processes it using spaCy's natural language processing (NLP) model,
    and then removes tokens that are classified as PERSON or ORGANIZATION named entities or tokens with a
    part-of-speech tag of VERB. The cleaned text is returned as a string with tokens joined by spaces.

    Args:
        text (str): The input text from which named entities and verbs should be removed.

    Returns:
        str: The cleaned text with named entities (PERSON and ORGANIZATION) and verbs removed.

    Example:
    >> input_text = "John works at Apple Inc. He loves programming."
    >> cleaned_text = remove_names_and_organizations(input_text)
    >> print(cleaned_text)
    "He loves."
    """
    # Load the spaCy NLP model
    nlp = spacy.load("en_core_web_sm")

    # Process the input text with spaCy
    doc = nlp(text)

    # Initialize an empty list to store the cleaned tokens
    cleaned_text = []

    # Iterate through the tokens in the processed text
    for token in doc:
        # Check if the token is not a PERSON or ORGANIZATION named entity and not a VERB
        if token.ent_type_ not in ["PERSON", "ORG"] and token.pos_ != "VERB":
            cleaned_text.append(token.text)

    # Join the cleaned tokens with spaces to create the cleaned text
    return ' '.join(cleaned_text)

                    
# cs_data["long_descriptions_pp"] = cs_data["Investee Company Long Business Description\n('|')"].apply(remove_names_and_organizations)             
# cs_data["short_descriptions_pp"] = cs_data["Investee Company Short Business Description\n('|')"].apply(remove_names_and_organizations)
# cs_data["long_descriptions_pp"] = cs_data["long_descriptions_pp"].apply(preprocess_descriptions)
# cs_data["short_descriptions_pp"] = cs_data["short_descriptions_pp"].apply(preprocess_descriptions)