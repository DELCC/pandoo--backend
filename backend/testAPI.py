import openfoodfacts

# User-Agent is mandatory
api = openfoodfacts.API(user_agent="my-app")

code = "3017620422003"
result = api.product.get(code, fields=["code", "product_name"])

print(result)