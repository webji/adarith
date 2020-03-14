import os
import pygame as pg


def quit():
    print(f'Good bye')

def main():
    numpass, numfail = pg.init()
    print(f'pass:{numpass}, fail:{numfail}')

    inited = pg.get_init()
    print(f'Inited: {inited}')

    try:
        raise pg.error('Custom Error')
    except RuntimeError as re:
        print(f'Exception: {re}')

    pg.set_error('Set Error')
    err = pg.get_error()
    print(f'Error: {err}')

    major, minor, path = pg.get_sdl_version()
    print(f'SDL: {major}.{minor}.{path}')

    pg.register_quit(quit)

    unencoded = '你好'
    encoded = pg.encode_string(unencoded, encoding='utf-8')
    print(f'Encoded: {encoded}, Original: {unencoded}')

    encoded_path = pg.encode_file_path(os.path.join(__file__))
    print(f'Encoded Path: {encoded_path}')

    print(f'{pg.version.PygameVersion(1, 2, 3)}, {pg.vernum}')

if __name__ == '__main__':
    main()
