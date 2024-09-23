# Task 9 ==============================================

def memoize(func):
    cache = {}

    def memoized_func(*args):
        if args in cache:
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result

    return memoized_func


@memoize
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)


@memoize
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)



print(factorial(5))
print(factorial(6))

print(fibonacci(10))
print(fibonacci(20))

