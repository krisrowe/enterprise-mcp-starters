"""Sociable Unit Tests for Enterprise MCP Server."""

import pytest
from mcp_server_starter.auth import CallerContext, extract_caller_context
from mcp_server_starter.tools import (
    QueryFilter,
    tool_get_server_time,
    tool_inspect_caller_identity,
    tool_query_sample_records,
)


def test_server_time_returns_utc():
    res = tool_get_server_time()
    assert res["status"] == "ok"
    assert "timestamp_utc" in res
    assert res["service"] == "enterprise-mcp-starter"


def test_caller_context_stdio():
    ctx = extract_caller_context({}, transport="stdio")
    assert ctx.is_authenticated is True
    assert ctx.has_scope("read") is True


def test_caller_context_gateway_headers():
    headers = {
        "x-remote-user": "alice@example.com",
        "x-caller-scopes": "records.read analytics.query",
        "x-consumer-id": "client-app-123"
    }
    ctx = extract_caller_context(headers, transport="http")
    assert ctx.is_authenticated is True
    assert ctx.identity == "alice@example.com"
    assert ctx.client_id == "client-app-123"
    assert ctx.has_scope("records.read") is True
    assert ctx.has_scope("admin") is False


def test_inspect_caller_identity():
    ctx = CallerContext(
        identity="bob@example.com",
        client_id="app-456",
        scopes=["tools.execute"],
        is_authenticated=True
    )
    res = tool_inspect_caller_identity(ctx)
    assert res["identity"] == "bob@example.com"
    assert res["client_id"] == "app-456"
    assert res["mode"] == "authorized"


def test_query_sample_records_all():
    params = QueryFilter(limit=10)
    res = tool_query_sample_records(params)
    assert res["count"] > 0
    assert len(res["records"]) <= 10


def test_query_sample_records_filter():
    params = QueryFilter(category="finance", limit=5)
    res = tool_query_sample_records(params)
    assert res["count"] >= 1
    for rec in res["records"]:
        assert rec["category"] == "finance"
