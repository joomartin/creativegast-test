
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
            }
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
                'Quantity': '10',
            }

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
