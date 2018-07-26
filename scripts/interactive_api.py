import ktrack_api


kt = ktrack_api.get_ktrack()


def main():
    user = {'type': 'user', 'id': '5af33abd6e87ff056014967a'}
    project = kt.create("project", {'name': 'my_test_project'})
    shot = kt.create('shot', {'project': project, 'code': 'my_test_shot'})
    task = kt.create("task",
                     {'project': project, 'entity': shot, 'assigned': user, 'name': 'my_test_task', 'step': 'anim'})


if __name__ == '__main__':
    main()
