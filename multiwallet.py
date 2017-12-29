# Specter MultiWallet Implementation
# Nick Frichette 12/10/2017

"""The purpose of the multiwallet is to provide an interface for users
    to interact with their Specter wallets. This application will show
    all the wallets thy currently possess, as well as allow users to
    create more."""

import shutil

from wallet import *
from blockchain import *

# ANSI escape sequences
FAIL = '\033[91m'
END = '\033[0m'
OK = '\033[92m'


def create_wallet(wallets):
    wallet_name = raw_input("What would you like to name the wallet?: ")
    print "Creating " + wallet_name
    wallets[wallet_name] = Wallet(wallet_name)


def delete_wallet(wallets, wallet_name):
    answer = raw_input("Are you sure you want to delete this wallet? It cannot be undone[y/n]: ")
    if answer == 'n':
        print FAIL + "Deletion aborted" + END
    elif answer == 'y':
        name = wallet_name.name
        print "Wallet to delete: " + name
        proof = raw_input("Please type the name of the wallet to finalize decision [" + name + "]: ")
        if proof == name:
            wallets.pop(name, None)
            shutil.rmtree('key-' + name)
            raw_input("Wallet deleted! Press [Enter] to continue...")
        else:
            print FAIL + "Name improperly typed. Aborting!" + END


def specific_wallet_input(wallets, guide, index, blockchain):
    selection = ""
    selected_wallet = wallets[guide[int(index)]]
    approved_input = ['0', '1', 'd']
    while selection != 'exit':
        print "\033[H\033[J",  # Note the comma
        print "\r(0) Display Address"  # \r is to clear that line
        print "(1) Send Amount to Other Wallet"
        selected_wallet.display_address_and_balance(blockchain)
        print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        print "To delete this wallet please enter 'd' and hit [Enter]"

        selection = raw_input(selected_wallet.name + ">> ")

        # Validate input
        if selection in approved_input:
            # If the input is '0' we need to display the public address
            if selection == '0':
                print selected_wallet.get_address()
                raw_input("Press [Enter] to continue...")

            # If the input is '1' we need to send funds to a public address
            if selection == '1':
                to = raw_input("What is the public address of the wallet you'd like to send to?: ")
                amount = raw_input("How much would you like to send? [Current funds: " +
                                   str(selected_wallet.get_balance(blockchain)) + "]: ")
                transaction = selected_wallet.create_transaction(amount, to)
                selected_wallet.broadcast_transaction(transaction)
                raw_input("Transaction Complete. Press [Enter] to continue...")

            # If the input is 'd' we need to delete a wallet
            if selection == 'd':
                delete_wallet(wallets, selected_wallet)
                selection = 'exit'

        else:
            None


def main():
    wallets = {}
    blockchain = Blockchain(is_node=False)

    approved_input = ['c']
    [approved_input.append(str(x)) for x in range(100)]

    # The convention for identifying wallets it having the public and
    # private keys in a local directory with the name key-"wallet name"
    for item in os.listdir('.'):
        if 'key-' in item and 'nodekey' not in item:
            wallets[item[item.index('-') + 1:]] = Wallet(item)

    # If there are no keys, then we need to offer the chance to make a wallet
    ans = ""
    if len(wallets.keys()) == 0:
        ans = raw_input("We didn't find a wallet, would you like to create one? [y/n]: ")
        if ans == 'y':
            create_wallet(wallets)
        if ans == 'n':
            print FAIL + "With no keys we'll have to exit. Goodbye" + END
            exit(0)

    """ Now that we've loaded the wallets, lets give the users some choices """
    guide = {}
    while ans != 'exit':
        print "\033[H\033[J",  # Note the comma
        print "\rWelcome to Specter Multi_Wallet V0.02"  # \r is to clear that line
        print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        print ""
        print "To begin, select a wallet listed below"
        print ""
        for i, item in enumerate(wallets.keys()):
            guide[i] = item
            print "(" + str(i) + ") " + wallets[item].name
        print ""
        print "To select a wallet please enter a number and hit [Enter]"
        print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        print "To create a wallet please enter 'c' and hit [Enter]"
        print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

        ans = raw_input(">> ")

        # Validate input
        if ans in approved_input:
            # If the input is 'c' we need to create a new wallet
            if ans == 'c':
                create_wallet(wallets)

            # If the user selects a number, we should check if it is a valid selection
            elif guide[int(ans)] in wallets.keys():
                specific_wallet_input(wallets, guide, ans, blockchain)
        else:
            None


if __name__ == '__main__':
    main()

