import inspect
from ragas.testset import TestsetGenerator

# Get the signature of from_langchain
sig = inspect.signature(TestsetGenerator.from_langchain)
print("TestsetGenerator.from_langchain parameters:")
print(sig)
print("\nParameter details:")
for param_name, param in sig.parameters.items():
    print(f"  - {param_name}: {param.annotation if param.annotation != inspect.Parameter.empty else 'Any'}")
