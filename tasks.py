from invoke import task

@task
def foo(_, client: str):
    print(f"hello {client}")