# Adding & Securing Custom Tools

## Step-by-Step Tool Definition

1. **Define Input Models:**
   Use Pydantic v2 `BaseModel` with explicit field descriptions:
   ```python
   from pydantic import BaseModel, Field

   class UserLookupParams(BaseModel):
       user_id: str = Field(..., description="Unique user identifier")
       include_audit_trail: bool = Field(default=False, description="Whether to include audit history")
   ```

2. **Implement Business Logic in `src/mcp_server_starter/tools.py`:**
   Keep functions focused and handle exceptions gracefully:
   ```python
   def tool_lookup_user(params: UserLookupParams, context: CallerContext) -> dict:
       # Enforce scope if needed
       if not context.has_scope("users.read"):
           raise ValueError("Caller lacks required scope: users.read")
       
       return {"user_id": params.user_id, "status": "active"}
   ```

3. **Register on Server in `src/mcp_server_starter/server.py`:**
   ```python
   @mcp.tool()
   def lookup_user(user_id: str, include_audit_trail: bool = False) -> dict:
       """Look up user details by user ID."""
       ctx = extract_caller_context({}, transport="stdio")
       return tool_lookup_user(UserLookupParams(user_id=user_id, include_audit_trail=include_audit_trail), ctx)
   ```

FastMCP automatically generates JSON-RPC 2.0 schemas from the type signatures and docstrings.
