"""Unit tests: correlation/request id helpers."""

from __future__ import annotations

from crm_bds_ai.shared_kernel import correlation


class TestCorrelationIds:
    def test_new_id_is_unique_and_hex(self) -> None:
        ids = {correlation.new_id() for _ in range(100)}
        assert len(ids) == 100
        assert all(
            len(value) == 32 and all(c in "0123456789abcdef" for c in value) for value in ids
        )

    def test_set_and_get_roundtrip(self) -> None:
        correlation.set_correlation_ids(request_id="r1", correlation_id="c1")
        assert correlation.get_request_id() == "r1"
        assert correlation.get_correlation_id() == "c1"

    def test_context_isolation_between_async_tasks(self) -> None:
        import asyncio

        async def task(value: str) -> tuple[str, str]:
            correlation.set_correlation_ids(request_id=value, correlation_id=f"c-{value}")
            await asyncio.sleep(0.01)
            return (correlation.get_request_id() or "", correlation.get_correlation_id() or "")

        async def main() -> None:
            a, b = await asyncio.gather(task("a"), task("b"))
            assert a == ("a", "c-a")
            assert b == ("b", "c-b")

        asyncio.run(main())
