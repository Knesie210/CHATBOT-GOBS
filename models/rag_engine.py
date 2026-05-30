import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
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
        Inicializa los componentes de datos y configuraciones de LangChain + Gemini.
        """
        if not os.getenv("GOOGLE_API_KEY"):
            raise ValueError("GOOGLE_API_KEY no encontrada en el archivo .env")

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
        Configura los motores de lenguaje y embeddings de Google Gemini.
        """
        self.llm = ChatGoogleGenerativeAI(model=self.model_name, temperature=0.2)
        self.embeddings = GoogleGenerativeAIEmbeddings(model=self.embedding_model)

    def _build_vector_store(self):
        """
        Carga los documentos operativos de GOBS y los indexa en Chroma.
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
                    page_content="Manual Global de GOBS: Sistema de operaciones iniciado."
                )
            ]

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
        )
        chunks = text_splitter.split_documents(docs)

        self.vector_store = Chroma.from_documents(chunks, self.embeddings)
        self.retriever = self.vector_store.as_retriever(search_kwargs={"k": 3})

    def _format_docs(self, docs):
        """
        Une los fragmentos de texto recuperados para pasárselos al prompt.
        """
        return "\n\n".join(doc.page_content for doc in docs)

    def _create_rag_chain(self):
        """
        Define el Prompt y ensambla la cadena usando LCEL moderno.
        """
        system_prompt = (
            "Eres GOBS-Bot, un asistente ejecutivo de alto nivel experto en el Global Operation Business System (GOBS), "
            "Manufactura, Six Sigma e Integridad de Datos (ALCOA+).\n"
            "Tu único propósito es responder consultas basadas estrictamente en la documentación técnica provista.\n\n"
            "Reglas corporativas inquebrantables:\n"
            "1. Responde de forma profesional, directa y organizada.\n"
            "2. Si la información solicitada no se encuentra explícitamente dentro del contexto provisto, responde exactamente: "
            "'Lo siento, esa información no forma parte del manual operativo actual de GOBS.'\n"
            "3. Apóyate únicamente en los datos operativos vigentes.\n\n"
            "Contexto del Manual GOBS:\n{context}"
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", "{input}"),
            ]
        )

        self.rag_chain = (
            {
                "context": self.retriever | RunnableLambda(self._format_docs),
                "input": RunnablePassthrough(),
            }
            | prompt
            | self.llm
            | StrOutputParser()
        )

    def query(self, user_input: str) -> str:
        """
        Método público que será llamado por el controlador para obtener respuestas.
        """
        if not self.rag_chain:
            return "Error: El motor RAG no se encuentra inicializado."

        try:
            return self.rag_chain.invoke(user_input)
        except Exception as e:
            return f"Error al procesar la consulta: {str(e)}"