import lib.db

def main():
    db = lib.db.db

    db.create_tables ([
        lib.db.User,
        lib.db.Bet,
        lib.db.Wager,
        lib.db.Outcome,
    ])

if __name__ == "__main__":
    main()
