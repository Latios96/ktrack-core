import ktrack_api


kt = ktrack_api.get_ktrack()


def main():
    paths = kt.find("path_entry", [['path', 'is', ""]])
    for path in paths:
        kt.delete("path_entry", path['id'])


if __name__ == '__main__':
    main()
