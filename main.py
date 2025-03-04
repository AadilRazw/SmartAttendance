# main.py
from deepface import DeepFace
import numpy as np
import os
from sklearn.metrics.pairwise import cosine_similarity



# Function to extract embeddings for a set of images
def extract_embeddings(image_paths):
    embeddings = []
    for image_path in image_paths:
        embedding = DeepFace.represent(image_path, model_name="VGG-Face")[0]["embedding"]
        embeddings.append(embedding)
    return np.array(embeddings)


# Function to compare embeddings using cosine similarity
def compare_embeddings(query_embedding, dataset_embeddings):
    similarities = cosine_similarity([query_embedding], dataset_embeddings)
    return similarities


def get_image_paths(folder_path):
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']
    image_paths = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if any(file.lower().endswith(ext) for ext in image_extensions):
                image_paths.append(os.path.join(root, file))

    return image_paths


def find_most_similar_image(image_folder, test_image):


    # Example image dataset (list of image paths)
    image_paths = get_image_paths(image_folder)  # Add your image paths

    # Extract embeddings for all dataset images (only do this once and store them)
    dataset_embeddings = extract_embeddings(image_paths)

    # Query image to match
    query_image = test_image # Provide the path to your query image

    # Extract the embedding for the query image
    query_embedding = DeepFace.represent(query_image, model_name="VGG-Face")[0]["embedding"]

    # Compare the query image embedding to the dataset embeddings
    similarities = compare_embeddings(query_embedding, dataset_embeddings)

    # Find the most similar image(s) by getting the highest cosine similarity
    most_similar_idx = np.argmax(similarities)
    most_similar_image = image_paths[most_similar_idx]
    similarity_score = similarities[0][most_similar_idx]

    return (most_similar_image,similarity_score)




def main(query_image):

    # Query image to match
      # Provide the path to your query image

    # Call the function to find the most similar image

    return find_most_similar_image("images",query_image)

   

if __name__ == "__main__":
    main()
