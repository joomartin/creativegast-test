
class TestData:

    RawMaterial = {
        'Bundas_kenyer':
            {
                'Name': 'Bundas_kenyer',
                'GrosPrice': '1000',
                'ModifiedGrossPrice': '1 010.00',
                'ME': 'liter',
                'Warehouse': 'Szeszraktár',
                'Quantity': '10',
                'Quantity2': '100',
                'FloatQuantity': '10.00',
                'NetPrice': '787.40',
                'NetValue': '7 874.02',
                'WhValue': '10000',
                'OpenQuantity': '10',
                'Waste': '5',
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
                'FloatQuantity': '10.00',
                'NetPrice': '787.40',
                'NetValue': '7 874.02',
                'WhValue': '10000',
                'OpenQuantity': '10',
                'Waste': '5',
                'FloatWaste': '5.00',
            }
    }

    WareHouses = {
        'Szeszraktár':
            {
                'Name': 'Szeszraktár',
                'ModifiedName': 'ModifiedWarehouse',
                'MoveQuantity': '5'
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
                'Position': '0',
                'ModifiedName': 'ModifiedCounter',
                'ModifiedPosition': '7'
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
                'ModifiedName': 'ModifiedName',
                'ModifiedPrice': '300',
                'ModifiedGrossPrice': '381.00'
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
                'GrossPrice': '1 270.00',
                'ModifiedName': 'ModifiedPizza',
                'ModifiedNetPrice': '3000',
                'ModifiedGrossPrice': '3 810.00',
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
                'Code2': '3131999',
                'NetPrice': '100',
                'ComponentName': 'TestComponent',
                'Quantity': '2',
                'ModifiedName': 'ModifiedProduct',
                'ModifiedCode': '11',
                'ModifiedPrice': '200',
                'ModifiedQuantity': '2',
                'ModifiedComponent': 'TestComponent2'
            },
        'Palacsinta':
            {
                'Name': 'Palacsinta',
                'Code': '73',
                'Code2': '71717171',
                'NetPrice': '100',
                'ComponentName': 'TestComponent',
                'Quantity': '2',
                'ModifiedName': 'ModifiedProduct',
                'ModifiedCode': '11',
                'ModifiedPrice': '200',
                'ModifiedQuantity': '2',
                'ModifiedComponent': 'TestComponent2'
            }

    }

    Partner={
        'Szallito':
            {
                'Name': 'Szallito',
                'Id': '01'
            }
    }
