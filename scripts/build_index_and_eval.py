"""Build sample corpus index and run evaluation."""

from __future__ import annotations

import logging
import shutil
from pathlib import Path

from docintel.config import ROOT
from docintel.data.store import reset_store_for_tests
from docintel.evaluation.harness import run_evaluation
from docintel.ingestion.pipeline import ingest_file

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def main() -> None:
    samples = ROOT / "data" / "samples"
    index_dir = ROOT / "data" / "processed" / "index"
    if index_dir.exists():
        shutil.rmtree(index_dir)
    reset_store_for_tests(index_dir)

    files = sorted(samples.glob("*.txt")) + sorted(samples.glob("*.pdf"))
    if not files:
        raise SystemExit(f"No samples found in {samples}")
    for path in files:
        doc = ingest_file(path)
        logger.info("Indexed %s → %s (%s chunks)", doc.filename, doc.document_id, doc.chunk_count)

    report = run_evaluation()
    logger.info("Wrote %s", report)


if __name__ == "__main__":
    main()
