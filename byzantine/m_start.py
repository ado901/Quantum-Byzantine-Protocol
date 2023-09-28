import importlib
import start # first execution

for _ in range(29): # other 49 executions
    importlib.reload(start)