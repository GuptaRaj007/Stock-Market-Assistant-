from sentence_transformers import SentenceTransformer

class EmbeddingGenerator:
    # Load the model once at the class level
    _model = SentenceTransformer("paraphrase-albert-small-v2")

    @staticmethod
    def generate(query: str):
        """Generate an embedding for the input query using the preloaded model."""
        return EmbeddingGenerator._model.encode(query).tolist()
