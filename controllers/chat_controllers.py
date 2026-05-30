from models.rag_engine import GobsRagModel


class ChatController:
    def __init__(self):
        """
        Inicializa el controlador y conecta el Modelo RAG de GOBS.
        """
        self.model = GobsRagModel()

    def process_user_message(self, message: str) -> str:
        """
        Recibe la pregunta de la Vista, valida que no esté vacía
        y le pide al Modelo la respuesta ejecutiva.
        """
        message = (message or "").strip()

        if not message:
            return "Por favor, escribe una pregunta válida sobre los estándares GOBS."

        try:
            return self.model.query(message)
        except Exception as e:
            return f"Error al procesar la consulta: {str(e)}"