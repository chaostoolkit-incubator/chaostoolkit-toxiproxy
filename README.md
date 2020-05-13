# Chaos Toolkit Driver for Toxiproxy

[![Build Status](https://travis-ci.org/chaostoolkit-incubator/chaostoolkit-toxiproxy.svg?branch=master)](https://travis-ci.org/chaostoolkit-incubator/chaostoolkit-toxiproxy)
[![Python versions](https://img.shields.io/pypi/pyversions/chaostoolkit-toxiproxy.svg)](https://www.python.org/)

Welcome to the [Chaos Toolkit][chaostoolkit] driver for [Toxiproxy][toxiproxy]! This extension allows you to setup toxy proxy probes and methods from chaostoolkit by leveraging the toxyproxy [http management api](https://github.com/Shopify/toxiproxy#http-api). 

[toxiproxy]: https://github.com/Shopify/toxiproxy
[chaostoolkit]: http://chaostoolkit.org

## Install
1. Install the [Toxiproxy base client](https://github.com/Shopify/toxiproxy/releases)
2. Install the [Toxiproxy CLI](https://github.com/Shopify/toxiproxy/releases)

### Driver
This package requires Python 3.5+

To be used from your experiment, this package must be installed in the Python
environment where [chaostoolkit][] already lives.

```
$ pip install -U chaostoolkit-toxiproxy
```

## Usage

### Configuration
First, run the Toxiproxy base client locally to create a `localhost:8474` host on your computer. Then [create a proxy](https://github.com/Shopify/toxiproxy#2-populating-toxiproxy).

Next, to start using the actions and probes all you need to do is add the toxiproxy host with "toxiproxy_host" as the key, and optionally the port with "toxiproxy_port" as the key, to the configuration section in your experiment json. If not provided the port defaults to 8474.

Alternatively, if toxiproxy api is accessible using a reverse proxy, you can use `toxiproxy_url` setting.

Example using `toxiproxy_host` in experiment.json

```json
"configuration": {
    "toxiproxy_host" : "10.124.23.183",
    "some_environment_variable": {
      "type": "environment",
      "key": "ENVIRONMENT_VARIABLE"
    }
  },
```

Example using `toxiproxy_url` in experiment.json

```json
"configuration": {
    "toxiproxy_url" : "http://mydomain.com:8080/path-to-toxiproxy-api",
    "some_environment_variable": {
      "type": "environment",
      "key": "ENVIRONMENT_VARIABLE"
    }
  },
```

This extension follows the toxiproxy rules. A proxy is the channel where toxicity can be added. For this reason the extension is broken into proxy management and toxic management. 

All actions and probes in the extension are of python type and are used like any other python extension.

### Proxy actions

#### create_proxy

Creates a proxy to which toxics can be added. In toxiproxy a listen port of value 0 tells the API to assign a random available port. The value where the proxy is listenting will be attached to the **chaostoolkit configuration object** as *\<proxyname\>_PORT*. Should the creation of the proxy fail, an assertion error is raised stopping all subsequent actions.

|Argument|Description|Required|Default|
|--------|-----------|--------|-------|
|proxy_name|name for the proxy|Yes|None|
|upstream_host|ip address of the host to send traffic to|Yes|None|
|upstream_port|port of the application to send traffic to|Yes|None|
|listen_host| IP address to bind where toxiproxy listens|No| 0.0.0.0|
|listen_port|port to listen for requests, 0 means pick random value|No|0|
|enabled| Whether to start listening or not|No|True|

#### modify_proxy

Modify the configuration of a given proxy. Useful to change the upstream configiuration. Only arguments supplied result in modification of the proxy.

|Argument|Description|Required|Default|
|--------|-----------|--------|-------|
|proxy_name|name for the proxy|Yes|None|
|listen_addres|ip:port address to modify|No|None|
|upstream_addres|ip:port of the upstream|No|None|
|enabled| Toggle enabled/disabled state|No|None|

#### disable_proxy

Disables the proxy, this is useful to simulate a proxied service being down.

|Argument|Description|Required|Default|
|--------|-----------|--------|-------|
|proxy_name|name for the proxy to disable|Yes|None|


#### enable_proxy

Enables a disabled proxy.

|Argument|Description|Required|Default|
|--------|-----------|--------|-------|
|proxy_name|name for the proxy to enable|Yes|None|

#### delete_proxy

Removes the proxy from the system.

Example usage

```json
 "method": [
      {
            "type": "action",
            "name": "setup_toxiproxy_proxy",
            "provider": {
                "type": "python",
                "module": "chaostoxi.proxy.actions",
                "func": "create_proxy",
                "arguments": {
                    "proxy_name": "myproxy",
                    "listen_port" : 6666,
                    "upstream_host" : "10.28.188.118",
                    "upstream_port" : 6040
                }
            },
            "pauses": {
                "after": 1
            }
        }
      ] 
```

#### reset

Enable all proxies and remove all active toxics.

Example usage:  
```json
"method": [
    {
        "type": "action",
        "name": "reset all proxies",
        "provider": {
            "type": "python",
            "module": "chaostoxi.proxy.actions",
            "func": "reset"
        },
        "pauses": {
            "after": 1
        }
    }
]
```

### Proxy pobes

#### proxy_exist

Returns True of False if a given proxy exists.

|Argument|Description|Required|Default|
|--------|-----------|--------|-------|
|proxy_name|name for the proxy|Yes|None|


### Toxic actions
All actions provided by this extension match the types and attributes of [toxics](https://github.com/Shopify/toxiproxy#toxics). 

#### create\_toxic

Allows you to create any of the supported types of toxics with their attributes. 

|Argument|Description|Required|Default|
|--------|-----------|--------|-------|
|for_proxy|name for the proxy to attach the toxy|Yes|None|
|toxic_name|name for this toxy|Yes|None|
|toxic_type|A valid toxic type|Yes|None|
|stream| The direction of the toxic "upstream" or "downstream"|No|downstream|
|toxicity|Percentage of toxiciy 1.0 is 100%, 0.5 is 50% etc| No| 1.0|
|attributes|Dictionary of attributes for the type of toxic|No|None|

#### create\_latency\_toxic

Add a delay to all data going through the proxy using a downstream with a toxicity of 100%.

|Argument|Description|Required|Default|
|--------|-----------|--------|-------|
|for_proxy|name for the proxy to attach the toxy|Yes|None|
|toxic_name|name for this toxy|Yes|None|
|latency| time in milliseconds to add for latency| Yes|None|
|jitter| time in milliseconds to jitter|No|0

#### create\_bandwith\_degradation\_toxic

Limit the bandwith of a  downstream connection with a toxicity of 100%.

|Argument|Description|Required|Default|
|--------|-----------|--------|-------|
|for_proxy|name for the proxy to attach the toxy|Yes|None|
|toxic_name|name for this toxy|Yes|None|
|rate| desired bandwith rate in KB/s| Yes|None|

#### create\_slow\_connection\_close\_toxic

Generate as downstream delayed TCP close with a toxicity of 100%.

|Argument|Description|Required|Default|
|--------|-----------|--------|-------|
|for_proxy|name for the proxy to attach the toxy|Yes|None|
|toxic_name|name for this toxy|Yes|None|
|delay| desired close delay in milliseconds| Yes|None|

#### create\_slicer\_toxic

Slices TCP data up into small bits, optionally adding a delay between each sliced "packet" with a toxicity of 100%.

|Argument|Description|Required|Default|
|--------|-----------|--------|-------|
|for_proxy|name for the proxy to attach the toxy|Yes|None|
|toxic_name|name for this toxy|Yes|None|
|average_size| size in bytes for the average package| Yes|None|
|size_variation| variation in bytes of an average pkg (should be smaller than average_size)|Yes|None
|delay| time in microseconds to delay each packet by|Yes|None

#### create\_limiter\_toxic

Closes connections when transmitted data after the limit, sets it up as a dowsntream, 100% toxicity.

|Argument|Description|Required|Default|
|--------|-----------|--------|-------|
|for_proxy|name for the proxy to attach the toxy|Yes|None|
|toxic_name|name for this toxy|Yes|None|
|bytes| number of bytes to transmit before connection is closed| Yes|None|

#### delete\_toxic

Deletes the a given toxic.

|Argument|Description|Required|Default|
|--------|-----------|--------|-------|
|for_proxy|name for the proxy to attach the toxy|Yes|None|
|toxic_name|name for this toxy|Yes|None|

Example usage:

```json
 "method": [        
      {
            "type": "action",
            "name": "create_latency_toxic",
            "provider": {
                "type": "python",
                "module": "toxiproxy.toxic.actions",
                "func": "create_dowsntream_latency_toxic",
                "arguments": {
                    "for_proxy": "edsproxy",
                    "toxic_name": "latency_toxic",
                    "latency": 5000,
                    "jitter": 200
                }
            },
            "pauses": {
                "after": 1
            }
        }    
 ]
```

## Contribute

If you wish to contribute more functions to this package, you are more than
welcome to do so. Please, fork this project, make your changes following the
usual [PEP 8][pep8] code style, sprinkling with tests and submit a PR for
review.

[pep8]: https://pycodestyle.readthedocs.io/en/latest/

The Chaos Toolkit projects require all contributors must sign a
[Developer Certificate of Origin][dco] on each commit they would like to merge
into the master branch of the repository. Please, make sure you can abide by
the rules of the DCO before submitting a PR.

[dco]: https://github.com/probot/dco#how-it-works

### Develop

If you wish to develop on this project, make sure to install the development
dependencies. But first, [create a virtual environment][venv] and then install
those dependencies.

[venv]: http://chaostoolkit.org/reference/usage/install/#create-a-virtual-environment

```console
$ pip install -r requirements-dev.txt -r requirements.txt
```

Then, point your environment to this directory:

```console
$ python setup.py develop
```

Now, you can edit the files and they will be automatically be seen by your
environment, even when running from the `chaos` command locally.

### Test

To run the unit tests for the project execute the following:

```
$ pytest
```

To run the integration tests for the project execute the following:

```
$ tox
```
