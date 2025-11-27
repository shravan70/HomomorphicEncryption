# app.py
from fastapi import FastAPI
from pydantic import BaseModel
from concrete import fhe

# FastAPI app
app = FastAPI(title="FHE API Example")

# Input model
class InputData(BaseModel):
    x: int

# 1) Define the FHE function
@fhe.compiler({"x": "encrypted"})
def homomorphic_compute(x):
    return (x * 3) + x + 3

# Compile circuit once at startup
inputset = [1, 2, 3, 4, 5, 9]
circuit = homomorphic_compute.compile(inputset)
circuit.keygen()


@app.post("/compute")
def compute(data: InputData):
    # 2) Encrypt input
    encrypted_input = circuit.encrypt(data.x)
    
    # 3) Run FHE computation
    encrypted_result = circuit.run(encrypted_input)
    
    # 4) Decrypt result
    result = circuit.decrypt(encrypted_result)
    
    return {"input": data.x, "result": result, "encrypted_input": str(encrypted_input), "encrypted_result": str(encrypted_result)}
