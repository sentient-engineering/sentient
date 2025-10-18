import os
import sqlite3
import datetime
import numpy as np
from sentence_transformers import SentenceTransformer
from basic_memory.mcp_server import MemoryServer

home = os.path.expanduser("~")
DB_PATH = f"{home}/.sentinel_data/memory/sentinel.sqlite"

class MemoryManager:
    def __init__(self):
        self.embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        self.mcp = MemoryServer(memory_path=f"{home}/.sentinel_data/memory")
        self._init_sql()

    def _init_sql(self):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS episodes (
                time TEXT,
                modality TEXT,
                task TEXT,
                result TEXT
            )
        """)
        conn.commit()
        conn.close()

    def log_event(self, modality, task, result):
        ts = datetime.datetime.now().isoformat()
        conn = sqlite3.connect(DB_PATH)
        conn.execute("INSERT INTO episodes VALUES (?, ?, ?, ?)", (ts, modality, task, result[:500]))
        conn.commit()
        conn.close()
        self.mcp.record(f"Episode@{ts}: [{modality}] {task}")
        return ts

    def recall_associative(self, query: str) -> str:
        """Return closest prior tasks using embedding similarity."""
        conn = sqlite3.connect(DB_PATH)
        rows = conn.execute("SELECT time, task, result FROM episodes").fetchall()
        conn.close()

        if not rows:
            return "No memories found."

        tasks = [row[1] for row in rows]
        task_embeddings = self.embedder.encode(tasks).astype("float32")
        query_embedding = self.embedder.encode([query]).astype("float32")

        scores = np.dot(task_embeddings, query_embedding.T).flatten()

        top_indices = scores.argsort()[-5:][::-1]

        top_associations = [rows[i] for i in top_indices]

        text = "\n".join([f"- {t}: {task}" for t, task, _ in top_associations])
        return f"🧩 Possible associations:\n{text}"

    def sync(self):
        self.mcp.sync_markdown()