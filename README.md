# NAME

config_onion -  layered configuration, because configs are like ogres

# VERSION

0.0.1

# DESCRIPTION

```py
@@ config.yml

config:
  value:
    connections:
      rabbitmq:
        default:
          - rabbitmq
          - user: guest
            password: guest

events:
  - amounts:
	  connection:
		$ref: config
		$path: /connections/rabbitmq/default

@@ .config.yml
config:
  value:
    connections:
      rabbitmq:
        default:
		  - rabbitmq1
          - user: root
            password: 123


@@ my.py

from config_onion import read

config = read(['config.yml', '.config.yml'])

print(config_onion)        # -> { ... 'connection': ['rabbitmq1', {'user': 'root', 'password: 123'}] ... }
```

# SYNOPSIS

Склеивает конфиги. Так же разыменовывает ссылки вида:

```yml
$ref: ...
$path: ...
```

Такая система используется в swagger-е. В perl есть аналогичный модуль `Config::Onion`.

# FUNCTIONS

## read

### ARGUMENTS

* `configs` - список файловых путей к конфигам. Обязательный

### RETURNS

Any

# INSTALL

```sh
$ pip install config_onion
```

# REQUIREMENTS

Нет

# LICENSE

Copyright (C) Kosmina O. Yaroslav.

This library is free software; you can redistribute it and/or modify
it under the same terms as Python itself.

# AUTHOR

Kosmina O. Yaroslav <darviarush@mail.ru>

# LICENSE

MIT License

Copyright (c) 2020 Kosmina O. Yaroslav

