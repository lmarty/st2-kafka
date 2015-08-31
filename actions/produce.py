from st2actions.runners.pythonrunner import Action
from kafka import SimpleProducer, KafkaClient
from kafka.util import kafka_bytestring

class ProduceMessageAction(Action):
    """
    Action to send messages to Apache Kafka system.
    """

    def run(self, hosts, topic, message):
        """
        Simple round-robin synchronous producer to send one message to one topic.

        :param hosts: Kafka hostname(s) to connect in host:port format.
                      Comma-separated for several hosts.
        :type hosts: ``str``
        :param topic: Kafka Topic to publish the message on.
        :type topic: ``str``
        :param message: The message to publish.
        :type message: ``str``

        :returns: Response data: `topic`, target `partition` where message was sent,
                  `offset` number and `error` code (hopefully 0).
        :rtype: ``dict``
        """
        client = KafkaClient(hosts, client_id='st2-kafka-producer')
        client.ensure_topic_exists(topic)
        producer = SimpleProducer(client)
        result = producer.send_messages(topic, kafka_bytestring(message))

        if result[0]:
            return result[0].__dict__
