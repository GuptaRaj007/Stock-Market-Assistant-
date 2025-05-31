from sentence_transformers import SentenceTransformer

class EmbeddingGenerator:
    # Load the model once at the class level
    _model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    @staticmethod
    def generate(query: str):
        """Generate an embedding for the input query using the preloaded model."""
        return EmbeddingGenerator._model.encode(query).tolist()
