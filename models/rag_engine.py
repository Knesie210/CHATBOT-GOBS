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
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import (
    RunnablePassthrough,
    RunnableLambda,
)
from langchain_core.output_parsers import StrOutputParser


PROJECT_ROOT = Path(__file__).resolve().parents[1]

load_dotenv(PROJECT_ROOT / ".env")


class GobsRagModel:
    def __init__(
        self,
        data_dir=None,
        model_name="gemini-2.5-flash",
        embedding_model="models/gemini-embedding-001",
    ):
        """
        Inicializa el motor RAG basado en Gemini + Chroma.
        Compatible con entorno local y Streamlit Cloud.
        """

        self.api_key = self._load_api_key()

        self.data_dir = Path(data_dir) if data_dir else PROJECT_ROOT / "data"

        self.chroma_dir = PROJECT_ROOT / "chroma_db"

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

    def _load_api_key(self):
        """
        Obtiene la API KEY desde:
        1. Variable de entorno local
        2. Streamlit Secrets
        """

        api_key = os.getenv("GOOGLE_API_KEY")

        if api_key:
            return api_key

        try:
            import streamlit as st

            api_key = st.secrets.get("GOOGLE_API_KEY")

            if api_key:
                os.environ["GOOGLE_API_KEY"] = api_key
                return api_key

        except Exception:
            pass

        raise ValueError(
            "No se encontró GOOGLE_API_KEY. "
            "Configúrala en .env o en Streamlit Secrets."
        )

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

    def _build_vector_store(self):
        """
        Carga documentos TXT y genera el índice vectorial.
        """

        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.chroma_dir.mkdir(parents=True, exist_ok=True)

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

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
        )

        chunks = splitter.split_documents(docs)

        self.vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=str(self.chroma_dir),
        )

        self.retriever = self.vector_store.as_retriever(
            search_kwargs={"k": 3}
        )

    @staticmethod
    def _format_docs(docs):
        """
        Convierte los documentos recuperados en texto.
        """

        return "\n\n".join(
            doc.page_content
            for doc in docs
        )

    def _create_rag_chain(self):
        """
        Construye la cadena RAG usando LCEL moderno.
        """

        system_prompt = """
Eres GOBS-Bot, un asistente ejecutivo especializado en:

- Global Operation Business System (GOBS)
- Manufactura
- Six Sigma
- Lean Manufacturing
- ALCOA+
- Excelencia Operacional

Reglas obligatorias:

1. Responde únicamente utilizando la información del contexto.
2. Sé profesional, preciso y organizado.
3. No inventes información.
4. Si la respuesta no está en el contexto responde exactamente:

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
                "context": self.retriever
                | RunnableLambda(self._format_docs),
                "input": RunnablePassthrough(),
            }
            | prompt
            | self.llm
            | StrOutputParser()
        )

    def query(self, user_input: str) -> str:
        """
        Ejecuta una consulta contra el motor RAG.
        """

        if not self.rag_chain:
            return "Error: El motor RAG no se encuentra inicializado."

        try:
            return self.rag_chain.invoke(user_input)

        except Exception as e:
            return f"Error al procesar la consulta: {str(e)}"