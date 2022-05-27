from functools import lru_cache # for adding cache functionality for quicker response
from fastapi import FastAPI # for deploying the solution as an API
import uvicorn #ASGI web server implementation for python
import time # for calculating execution time in the output

app = FastAPI() #creating the app object
    
def fibonacci(n: int):                  
    """ 
    async is not very helpful in this case as this is a mathematical operation and we need the output
    from the previous call to continue with the current calculations.
    """
    if n <= 0:
        # raise ValueError("Negative arguments not implemented")
        result = {"fibonacci_result":None,"msg":"Non-Negative arguments not implemented"}
        return result
    """
    we can pass a msg explaining what is wrong with the input, or raise ValueError. If we return a msg then
    this will be of status code 200 and wont be logged as an error. If we want to log all error then raise error is
    a better approach. Haven't raised error for this exercise.
    
    """ 
        	
    result = {"fibonacci_result":__fibo(n)[0],"msg":"Success"}

    """ 
    __fibo(n) is the private function that calculates the fibonacci number.
    Made it private so that its not accessible thru api calls. Separating the business logic
    to a private method is a good practice in production.
    """
    return result
    
@lru_cache(maxsize=1000,typed=True)  
def __fibo(n: int):
    """  
    lru_cache discards the least recently used items first from the cache. max of 1000 items before
    cache starts evicting older items, typed = True, so that function arguments of different types will 
    be cached separately.
    Caching the results has increased requests/sec greatly when the same value is
    called multiple times.
    Specifically chose maxsize of 1000 to ensure cache doesnt grow beyond bounds.
    typed is set to True to cache results based on input type
    """
    """
    Private funtion returns the tuple (F(n), F(n+1)).
    Fast doubling is based on a 2 formula approach
    F(2n) = F(n)[2*F(n+1) - F(n)]
    F(2n + 1) = F(n)^2 + F(n+1)^2

    In the below code a = F(n),b = F(n+1),c = F(2n),d = F(2n+1)
    base case F(n)=0 and F(n+1)=1

    """
    if n == 0:
        return (0, 1) # base case
    else:		
        a, b = __fibo(n// 2)    #   implementing fast doubling algorithm,one of the fastest algorithm to calculate fibonacci number with time complexity of O(log n).
                                #   The fast doubling algorithm avoids redundantly calculating twice and improves performance comapred to previous recursive calls alogorith where complexity is O(n^2).
        c = a * (b * 2 - a)     

        d = a * a + b * b
        
        if n % 2 == 0:
            return (c, d)
        else:
            return (d, c + d)

@app.get("/")
def read_root():    #   root path
    return {"routes": ["/fibonacci/{input:int}"]}   #   example: http://0.0.0.0:8000/fibonacci/4096


@app.get("/fibonacci/{input}")
def read_item(input: int):
    """
    If the input is bigger than 1 million, the function takes longer to compute the result, which blocks the python thread.
    In order to facilitate computing larger fibonacci series, we would have to use task scheduler similar to celery
    to compute the fibonacci series based on the user input and send the result to the user after its computed in 
    asynchronous manner (using async and await) and let the API serve other requests in the mean time.

    """
    start_time = time.monotonic_ns()
    output = fibonacci(input)
    end_time = time.monotonic_ns()
    execution_time_in_ms = round((end_time - start_time)/1000000.0,4)   #   converting nano seconds into milli seconds by dividing by 1000000.
    return {"msg": output["msg"],"nth_fibonacci": output["fibonacci_result"],"execution_time_in_ms":execution_time_in_ms}    #   calculating the fibonaci number for a million should take approx 75 milliseconds
    
    """
    execution time is intentionally calculated in the read_item function as we are caching the result
    and the function we return caches execution time if its calculated inside the function thats using cache.
    So calculating it here so its more accurate per request.

    """
    
if __name__ == '__main__':
    uvicorn.run(app, port=8000,host="0.0.0.0")  #   running the app on common port 8000
