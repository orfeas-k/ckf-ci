# Kubeflow Operators

## Introduction

Charmed Kubeflow is a full set of Kubernetes operators to deliver the 30+ applications and services
that make up the latest version of Kubeflow, for easy operations anywhere, from workstations to
on-prem, to public cloud and edge.

A charm is a software package that includes an operator together with metadata that supports the
integration of many operators in a coherent aggregated system.

This technology leverages the Juju Operator Lifecycle Manager to provide day-0 to day-2 operations
of Kubeflow.

Visit [charmed-kubeflow.io][charmedkf] for more information.

## Install

There are two possible paths, depending on your choice of Kubernetes:

1. For any Kubernetes, follow the [installation instructions][install].
1. On MicroK8s, you simply have to enable the [Kubeflow add-on][addon].

## Testing

To deploy this bundle and run tests locally, do the following:
1. Set up Kubernetes, Juju, and deploy the bundle you're interested in (`kubeflow` or `kubeflow-lite`) using the [installation guide](https://charmed-kubeflow.io/docs/install/)
2. Install test prerequisites:
```bash
   sudo snap install juju-wait --classic
   sudo apt update
   sudo pip3 install -r requirements.txt
   sudo pip3 install tox
```
3. Run tests on your bundle with tox:
   1. full bundle: `tox -e tests -- -m full --username user123@email.com --password user123`
   2. lite bundle: `tox -e tests -- -m lite --username user123@email.com --password user123`

Subsets of the tests are also available using pytest's substring expression selector
(eg: `tox -e tests -- -m full --username user123@email.com --password user123 -k 'selenium'` to run just the selenium tests).

## Documentation

Read the [official documentation][docs].

[addon]: https://microk8s.io/docs/addon-kubeflow
[charmedkf]: https://charmed-kubeflow.io/
[docs]: https://charmed-kubeflow.io/docs/
[install]: https://charmed-kubeflow.io/docs/install
