import customer

# button in the gutter to run the script.
if __name__ == '__main__':
    cust = customer.Customer()
    cust.create_table()
    cust.insert(1, 'Bilbo', 'Biggins', '1234-5678-9876-5432', '04/25', '123')
    cust.insert(2, 'Frodo', 'Baggins', '9876-5432-1234-5678', '08/23', '456')
    cust.insert(3, 'Samwise', 'Gamgee', '4567-8901-2345-6789', '12/21', '789')

    print(cust.lookup(1))
    print(cust.lookup(2))
    print(cust.lookup(3))

    #cust.delete(2)






