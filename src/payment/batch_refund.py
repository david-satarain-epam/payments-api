"""
Payment API — Batch refund processing.

NEW ENDPOINT: POST /refund/batch
Status: In development. ZERO test coverage.

Accepts an array of refund requests and processes them
sequentially or in parallel.
"""

from datetime import datetime, timezone
from .schema import BatchRefundRequest, BatchRefundResponse, RefundResponse
from .api import process_refund


def process_batch_refund(request: BatchRefundRequest) -> BatchRefundResponse:
    """
    Process multiple refunds in batch mode.

    ⚠️ WARNING: New endpoint. No tests exist yet.
    ⚠️ Risk: HIGH — affects core payment flow.
    """
    batch_id = f"batch-{int(datetime.now().timestamp())}"
    results: list[RefundResponse] = []
    processed = 0
    failed = 0
    mode = request.mode or "SEQUENTIAL"

    if mode == "PARALLEL":
        import concurrent.futures

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = {
                executor.submit(_safe_process, refund): refund
                for refund in request.refunds
            }
            for future in concurrent.futures.as_completed(futures):
                try:
                    result = future.result()
                    if result:
                        results.append(result)
                        processed += 1
                    else:
                        failed += 1
                except Exception:
                    failed += 1
    else:
        for refund in request.refunds:
            result = _safe_process(refund)
            if result:
                results.append(result)
                processed += 1
            else:
                failed += 1

    return BatchRefundResponse(
        batch_id=batch_id,
        total_refunds=len(request.refunds),
        processed=processed,
        failed=failed,
        results=results,
    )


def _safe_process(refund) -> RefundResponse | None:
    """Safely process a single refund, returning None on failure."""
    try:
        return process_refund(refund)
    except Exception:
        return None