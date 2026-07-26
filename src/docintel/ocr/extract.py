"""Text extraction: digital PDF / TXT first."""

from __future__ import annotations

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def extract_text_from_path(path: Path) -> tuple[str, str, int | None]:
    """Return (text, content_type, page_count)."""
    suffix = path.suffix.lower()
    if suffix == ".txt":
        text = path.read_text(encoding="utf-8", errors="replace")
        return normalize_text(text), "text/plain", None
    if suffix == ".pdf":
        return _extract_pdf(path)
    raise ValueError(f"Unsupported file type: {suffix}. Supported: .pdf, .txt")


def extract_text_from_bytes(data: bytes, filename: str) -> tuple[str, str, int | None]:
    suffix = Path(filename).suffix.lower()
    tmp_hint = filename
    if suffix == ".txt":
        text = data.decode("utf-8", errors="replace")
        return normalize_text(text), "text/plain", None
    if suffix == ".pdf":
        return _extract_pdf_bytes(data)
    raise ValueError(f"Unsupported file type for {tmp_hint}. Supported: .pdf, .txt")


def normalize_text(text: str) -> str:
    text = text.replace("\x00", " ")
    lines = [ln.strip() for ln in text.replace("\r\n", "\n").split("\n")]
    cleaned: list[str] = []
    blank = 0
    for ln in lines:
        if not ln:
            blank += 1
            if blank <= 1:
                cleaned.append("")
            continue
        blank = 0
        cleaned.append(ln)
    return "\n".join(cleaned).strip()


def _extract_pdf(path: Path) -> tuple[str, str, int | None]:
    try:
        import pdfplumber

        pages: list[str] = []
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                pages.append(page.extract_text() or "")
            page_count = len(pdf.pages)
        text = normalize_text("\n\n".join(pages))
        if text:
            return text, "application/pdf", page_count
    except Exception as exc:  # noqa: BLE001
        logger.warning("pdfplumber failed (%s); trying pypdf", exc)

    from pypdf import PdfReader

    reader = PdfReader(str(path))
    pages = [(p.extract_text() or "") for p in reader.pages]
    text = normalize_text("\n\n".join(pages))
    if not text:
        raise ValueError(
            "No extractable text layer in PDF. Enable OCR path for scanned documents (v1 digital-first)."
        )
    return text, "application/pdf", len(reader.pages)


def _extract_pdf_bytes(data: bytes) -> tuple[str, str, int | None]:
    import tempfile

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        tmp.write(data)
        tmp_path = Path(tmp.name)
    try:
        return _extract_pdf(tmp_path)
    finally:
        tmp_path.unlink(missing_ok=True)
