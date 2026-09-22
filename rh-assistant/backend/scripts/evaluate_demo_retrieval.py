"""Evaluate semantic retrieval against the synthetic EUBIA questions."""

import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_DIR))

from app.data.eubia_demo_documents import DEMO_EVALUATION_QUERIES
from app.services.document_index import search_documents


def main() -> int:
    passed = 0
    for item in DEMO_EVALUATION_QUERIES:
        result = search_documents(item["question"], n_results=3)
        filenames = [
            metadata.get("filename", "")
            for metadata in result.get("metadatas", [[]])[0]
        ]
        is_match = item["expected_source"] in filenames
        passed += int(is_match)
        marker = "PASS" if is_match else "FAIL"
        print(f"[{marker}] {item['question']} -> {filenames}")

    print(f"{passed}/{len(DEMO_EVALUATION_QUERIES)} retrieval checks passed.")
    return 0 if passed == len(DEMO_EVALUATION_QUERIES) else 1


if __name__ == "__main__":
    raise SystemExit(main())
