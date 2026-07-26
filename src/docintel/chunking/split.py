"""Chunking strategies for document intelligence."""

from __future__ import annotations


def chunk_text(
    text: str,
    strategy: str = "recursive",
    chunk_size: int = 512,
    overlap: int = 64,
) -> list[str]:
    text = text.strip()
    if not text:
        return []
    if strategy == "fixed_tokens":
        return _fixed_window(text, chunk_size, overlap)
    if strategy == "page":
        # Caller may pass page-joined text with form feeds; treat double newlines as pages
        pages = [p.strip() for p in text.split("\f") if p.strip()]
        if len(pages) <= 1:
            pages = [p.strip() for p in text.split("\n\n") if p.strip()]
        return pages or [text]
    # default recursive / paragraph-aware
    return _recursive_split(text, chunk_size, overlap)


def _fixed_window(text: str, size: int, overlap: int) -> list[str]:
    words = text.split()
    if not words:
        return []
    step = max(1, size - overlap)
    chunks: list[str] = []
    for i in range(0, len(words), step):
        window = words[i : i + size]
        if not window:
            break
        chunks.append(" ".join(window))
        if i + size >= len(words):
            break
    return chunks


def _recursive_split(text: str, size: int, overlap: int) -> list[str]:
    """Approximate token windows using whitespace word counts."""
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    if not paragraphs:
        return _fixed_window(text, size, overlap)

    chunks: list[str] = []
    buf: list[str] = []
    buf_words = 0
    for para in paragraphs:
        n = len(para.split())
        if buf and buf_words + n > size:
            chunks.append("\n\n".join(buf))
            # overlap: keep tail words from previous buffer
            if overlap > 0:
                prev_words = " ".join(buf).split()
                tail = prev_words[-overlap:] if len(prev_words) > overlap else prev_words
                buf = [" ".join(tail), para] if tail else [para]
                buf_words = len(" ".join(buf).split())
            else:
                buf = [para]
                buf_words = n
        else:
            buf.append(para)
            buf_words += n
    if buf:
        chunks.append("\n\n".join(buf))
    # Split any oversized chunk further
    final: list[str] = []
    for c in chunks:
        if len(c.split()) <= size * 1.5:
            final.append(c)
        else:
            final.extend(_fixed_window(c, size, overlap))
    return final
