### Poetry setup

set python version for virtual environment:
```
poetry env use <python version>
```

install dependencies
```
poetry install 
```

enter virtual environment
```
eval $(poetry env activate)
```

exit virtual environment
```
deactivate
```

### Running 

running the invoke task assumes you already have already authenticated with aws. It will assume the roles associated with the aws-profile names you pass in.

Ensure you are in a virtual environment before running the following command:

```
inv template --envs dev,qa,uat --client-name bss
```


### Larger Refactor Notes

- ansible playbook should read secrets and credentials from aws store at runtime so passwords are not stored in yaml files on machines. For example, instead of reading db_pwd and writing to .yml file, the ansible playbook should read that password from aws ssm at runtime