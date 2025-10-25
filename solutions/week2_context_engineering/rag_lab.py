import requests
import json
import chromadb
import argparse

# --- 1. Configuration ---
OLLAMA_ENDPOINT = "http://localhost:11434/api"
OLLAMA_CONFIG = {
    "model": "llama3",
    "stream": False,
}
CHROMA_DB_PATH = "./chroma_db"
COLLECTION_NAME = "faq_collection"

# --- 2. Knowledge Base ---
# In a real-world scenario, this would come from a file, database, or API.
FAQ_DATA = [
    {"id": "faq1", "question": "What is the return policy?", "answer": "You can return any item within 30 days of purchase for a full refund."},
    {"id": "faq2", "question": "How do I track my order?", "answer": "Once your order has shipped, you will receive an email with a tracking number."},
    {"id": "faq3", "question": "Do you ship internationally?", "answer": "Yes, we ship to most countries worldwide. Shipping costs may vary."},
    {"id": "faq4", "question": "How can I contact customer support?", "answer": "You can reach our customer support team via email at support@example.com or by calling our toll-free number."},
    {"id": "faq5", "question": "What payment methods do you accept?", "answer": "We accept all major credit cards, PayPal, and Apple Pay."},
    {"id": "faq6", "question": "Can I change my shipping address?", "answer": "If your order has not yet shipped, you can contact customer support to update your shipping address."},
    {"id": "faq7", "question": "What are your business hours?", "answer": "Our customer support is available Monday to Friday, from 9 AM to 5 PM EST."},
    {"id": "faq8", "question": "Do you offer gift wrapping?", "answer": "Yes, we offer gift wrapping for an additional fee. You can select this option at checkout."},
    {"id": "faq9", "question": "How do I use a discount code?", "answer": "You can apply your discount code in the 'Promo Code' box at checkout."},
    {"id": "faq10", "question": "What if my item is damaged?", "answer": "If your item arrives damaged, please contact customer support immediately for a replacement or refund."}
]

# --- 3. ChromaDB Setup ---
client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
collection = client.get_or_create_collection(name=COLLECTION_NAME)

# --- 4. Helper Functions ---

def get_embedding(text):
    """
    Generates an embedding for the given text using the Ollama API.
    """
    try:
        response = requests.post(
            f"{OLLAMA_ENDPOINT}/embeddings",
            json={"model": OLLAMA_CONFIG["model"], "prompt": text}
        )
        response.raise_for_status()
        return response.json()["embedding"]
    except requests.exceptions.RequestException as e:
        print(f"Error getting embedding: {e}")
        return None

def index_knowledge_base():
    """
    Indexes the knowledge base into ChromaDB.
    """
    print("Indexing knowledge base...")
    documents = []
    metadatas = []
    ids = []
    embeddings = []

    for item in FAQ_DATA:
        # We are embedding the questions to find similar user queries.
        embedding = get_embedding(item["question"])
        if embedding:
            ids.append(item["id"])
            embeddings.append(embedding)
            documents.append(item["answer"]) 
            metadatas.append({"original_question": item["question"], "original_answer": item["answer"]})
    
    if ids:
        collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents, 
            metadatas=metadatas
        )
    print("Indexing complete.")

def query_rag_agent(user_query, k=2, use_context=True):
    """
    Queries the RAG agent with a user's question, with adjustable k and context use.
    """
    print(f"\n--- Querying for: '{user_query}' (k={k}, context={'ON' if use_context else 'OFF'}) ---")
    
    # 1. Get embedding for the user query
    query_embedding = get_embedding(user_query)
    if not query_embedding:
        return "Sorry, I couldn't process your query due to an embedding error."

    # 2. Query ChromaDB for relevant context
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=k
    )

    retrieved_documents = results.get('documents', [[]])[0]
    retrieved_metadatas = results.get('metadatas', [[]])[0]

    if not use_context or not retrieved_documents:
        retrieved_context = "No context was used."
    else:
        context_blocks = []
        citation_sources = []
        citation_list = ""

        for i, (doc, meta) in enumerate(zip(retrieved_documents, retrieved_metadatas)):
            citation_sources.append(f"Source faq{i+1}: Q: '{meta['original_question']}'")
            context_blocks.append(f"---CONTEXT BLOCK {i+1}---\n{doc}")
                
        retrieved_context = "\n\n".join(context_blocks)
            
        # Add citation list at end of answer (will be appended later)
        citation_list = "\n\n**Sources Used:**\n" + "\n".join(citation_sources)
    
    print(f"Retrieved context: {retrieved_context}")

    # 3. Construct the prompt for the LLM
    if use_context:
        prompt = f"""
        You are a helpful FAQ assistant. A user has asked the following question:
        '{user_query}'

        Here is some context that might be relevant to the question. Each source is in a delimited block:
        '{retrieved_context}'

        Based on this context, please provide a clear and concise answer. If the context is not relevant, say so.
        """
    else:
        prompt = f"""
        You are a helpful FAQ assistant. A user has asked the following question:
        '{user_query}'

        print("no context")

        """

    # 4. Send the prompt to the LLM
    try:
        response = requests.post(
            f"{OLLAMA_ENDPOINT}/generate",
            json={"prompt": prompt, **OLLAMA_CONFIG}
        )
        response.raise_for_status()
        llm_response = json.loads(response.text)["response"].strip()
        
        final_answer = llm_response

        if use_context and citation_list:
            final_answer += citation_list
             
        return final_answer
    except requests.exceptions.RequestException as e:
        return f"Error communicating with the model: {e}"

# --- 5. Main Execution ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Week 2 Prompt RAG Agent")
    parser.add_argument('--k', type=int, default=2, help="The number of documents to retrieve from ChromaDB (n_results). Default is 2.")
    parser.add_argument('--no-context', action='store_true', help="If set, the retrieved context will NOT be passed to the LLM.")
    parser.add_argument('--query', type=str, required=False, help="The user question to query the RAG agent.")
    args = parser.parse_args()

    # Check if the collection is empty before indexing
    if collection.count() == 0:
        index_knowledge_base()
    else:
        print("Knowledge base is already indexed.")

    if args.query:
        answer = query_rag_agent(args.query, args.k, not args.no_context)
        print(answer)
    elif args.test_mode:
    # --- Test Queries ---
        test_queries = [
            "How can I return a product?",
            "What's the process for tracking my package?",
            "Do you ship to Canada?",
            "What are the support hours?",
            "Can I pay with Bitcoin?"
        ]

        for query in test_queries:
            answer = query_rag_agent(query, args.k, not args.no_context)
            print(f"Answer: {answer}")
    else:
        print("\nNo query provided. Please run with --query \"...\" or --test-mode.")
        parser.print_help()