Desafio python
================

### Documentação da api

#### Criar usuário.
```sh
    >>> curl -X POST -H "Content-Type: application/json" -d '{"name": "Henrique Lopes", "email": "contato@henriquelopes.com", "password": "00000000"}' https://python-challenge.herokuapp.com/user
```

#### Logar usuário.
```sh
    >>> curl -X POST -H "Content-Type: application/json" -d '{"email": "contato@henriquelopes.com", "password": "00000000"}' https://python-challenge.herokuapp.com/login
```

#### Acessar profile do usuário.
```sh
    >>> curl -X GET -H "X-TOKEN:x1x1x1" https://python-challenge.herokuapp.com/profile
```


### Criar ambiente.
```sh
    >>> make venv
    >>> source venv/bin/activate
    >>> make setup-local
```

### Executar testes.
```sh
    >>> make test
```

### Executar coverage.
```sh
    >>> make test-cov
```
