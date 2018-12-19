def task_hello():
    def python_hello(targets):
        with open(targets[0], "a") as output:
            output.write("Python says hellow world")
        print(targets)

    return {
        'actions': [python_hello],
        'targets': ['hellow.txt']
    }
