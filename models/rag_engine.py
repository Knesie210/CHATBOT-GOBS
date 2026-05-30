import os
from pathlib import Path

from dotenv import load_dotenv

from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings,
)

from langchain_community.document_loaders import (
    DirectoryLoader,
    TextLoader,
)

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.vectorstores import FAISS

from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser


PROJECT_ROOT = Path(__file__).resolve().parents[1]

# Cargar .env para desarrollo local
load_dotenv(PROJECT_ROOT / ".env")


class GobsRagModel:
    def __init__(
        self,
        data_dir=None,
        model_name="gemini-2.5-flash",
        embedding_model="models/gemini-embedding-001",
    ):
        """
        Inicializa el motor RAG de GOBS.
        Compatible con Streamlit Cloud y ejecución local.
        """

        api_key = os.getenv("GOOGLE_API_KEY")

        if not api_key:
            raise ValueError(
                "GOOGLE_API_KEY no encontrada. "
                "Configúrala en .env o en Streamlit Secrets."
            )

        self.data_dir = Path(data_dir) if data_dir else PROJECT_ROOT / "data"

        self.model_name = model_name
        self.embedding_model = embedding_model

        self.llm = None
        self.embeddings = None
        self.vector_store = None
        self.retriever = None
        self.rag_chain = None

        self._initialize_llm()
        self._build_vector_store()
        self._create_rag_chain()

    def _initialize_llm(self):
        """
        Inicializa Gemini y el modelo de embeddings.
        """

        self.llm = ChatGoogleGenerativeAI(
            model=self.model_name,
            temperature=0.2,
        )

        self.embeddings = GoogleGenerativeAIEmbeddings(
            model=self.embedding_model
        )

    def _load_documents(self):
        """
        Carga todos los TXT de la carpeta data.
        """

        self.data_dir.mkdir(parents=True, exist_ok=True)

        loader = DirectoryLoader(
            str(self.data_dir),
            glob="*.txt",
            loader_cls=TextLoader,
            loader_kwargs={"encoding": "utf-8"},
        )

        docs = loader.load()

        if not docs:
            docs = [
                Document(
                    page_content=(
                        "Manual Global de GOBS: "
                        "Sistema de operaciones iniciado."
                    )
                )
            ]

        return docs

    def _build_vector_store(self):
        """
        Construye el índice vectorial FAISS.
        Mucho más estable que Chroma en Streamlit Cloud.
        """

        docs = self._load_documents()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=700,
            chunk_overlap=100,
        )

        chunks = splitter.split_documents(docs)

        self.vector_store = FAISS.from_documents(
            documents=chunks,
            embedding=self.embeddings,
        )

        self.retriever = self.vector_store.as_retriever(
            search_kwargs={"k": 3}
        )

    def _format_docs(self, docs):
        """
        Convierte documentos recuperados en texto.
        """

        return "\n\n".join(
            doc.page_content
            for doc in docs
        )

    def _create_rag_chain(self):
        """
        Construye la cadena RAG utilizando LCEL.
        """

        system_prompt = """
Eres GOBS-Bot, un asistente ejecutivo experto en:

- Global Operation Business System (GOBS)
- Manufactura
- Operational Excellence
- Six Sigma
- DMAIC
- ALCOA+
- KPIs operativos

Reglas obligatorias:

1. Responde de forma profesional, clara y estructurada.
2. Utiliza únicamente el contexto proporcionado.
3. No inventes procedimientos.
4. Si la respuesta no existe en el contexto responde exactamente:

Lo siento, esa información no forma parte del manual operativo actual de GOBS.

Contexto:
{context}
"""

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", "{input}"),
            ]
        )

        self.rag_chain = (
            {
                "context": (
                    self.retriever
                    | RunnableLambda(self._format_docs)
                ),
                "input": RunnablePassthrough(),
            }
            | prompt
            | self.llm
            | StrOutputParser()
        )

    def query(self, user_input: str) -> str:
        """
        Método público utilizado por el controlador.
        """

        if not self.rag_chain:
            return "Error: El motor RAG no fue inicializado."

        try:
            response = self.rag_chain.invoke(user_input)

            if not response:
                return (
                    "Lo siento, esa información no forma parte "
                    "del manual operativo actual de GOBS."
                )

            return response

        except Exception as e:
            return f"Error al procesar la consulta: {str(e)}"