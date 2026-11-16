
import os
import sqlite3

DATABASE = "database/lives.db"


def conectar():
    os.makedirs("database", exist_ok=True)
    return sqlite3.connect(DATABASE)


def criar_tabela():
    with conectar() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS lives (
                username TEXT PRIMARY KEY,
                ativo INTEGER DEFAULT 1,
                estava_ao_vivo INTEGER DEFAULT 0
            )
        """)


def listar_perfis():
    with conectar() as conn:
        return conn.execute("""
            SELECT username, estava_ao_vivo
            FROM lives
            WHERE ativo = 1
        """).fetchall()


def adicionar_perfil(username):
    with conectar() as conn:
        conn.execute("""
            INSERT INTO lives (username)
            VALUES (?)
        """, (username,))


def remover_perfil(username):
    with conectar() as conn:
        cursor = conn.execute("""
            DELETE FROM lives
            WHERE username = ?
        """, (username,))

        return cursor.rowcount > 0


def atualizar_status(username, ao_vivo):
    with conectar() as conn:
        conn.execute("""
            UPDATE lives
            SET estava_ao_vivo = ?
            WHERE username = ?
        """, (int(ao_vivo), username))
