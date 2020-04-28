import config_onion
import unittest
import os


RESULT = {'config': {'value': {'connections': {'rabbitmq': {'default': ['rabbitmq1',
                                                               {'password': 123,
                                                                'user': 'root'}]}}}},
 'events': {'args': [{'amounts': {'connection': ['rabbitmq1',
                                                 {'password': 123,
                                                  'user': 'root'}],
                                  'exchange': 'products',
                                  'key': 'up.to.date'},
                      'properties': {'connection': ['rabbitmq1',
                                                    {'password': 123,
                                                     'user': 'root'}],
                                     'exchange': 'products',
                                     'key': 'up.to.date',
                                     'options': {'durable': 1,
                                                 'exchange_type': 'topic'}}}],
            'class': 'Low::Level'},
 'handlers': {'amounts': {'event': 'amounts',
                          'handler': 'Integration::Invalidate',
                          'options': {'queue': 'amounts'}},
              'or_error': {'event': 'error',
                           'options': None,
                           'queue': 'amounts'},
              'short_link': {'event': 'properties',
                             'handler': 'Integration::ShortLink',
                             'options': {'queue': 'short_link'}}}}

CONFIG_YML = '''
config:
  value:
    connections:
      rabbitmq:
        default:
          - rabbitmq
          - user: guest
            password: guest

# События
events:
  class: Low::Level
  args:
      - amounts:
          connection:
            $ref: config
            $path: /connections/rabbitmq/default
          exchange: products
          key: up.to.date
        properties:
          connection:
            $ref: config
            $path: /connections/rabbitmq/default
          exchange: products
          key: up.to.date
          options:
            exchange_type: topic
            durable: 1
'''

LISTENER_YML = '''
# Обработчики событий
handlers:
  or_error:
    event: error
    options:
    queue: amounts
  short_link:
    event: properties
    options:
      queue: short_link
    handler: Integration::ShortLink
  amounts:
    event: amounts
    options:
      queue: amounts
    handler: Integration::Invalidate

# Просто для того, чтобы перекрылись конфиги (для coverage)
config:
  value:
    connections:
      rabbitmq:
        default:
          - rabbitmq1
          - user: root
            password: 123

'''

PATH_CONFIG_YML = "/tmp/00.rabbitmq.test.config.yml"
PATH_LISTENER_YML = "/tmp/00.rabbitmq.test.listener.yml"


class Config_onionTestCase(unittest.TestCase):

    def setUp(self) -> None:
        """ Перед каждым тестом """
        with open(PATH_CONFIG_YML, "w") as f:
            f.write(CONFIG_YML)
        with open(PATH_LISTENER_YML, "w") as f:
            f.write(LISTENER_YML)

    def tearDown(self) -> None:
        os.unlink(PATH_CONFIG_YML)
        os.unlink(PATH_LISTENER_YML)

    def test_config_onion(self):
    
        config = config_onion.read([PATH_CONFIG_YML, PATH_LISTENER_YML])
        from pprint import pprint
        pprint(config)
        self.assertEqual(config, RESULT)


if __name__ == '__main__':
    unittest.main()

