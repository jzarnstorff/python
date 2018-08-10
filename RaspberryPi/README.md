Example output using Python3

'>>> import mcp9808'
'>>> mcp = mcp9808.MCP9808(0x18)'
'>>> temp = mcp.get_temperature()'
'>>> print("{} C".format(temp))'
'22.5 C'
'>>> print("{} F".format((temp * 1.8) + 32))'
'72.5 F'
'>>> '
