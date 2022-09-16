from gaiaHelper import Player

player1 = Player("Torigas", 1)
player2 = Player("Aninha", 1)
player3 = Player("Teresa", 1)
player4 = Player("Paulinho", 1)
print(player1)

player1.gain_resource(25,25,50,25)

player1.avanca_track(4)
player1.avanca_track(4)
player1.avanca_track(4)
player1.avanca_track(5)
player1.avanca_track(5)
player1.avanca_track(5)
player1.avanca_track(3)
player1.avanca_track(3)
player1.avanca_track(3)


player1.make_mine(1, 1)
player1.make_mine(3, 0)
player1.make_mine(0, 0)
player1.upgrade_mine_to_comercio(True)
player1.upgrade_mine_to_comercio()
player1.upgrade_comercio_to_lab()
player1.upgrade_comercio_to_lab()

player1.general_status()
player1.gaiaform()
player1.general_status()


player1.fase_renda()
player1.fase_gaia()
player1.general_status()
