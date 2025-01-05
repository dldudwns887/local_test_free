from decimal import Decimal

num1 = Decimal('2.4e-27')
num2 = Decimal('1.25e-26')

result = num1 + num2
print(f"Exact result using Decimal: {result}")