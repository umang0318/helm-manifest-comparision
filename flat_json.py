def flatten_json(data, parent_key='', sep='.'):
    items = {}
    if isinstance(data, dict):
        for k, v in data.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            items.update(flatten_json(v, new_key, sep=sep))
    elif isinstance(data, list):
        for i, v in enumerate(data):
            new_key = f"{parent_key}[{i}]"
            items.update(flatten_json(v, new_key, sep=sep))
    else:
        items[parent_key] = data
    return items


nested_json = {
    'apiVersion': 'apps/v1',
    'kind': 'Deployment',
    'metadata': {
        'name': 'my-app',
        'namespace': 'default',
        'labels': {'app': 'my-app'},
        'annotations': {'description': 'Full-featured deployment example'}
    },
    'spec': {
        'replicas': 3,
        'revisionHistoryLimit': 10,
        'minReadySeconds': 5,
        'progressDeadlineSeconds': 600,
        'strategy': {
            'type': 'RollingUpdate',
            'rollingUpdate': {'maxUnavailable': '25%', 'maxSurge': 1}
        },
        'selector': {'matchLabels': {'app': 'my-app'}},
        'template': {
            'metadata': {
                'labels': {'app': 'my-app'},
                'annotations': {'prometheus.io/scrape': 'true', 'prometheus.io/port': '8080'}
            },
            'spec': {
                'restartPolicy': 'Always',
                'terminationGracePeriodSeconds': 30,
                'dnsPolicy': 'ClusterFirst',
                'hostNetwork': False,
                'hostPID': False,
                'hostIPC': False,
                'serviceAccountName': 'default',
                'automountServiceAccountToken': True,
                'securityContext': {'runAsUser': 1000, 'runAsGroup': 3000, 'fsGroup': 2000},
                'nodeSelector': {'disktype': 'ssd'},
                'affinity': {
                    'nodeAffinity': {
                        'requiredDuringSchedulingIgnoredDuringExecution': {
                            'nodeSelectorTerms': [{
                                'matchExpressions': [{
                                    'key': 'kubernetes.io/e2e-az-name',
                                    'operator': 'In',
                                    'values': ['e2e-az1', 'e2e-az2']
                                }]
                            }]
                        }
                    },
                    'podAffinity': {
                        'preferredDuringSchedulingIgnoredDuringExecution': [{
                            'weight': 100,
                            'podAffinityTerm': {
                                'labelSelector': {
                                    'matchExpressions': [{
                                        'key': 'security',
                                        'operator': 'In',
                                        'values': ['S1']
                                    }]
                                },
                                'topologyKey': 'kubernetes.io/hostname'
                            }
                        }]
                    }
                },
                'tolerations': [{
                    'key': 'key1',
                    'operator': 'Equal',
                    'value': 'value1',
                    'effect': 'NoSchedule'
                }],
                'volumes': [{
                    'name': 'config-volume',
                    'configMap': {'name': 'my-config'}
                }],
                'containers': [{
                    'name': 'my-container',
                    'image': 'my-image:latest',
                    'imagePullPolicy': 'IfNotPresent',
                    'command': ['./start.sh'],
                    'args': ['--debug'],
                    'workingDir': '/app',
                    'ports': [{
                        'containerPort': 8080,
                        'name': 'http',
                        'protocol': 'TCP'
                    }],
                    'env': [
                        {'name': 'ENV_VAR', 'value': 'value'},
                        {'name': 'CONFIG_JSON', 'valueFrom': {'configMapKeyRef': {'name': 'my-config', 'key': 'config.json'}}}
                    ],
                    'envFrom': [{'secretRef': {'name': 'my-secret'}}],
                    'resources': {
                        'limits': {'memory': '512Mi', 'cpu': '1'},
                        'requests': {'memory': '256Mi', 'cpu': '0.5'}
                    },
                    'volumeMounts': [{'name': 'config-volume', 'mountPath': '/etc/config'}],
                    'lifecycle': {'preStop': {'exec': {'command': ['/bin/sh', '-c', 'sleep 10']}}},
                    'livenessProbe': {
                        'httpGet': {'path': '/healthz', 'port': 8080},
                        'initialDelaySeconds': 15,
                        'periodSeconds': 20,
                        'timeoutSeconds': 5,
                        'successThreshold': 1,
                        'failureThreshold': 3
                    },
                    'readinessProbe': {
                        'tcpSocket': {'port': 8080},
                        'initialDelaySeconds': 10,
                        'periodSeconds': 10,
                        'timeoutSeconds': 5,
                        'successThreshold': 1,
                        'failureThreshold': 3
                    }
                }],
                'initContainers': [{
                    'name': 'init-myservice',
                    'image': 'busybox:1.28',
                    'command': ['sh', '-c', 'echo Initializing...'],
                    'volumeMounts': [{'name': 'config-volume', 'mountPath': '/etc/config'}]
                }],
                'imagePullSecrets': [{'name': 'myregistrykey'}],
                'hostname': 'my-app-pod',
                'subdomain': 'my-app-headless'
            }
        }
    }
}

flat_json = flatten_json(nested_json)
for k, v in flat_json.items():
    print(f"{k}: {v}")