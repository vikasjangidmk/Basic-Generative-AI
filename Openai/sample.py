def fibonacci_series(n):
    """Generate Fibonacci series up to n terms."""
    if n <= 0:
        return "Please enter a positive integer."
    series = []
    a, b = 0, 1
    for _ in range(n):
        series.append(a)
        a, b = b, a + b
    return series

# Input: Number of terms
num_terms = int(input("Enter the number of terms for the Fibonacci series: "))
print(f"Fibonacci series: {fibonacci_series(num_terms)}")
