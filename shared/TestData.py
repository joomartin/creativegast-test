
class TestData:
    RawMaterial = {
        'Bundas_kenyer':
            {
                'Name': 'Bundas_kenyer',
                'GrossPrice': '1 000.00',
                'ModifiedGrossPrice': '1 010.00',
                'ME': 'liter',
                'Warehouse': 'Szeszraktár',
                'Quantity': '10.00',
                'Quantity2': '100.00',
                'Waste': '5.00',
                'LessBySell': '8.00',
                'FloatWaste': '5.00',

            },
        'Alma':
            {
                'Name': 'Alma',
                'GrosPrice': '500',
                'ModifiedGrossPrice': '1 010.00',
                'ME': 'liter',
                'Warehouse': 'Szeszraktár',
                'Quantity': '10',
                'Quantity2': '100',
                'Waste': '5',
                'FloatWaste': '5.00',
            },
        'Csirkemell':
            {
                'Name': 'Csirkemell',
                'GrosPrice': '500',
                'ModifiedGrossPrice': '1 010.00',
                'ME': 'kg',
                'Warehouse': 'Szeszraktár',
                'Quantity': '10',
                'Quantity2': '100',
                'Waste': '5',
                'FloatWaste': '5.00',
            },

        'Finomliszt':
            {
                'Name': 'Finomliszt',
                'GrosPrice': '500',
                'ModifiedGrossPrice': '1 010.00',
                'ME': 'kg',
                'Warehouse': 'Szeszraktár',
                'Quantity': '10',
                'Quantity2': '100',
                'Waste': '5',
                'FloatWaste': '5.00',
            },
        'Almalé':
            {
                'Name': 'Almalé',
                'GrosPrice': '500',
                'ModifiedGrossPrice': '1 010.00',
                'ME': 'liter',
                'Warehouse': 'Szeszraktár',
                'Quantity': '10',
                'Quantity2': '100',
                'Waste': '5',
                'FloatWaste': '5.00',
            },

        'Hasábburgonya':
            {
                'Name': 'Hasábburgonya',
                'GrosPrice': '500',
                'ModifiedGrossPrice': '1 010.00',
                'ME': 'kg',
                'Warehouse': 'Szeszraktár',
                'Quantity': '10',
                'Quantity2': '100',
                'Waste': '5',
                'FloatWaste': '5.00',
            },
        'Sonka':
            {
                'Name': 'Sonka',
                'GrosPrice': '200',
                'ModifiedGrossPrice': '1 010.00',
                'ME': 'kg',
                'Warehouse': 'Szeszraktár',
                'Quantity': '10',
                'Quantity2': '100',
                'Waste': '5',
                'FloatWaste': '5.00',
            },
        'Paradicsomszósz':
            {
                'Name': 'Paradicsomszósz',
                'GrosPrice': '0',
                'ModifiedGrossPrice': '1 010.00',
                'ME': 'kg',
                'Warehouse': 'Szeszraktár',
                'Quantity': '10',
                'Quantity2': '100',
                'Waste': '5',
                'FloatWaste': '5.00',
            },

    }


    WareHouses = {
        'Szeszraktár':
            {
                'Name': 'Szeszraktár',
            },

        'Tartalékraktár':
            {
                'Name': 'Tartalékraktár',
            }
    }


    #TODO szeritntem ez nem kell itt, simán lehet a tesztben
    StockMovement = {
        'Name': 'TestMovement',
        'Quantity': '11',
    }

    Counter = {
        'TestCounter':
            {
                'Name': 'TestCounter',
                'Position': '0'
            }
    }

    Menu = {
        'NapiMenu':
            {
                'Name': 'NapiMenu',
                'Code': '1212',
                'Price': '100',
                'GrossPrice': '127.00',
                'MenuComponentName': 'Előétel',
                'MenuComponentUnit': '1',
                'MenuComponentName2': 'Főétel',
                'MenuComponentUnit2': '1',
            }
    }

    Pizza = {
        'Sonkas_pizza':
            {
                'Name': 'Sonkas_pizza',
                'Code': '1211',
                'BaseComponentName': 'LisztTest',
                'ToppingComponentName': 'SonkaTeszt',
                'NetPrice': '1000',
                'GrossPrice': '1270.00',
                'WasteQuantity': '10',
            }
    }

    ProductGroup = {
        'Egyeb':
            {
                'Name': 'Egyeb',
                'Conveniences': 'Gyártmányok'
            },
        'Öntetek':
            {
                'Name': 'Öntetek',
                'Conveniences': 'Gyártmányok'
            }
    }

    Product = {
        'Babgulyás':
            {
                'Name': 'Babgulyás',
                'Code': '99',
                'NetPrice': '100',
                'ComponentName': 'TestComponent',
                'Quantity': '10',
            },
        'Palacsinta':
            {
                'Name': 'Palacsinta',
                'Code': '73',
                'NetPrice': '100',
                'ComponentName': 'TestComponent',
                'Quantity': '2',
            },

        'Hasábburgonya':
            {
                'Name': 'Hasábburgonya',
                'Code': '01',
                'ProductGroup': 'Köretek',
                'NetPrice': '400',
                'ComponentName': 'Hasábburgonya',
                'Quantity': '0.18',
            },
        'Sonka':
            {
                'Name': 'Sonka',
                'Code': '03',
                'ProductGroup': 'Pizza feltét',
                'NetPrice': '200',
                'ComponentName': 'Sonka',
                'Quantity': '0.1',
            },
        'Paradicsomszósz':
            {
                'Name': 'Paradicsomszósz',
                'Code': '04',
                'ProductGroup': 'Szószok',
                'NetPrice': '200',
                'ComponentName': 'Paradicsomszósz',
                'Quantity': '0.05',
            },
    }

    Partner = {
        'Szallito':
            {
                'Name': 'Szallito',
                'Id': '01'
            }
    }

    Table = {
        'Normal':
            {
                'Name': 'Teszt asztal',
                'Type': 'Normál'
            },

        'Courier':
            {
                'Name': 'Net Pincér',
                'Type': 'Futár'
            },

        'Boss':
            {
                'Name': 'Boss',
                'Type': 'Főnöki'
            },
    }

    Client = {
        'Pista':
            {
                'Name': 'Pista',
                'Code': '987654321',
                'Phone': '123456789',
                'Discount': '10',
                'TaxNumber': '2468',
                'Country': 'Hungary',
                'PostalCode': '1171',
                'City': 'Budapest',
                'Street': 'Csak utca',
                'HouseNumber': '1'
            }
    }

    DiscountCard = {
        'White Friday':
            {
                'Name': 'White Friday',
                'Code': 'White10',
                'Category': 'Ital',
                'ProductGroup': 'Üdítők',
                'Product': 'Cola', # valszeg ez amjd nem fog kelleni itt ahogy a product group se
                'Discount': '10',
            },
        'Blue Friday':
            {
                'Name': 'Blue Friday',
                'Code': 'Blue10',
                'Category': 'Étel',
                'Discount': '10',
            }
    }





