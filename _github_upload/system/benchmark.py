import time
import sys
import os
import importlib.util

# Load substrate.pvm as a module
module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "substrate.pvm"))
from importlib.machinery import SourceFileLoader
substrate = SourceFileLoader("substrate", module_path).load_module()

tokenize = substrate.tokenize
parse_from_tokens = substrate.parse_from_tokens
create_global_env = substrate.create_global_env
compile_to_vm = substrate.compile_to_vm

def benchmark_loop(n=100000):
    code = f"""
    (let ((i 0) (sum 0))
      (while (< i {n})
        (set! sum (+ sum i))
        (set! i (+ i 1)))
      sum)
    """
    env = create_global_env()
    tokens = tokenize(code)
    ast = parse_from_tokens(tokens)
    vm = compile_to_vm(ast, env)
    
    start = time.time()
    result = vm.run()
    end = time.time()
    
    print(f"Benchmark results for {n} iterations:")
    print(f"Result: {result}")
    print(f"Time taken: {end - start:.4f} seconds")
    return end - start

if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 100000
    benchmark_loop(n)
