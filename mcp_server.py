import sys
import json
from client import VirtualMemoryTLB

vm = VirtualMemoryTLB(tlb_size=4, page_size=4096)
# Map sample default pages
for i in range(16):
    vm.map_page(i, i + 100)

def handle_rpc(line):
    global vm
    try:
        req = json.loads(line)
    except Exception:
        return
    req_id = req.get("id")
    method = req.get("method")
    params = req.get("params", {})

    if method == "initialize":
        res = {
            "protocolVersion": "2024-11-05",
            "serverInfo": {"name": "genpark-virtual-memory-tlb-page-table-skill", "version": "1.0.0"},
            "capabilities": {"tools": {}}
        }
    elif method == "tools/list":
        res = {
            "tools": [
                {
                    "name": "translate_address",
                    "description": "Translate virtual address to physical address with TLB caching",
                    "inputSchema": {
                        "type": "object",
                        "properties": {"virtual_address": {"type": "integer"}},
                        "required": ["virtual_address"]
                    }
                }
            ]
        }
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "translate_address":
            va = args.get("virtual_address", 0)
            data = vm.translate(va)
            res = {"content": [{"type": "text", "text": json.dumps(data)}]}
        else:
            res = {"isError": True, "content": [{"type": "text", "text": f"Unknown tool {tool_name}"}]}
    else:
        res = {"error": {"code": -32601, "message": "Method not found"}}

    resp = {"jsonrpc": "2.0", "id": req_id, "result": res.get("result", res)}
    sys.stdout.write(json.dumps(resp) + "\n")
    sys.stdout.flush()

def main():
    for line in sys.stdin:
        if line.strip():
            handle_rpc(line.strip())

if __name__ == "__main__":
    main()
