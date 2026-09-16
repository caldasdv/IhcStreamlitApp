"""Sinalizadores de execução seguros e explícitos."""

from __future__ import annotations

import os


def is_local_mode() -> bool:
    """Ativa o ambiente demo somente quando solicitado explicitamente."""
    return os.getenv("PLANO_LOCAL_MODE", "").strip().lower() in {"1", "true", "yes", "sim"}
