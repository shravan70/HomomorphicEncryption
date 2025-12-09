from fastapi import FastAPI
from pydantic import BaseModel
from concrete import fhe

app = FastAPI(title="FHE API Example")

class InputData(BaseModel):
    x: int

# FHE function
@fhe.compiler({"x": "encrypted"})
def homomorphic_compute(x):
    return (x * 3) + x + 3

# Compile circuit once at startup
inputset = [1, 2, 3, 4, 5, 9]
circuit = homomorphic_compute.compile(inputset)
circuit.keygen()


@app.post("/compute")
def compute(data: InputData):
    # Encrypt input
    encrypted_input = circuit.encrypt(data.x)
    
    # Run FHE computation
    encrypted_result = circuit.run(encrypted_input)
    
    # Decrypt result
    result = circuit.decrypt(encrypted_result)
    
    return {"input": data.x, "result": result, "encrypted_input": str(encrypted_input), "encrypted_result": str(encrypted_result)}
