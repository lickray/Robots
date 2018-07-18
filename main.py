from robots import Robots


def main():

    game = Robots()
    game.set_object()
    game.print_map()

    while True:
        game.move_player()
        game.move_enemy()
        if game.check():
            game.print_map()
            if game.game_over():
                game.__init__()
                game.set_object()
                game.print_map()
            else:
                break
        else:
            game.print_map()


if __name__ == '__main__':
    main()
