from functools import lru_cache # for adding cache functionality for quicker response
from fastapi import FastAPI
import uvicorn
import time

app = FastAPI()

async def fibonacci(n: int):  
    start_time = time.monotonic_ns()
   
    if n < 0:
        raise ValueError("Negative arguments not implemented")	
    result = _fib(n)[0]
 
    end_time = time.monotonic_ns()
    execution_time_in_ms = round((end_time - start_time)/1000000,4) # converting nano seconds into milli seconds
    return [result,execution_time_in_ms]
    

# (Private) Returns the tuple (F(n), F(n+1)).
@lru_cache(maxsize=1000,typed=True)
def _fib(n: int):
    if n == 0:
        return (0, 1)
    else:		
        a, b = _fib(n// 2)

        c = a * (b * 2 - a)

        d = a * a + b * b
        
        if n % 2 == 0:
            return (c, d)
        else:
            return (d, c + d)

@app.get("/")
def read_root():
    return {"routes": ["/fibonacci/{input:int}"]}


@app.get("/fibonacci/{input}")
async def read_item(input: int):
    output = await fibonacci(input)
    return {"nth_fibonacci": output[0],"execution_time_in_ms":output[1]}

if __name__ == '__main__':
    uvicorn.run(app, port=8000,host="0.0.0.0")    
