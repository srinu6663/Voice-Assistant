import chromadb
import logging

chroma_logger = logging.getLogger("chromadb")
chroma_logger.setLevel(logging.ERROR)
chroma_logger.propagate = False

chroma_client = chromadb.PersistentClient(path="chroma_data")

collection_name = "chat_memory"

existing_collections = chroma_client.list_collections()

if collection_name not in existing_collections:
    print(f"🛠️ Creating collection: {collection_name}")
    chroma_client.create_collection(name=collection_name)

collection = chroma_client.get_collection(name=collection_name)

def store_chat(query, response):
    """Store a chat interaction in ChromaDB."""
    try:
        collection.add(
            documents=[f"User: {query}\nAssistant: {response}"],
            ids=[str(hash(query + response))]
        )
        print("✅ Chat stored successfully.")
    except Exception as e:
        print(f"❌ Error storing chat: {e}")




# def get_all_chats():
#     """Retrieve and display all stored chat interactions."""
#     try:
#         data = collection.get()
#         for doc in data["documents"]:
#             print(doc)
#     except Exception as e:
#         print(f"Error retrieving chats: {e}")

# get_all_chats()


# chroma_client.delete_collection(name=collection_name)
# print("Collection deleted successfully.")
