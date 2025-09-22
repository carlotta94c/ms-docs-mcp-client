#!/usr/bin/env python3
"""
Simple MCP Python client for Microsoft Learn MCP server.

This script connects to the Learn MCP server at https://learn.microsoft.com/api/mcp
using the official MCP Python SDK (streamable-http transport), lists available tools,
and invokes the `microsoft_docs_search` tool with the question:

    Does Azure AI Foundry offer a Python SDK?

Requirements:
- Python 3.10+
- Install the MCP Python SDK: pip install "mcp[cli]" (or pip install mcp)

Notes:
- The Learn MCP server expects a streamable-http client. This script uses the
  Python MCP SDK's `streamablehttp_client` helper to handle the transport.
- If the server rejects direct connections (e.g. HTTP 405), use an MCP-capable
  client such as the official SDK or the recommended MCP integrations.

"""

import asyncio
import json

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
import mcp.types as types

# Remote MCP server URL (Microsoft Learn MCP server)
SERVER_URL = "https://learn.microsoft.com/api/mcp"
QUESTION = "Does Azure AI Foundry offer a Python SDK?"


async def main() -> None:
    print("Connecting to Microsoft Learn MCP server:", SERVER_URL)

    try:
        # Create a streamable HTTP client against the remote server
        async with streamablehttp_client(SERVER_URL) as (read_stream, write_stream, _):
            async with ClientSession(read_stream, write_stream) as session:
                print("Initializing session...")
                await session.initialize()
                print("Session initialized.")

                # List tools so we can discover available functionality
                tools_resp = await session.list_tools()
                print("\nAvailable tools:")
                for t in tools_resp.tools:
                    # Some servers provide a title/annotations; fall back to name
                    title = getattr(t, "title", None) or (getattr(t, "annotations", None) and t.annotations.get("title")) or t.name
                    print(f" - {t.name} (title={title})")

                # Use the microsoft_docs_search tool to answer the question
                tool_name = "microsoft_docs_search"
                print(f"\nInvoking tool '{tool_name}' with query: {QUESTION}\n")

                try:
                    result = await session.call_tool(tool_name, arguments={"query": QUESTION})
                except Exception as e:
                    print("Tool invocation failed:", repr(e))
                    return

                # Print textual content blocks returned by the tool
                print("=== Tool call content blocks ===")
                if getattr(result, "isError", False):
                    print("Tool returned an error flag.")

                if hasattr(result, "content") and result.content:
                    for idx, content in enumerate(result.content, start=1):
                        if isinstance(content, types.TextContent):
                            print(f"[Text #{idx}]\n{content.text}\n")
                        else:
                            # Fallback: print a simple representation
                            print(f"[Content #{idx}]: {content}")
                else:
                    print("No content blocks returned by the tool.")

                # If the tool returned structured content, print it as JSON
                if hasattr(result, "structuredContent") and result.structuredContent:
                    print("=== Structured content ===")
                    try:
                        print(json.dumps(result.structuredContent, indent=2, ensure_ascii=False))
                    except Exception:
                        print(result.structuredContent)

    except Exception as e:
        # Streamable HTTP servers may reject non-MCP clients with HTTP 405.
        # The SDK's transport abstracts details, but we still surface failures.
        print("Failed to connect or complete the request:", repr(e))
        print("Note: The Learn MCP server requires a streamable-http client. Ensure the MCP SDK is installed and your environment supports HTTPS streaming.")

    print("Done.")


if __name__ == "__main__":
    asyncio.run(main())
