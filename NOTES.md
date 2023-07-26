# RabbitMQ

> docker run -d --hostname my-rabbit --name some-rabbit   rabbitmq:3-management
> git config --global alias.co checkout
> git config --global alias.br branch
> git config --global alias.ci commit
> git config --global alias.st status

AMQP(Advanced Message Queuing Protocol)

rabbitmq recommend AMQP 0-9-1

rabbitmq also support other protocols through plugin

+ STOMP -> Messaging protocol
+ MQTT -> Lightweight Protocol
+ HTTP -> For management plugins
+ Hex-STOMP


Exchange Attributes

+ Exchange type
+ Exchange name
+ Exchange durability
+ auto-delete

Message Attributes

+ Routing Key
+ Header

Used by bindings


Exchange Types

+ Default Exchange
  + Doesn't have a name
  + Creates automatic binding with every queue
  + Binding key will be the Queue name
  + Useful for simple application
+ Direct Exchange
  + Will have a name
  + Bindings are note created automatically 
  + Binding key will be the Queue name
  + Useful for simple application
+ Fanout Exchange
  + Routing key doesn't have any effect
  + Routes a copy of message to all queues
+ topic Exchange
  + Its similar to direct exchange
  + Rouing key is compared with binding patterns to route messages
+ Header Exchange
  + Message Header is used to route message
  + Messages are routed on match between message header and binding header
  + If x-match=all, then all attributes should match
  + If x-match=any, then any one attributes should match

# means 0 or one time
* means any time

## Install

> rabbitmq-plugins enable rabbitmq_management
config file
/etc/rabbitmq/rabbitmq.config

log file

/var/log/rabbitmq

startup_err
startup_log

## Add user

rabbitmqctl add_user  username apssword
rabbitmqctl set_user_tags username administrator(permission tag)
rabbitmqctl set_permissions -p / username ".*" ".*" ".*"

## RabbitMQ Environment Variables 

ON windows

setx varname varvalue

| variable name            | Default value                                                | OS               | Usage                                                                          |
|--------------------------|--------------------------------------------------------------|------------------|--------------------------------------------------------------------------------|
| RABBITMQ_BASE            | %APPDATA%RabbitMQ                                            | Windows Only     | Location where RabbitMQ has database and logs files                            |
| RABBITMQ_CONFIG_FILE     | %RABBITMQ_BASE%rabbitmq.conf                                 | Windows and Unix | Used to configure location of RabbitMQ config file                             |
| RABBITMQ_CONSOLE_LOG     | NA                                                           | Windows and Unix | Used to redirect console output from server to a file                          |
| RABBITMQ_LOGS            | Windows - %APPDATA%RabbitMQ\log,Linux: /var/log/rabbitmq     | Windows & Unix   | This variable holds the location of rabbitmq logs                              |
| RABBITMQ_LOG_BASE        | NA                                                           | Windows & Unix   | This variable hods log file base location of rabbitmq logs                     |
| RABBITMQ_MNESIA_DIR      | Linux: /var/lib/rabbitmq, Windows - %APPDATA%RabbitMQ        | Windows & Unix   | Used to configure location of Mnesia database directory                        |
| RABBITMQ_MNESIA_BASE     | NA                                                           | Windows & Unix   | Used to store base directory of Mnesia database                                |
| RABBITMQ_NODE_IP_ADDRESS | By default, it binds to all network interfaces in the server | Windows & Unix   | Used to configure the IP address to which yo want to bind your RabbitMQ server |
| RABBITMQ_NODENAME        | Linux: rabbit@hostname, Windows: rabbit@computername         | Windows & Unix   | Used to configure node name of your RabbitMQ server                            |
| RABBITMQ_NODE_PORT       | 5672                                                         | Windows & Unix   | Used to configure node binding port of your RabbitMQ server                    |
| RABBITMQ_PLUGINS_DIR     | rabbitMQ base directory                                      | Windows & Unix   | Used to configure location of RabbitMQ server plugins                          |
| RABBITMQ_SASL_LOGS       | rabbitMQ base directory                                      | Windows & Unix   | Used to configure location of system libraries logs                            |
| RABBITMQ_SERVICENAME     | rabbitmq-server                                              | Windows & Unix   | Used to configure rabbitmq service name that will be installed                 |

## RabbitMQ Config files

/opt/homebrew/etc/rabbitmq/rabbitmq.conf

> brew info rabbitmq


+ Authentication
+ Performance
+ Memory limit
+ Disc Limit
+ Exchanges
+ Queues


List and tuples in Erlang

Array

Sunset = [18,18.01,18.02]. # each line must end with .

Tuples

data = {true, 123, "hello}

Every configuration data is a tuple
	{"config name" "config value‘}

Tuples should be inside list

	[{"config name" : "config value1"}, {"config name": "config value2"}]


[{rabbit,
    [
        {tcp_listensers, [{"127.0.0.1", 5222}], 
			 [{"::1", 5222}]},
        {num_tcp_acceptors, 1}
    ]
}
].















localhost:15672  guest/guest

















binding

# RabbitMQ Cluster
                                                                  
## Types of Nodes

+  RAM node (RAM memory)
+ Disk Node (Disc memory)

> rabbitmqctl cluster_status
> 
> rabbitmqctl stop_app
> 
> nohup rabbitmq-server restart &
> 
> nohup rabbitmqctl start_app
> 

> vim /var/lib/rabbitmq/.erlang.cookie
> 
>rabbitmqctl join_cluster rabbit@masternode  --ram
> 

## Asynchronous communication

+ asynchronous communication is done using adaptor called selectConnection
+ implements IO loops for asynchronous connection
