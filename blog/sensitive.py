"""Detecta y censura información sensible antes de publicar un post.

Regla de Pablo (2026-10-01): en el blog nunca puede salir una API key, una variable de entorno
con credenciales ni ningún otro dato sensible. Esto se aplica a todo post antes de publicarlo
(ver el comando audit_posts) y lo que encuentra se sustituye por un marcador visible.
"""

from __future__ import annotations

import re

REDACTED = "[censurado]"

# (nombre, patrón). El orden importa: lo más específico primero.
PATTERNS: list[tuple[str, re.Pattern]] = [
    ("clave privada", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----", re.S)),
    ("api key", re.compile(r"\b(?:sk-ant-[\w-]{10,}|sk-[\w-]{16,}|nvapi-[\w-]{16,}|gh[pousr]_\w{20,}|github_pat_\w{20,}|xox[abpr]-[\w-]{10,}|AKIA[0-9A-Z]{16}|AIza[\w-]{30,})")),
    ("jwt", re.compile(r"\beyJ[\w-]{10,}\.[\w-]{10,}\.[\w-]{10,}")),
    ("asignación de secreto", re.compile(r"\b([A-Z][A-Z0-9_]*(?:KEY|TOKEN|SECRET|PASSWORD|PASS|CREDENTIAL)[A-Z0-9_]*)\s*[=:]\s*['\"]?[^\s'\"]{6,}")),
    ("variable de entorno de credencial", re.compile(r"\b[A-Z][A-Z0-9_]*_(?:API_KEY|KEY|TOKEN|SECRET|PASSWORD|CREDENTIALS?|VOICE_ID|CHAT_ID)\b")),
    ("token largo", re.compile(r"\b(?=[A-Za-z0-9_-]*\d)(?=[A-Za-z0-9_-]*[A-Za-z])[A-Za-z0-9_-]{32,}\b")),
    ("email", re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b")),
    ("ip", re.compile(r"\b(?!127\.0\.0\.1\b)(?!0\.0\.0\.0\b)(?:\d{1,3}\.){3}\d{1,3}\b")),
    ("url de túnel", re.compile(r"https?://[\w-]+\.trycloudflare\.com\S*")),
    ("ruta de usuario", re.compile(r"/home/[\w.-]+(?:/[\w./-]*)?|/root/\.[\w./-]+")),
    ("usuario o host", re.compile(r"\b(?:ocultwolf|cl3v3rt04st3r)\b", re.I)),
]


def find_sensitive(text: str) -> list[tuple[str, str]]:
    """Devuelve [(tipo, fragmento)] de todo lo sensible encontrado en `text`."""
    hits = []
    for name, pattern in PATTERNS:
        for m in pattern.finditer(text or ""):
            hits.append((name, m.group(0)))
    return hits


def redact(text: str) -> str:
    """Sustituye todo lo sensible por un marcador visible."""
    for _, pattern in PATTERNS:
        text = pattern.sub(REDACTED, text or "")
    return text
