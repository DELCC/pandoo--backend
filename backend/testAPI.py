import openfoodfacts

# User-Agent is mandatory
api = openfoodfacts.API(user_agent="my-app")

code = "3254381058694"
result = api.product.get(code)

print(result)


def get_barcode_informations(code : str) -> dict :
    try :
         return api.product.get(code, fields=["code", "product_name"])
    except ValueError as e :
        raise ValueError("Le code bar n'existe pas", e)