""" Считыватель конфигов """

from typing import Union, Any
import yaml

Structure = Union[list, dict]


def read(paths: list) -> dict:
    """ Считывает конфиги и склеивает их между собой """

    def glue_two_configs(config1: Structure, config2: Structure) -> None:
        """ Склеивает первый конфиг со вторым рекурсивно """
        is_lists = isinstance(config1, list)
        keys = range(0, len(config2)) if is_lists else config2.keys()
        for k in keys:
            value1 = config1[k] if is_lists else config1.get(k)
            value2 = config2[k]
            if isinstance(value1, dict) and isinstance(value2, dict):
                glue_two_configs(value1, value2)
            elif isinstance(value1, list) and isinstance(value2, list):
                glue_two_configs(value1, value2)
            else:
                config1[k] = value2

    config = {}  # Результирующий конфиг
    ref_cache = {}  # Кеш найденных ссылок

    def get_dict_by_ref(ref: str, ref_path: str) -> Any:
        """ Возвращает словарь по ссылке из конфига """
        if ref in ref_cache and ref_path in ref_cache[ref]:
            return ref_cache[ref][ref_path]

        keys_path = ref_path.split('/')
        assert keys_path[0] == ''
        keys_path[0] = 'value'
        x = config[ref]
        for key in keys_path:
            x = x[key]
        ref_cache.setdefault(ref, {})[ref_path] = x
        return x

    def resolve_config_refs(parent_config: Structure, instance_key: Union[str, int]) -> None:
        """ В конфиге есть ссылки, которые нужно заменить на их значения """
        dict_config = parent_config[instance_key]

        if isinstance(dict_config, dict) and '$ref' in dict_config:
            dict_config = parent_config[instance_key] = get_dict_by_ref(dict_config['$ref'], dict_config['$path'])

        if isinstance(dict_config, dict):
            for key in dict_config.keys():
                resolve_config_refs(dict_config, key)

        elif isinstance(dict_config, list):
            for i in range(0, len(dict_config)):
                resolve_config_refs(dict_config, i)

    # Тело функции
    for path in paths:
        with open(path) as f:
            item_config = yaml.load(f, Loader=yaml.FullLoader)
        glue_two_configs(config, item_config)

    resolve_config_refs([config], 0)
    return config
