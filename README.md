# Apache Kafka Integration Pack
This pack allows integration with [Apache Kafka](http://kafka.apache.org/), high-throughput distributed messaging system.

## Actions
* `kafka.produce` - Send *message* categorized by *topic* to Kafka *hosts*.

## Sensors

### KafkaMessageSensor
Connects to a Kafka broker, subscribing to various topics and dispatches triggers for each new message.

When receives new data, it emits:
* trigger: `kafka.new_message`
* payload:
  * `topic` - Category from which message was retrieved (string).
  * `message` - Message. JSON-serialized messages are converted to objects (object|string).
  * `partition` - Topic partition number message belongs to (integer).
  * `offset` - Consumer offset for current topic. Position of what has been consumed (integer).
  * `key` - Message's key, used only for keyed messages (string).

#### Configuration
* message_sensor:
  * `hosts` - Kafka hostname(s) to connect in host:port format. Comma-separated for several hosts. (ex: `localhost:9092`)
  * `topics` - Listen for new messages on these topics, (ex: `['test', 'meetings']`)
  * `group_id` - Consumer group (default: `st2-kafka-producer`)

## Examples
Send message to Kafka queue:
```sh
# Publish message to `meetings` topic
st2 run kafka.produce hosts=localhost:9092 topic=meetings message='StackStorm meets Apache Kafka'
# Send JSON-formatted message
st2 run kafka.produce hosts=localhost:9092 topic=test message='{"menu": {"id": "file"}}'
```

## Known Issues
Kafka `topic` should be registered before starting the sensor which listens on that topic.
Publishing message to topic and then re-running sensor should work:
```sh
# Publishing first message automatically creates the topic
st2 run kafka.produce hosts=localhost:9092 topic=test message=Hello1
st2ctl restart
# Sensor should see new message now
st2 run kafka.produce hosts=localhost:9092 topic=test message=Hello2
```
