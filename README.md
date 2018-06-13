### Scope of the MVP (Minimal Viable Product)

#### What does this MVP do?

- Parses the container index and creates OpenShift Pipelines (based on Jenkins
  Pipeline)
- The newly created OpenShift Pipelines are triggered at the time of creation
- Lints the Dockerfile
- Builds the container image. Can do parallel builds using sinngle Docker
  daemon at the same time
- Scans the container image for RPM updates and RPM verification (`rpm -Va`)
- Delivers the container image to external registry (`docker-distribution`)

#### What does this MVP not do?

- It doesn't poll the remote repositories to automatically trigger a build when
  there's an update in the repo
- It doesn't have parent-child relationship between images
- There's no weekly scan, repo tracking, etc. which are the parts of existing
  container pipeline
- Above discussed points will be added gradually to the Pipeline but not on
  this branch
- Registry cleanup is not covered. The external registry you use could get full
  depending on the amount of projects you're building

#### How to work with this MVP?

- Once you've followed the instruction to setup the MVP using either minishift
  or `oc cluster up`, you need to open the OpenShift web console (IP-port
  combination will be provided by minishift or `oc cluster up`, whichever you
  use)
- In the web console, login using the user `developer`
- To see the OpenShift Pipelines in action, hover your mouse over "Builds" on
  the side-bar at left and click on "Pipelines"
- To trigger a build (lint + build + scan + delivery) for any project after the
  first build, you'll have to manually click on "Start Build"

### Let's get started!

To spin up things in an OpenShift cluster based on the contents in this
repository, please make sure you have a minishift based VM or a CentOS VM with
root privileges. You'll also need to spin up Docker Distribution (registry) on
same VM or different VM.

### Docker Distribution (registry) setup

The system on which you'd like to setup the registry, execute following
commands:

```bash
$ yum install -y docker-distribution
$ systemctl enable --now docker-distribution
```

Also make sure that the firewall rules are not blocking access to the registry
(port 5000 by default.)

### OpenShift setup

**Minishift**

Start the minishift VM using below command:

```bash
$ minishift start --disk-size 50GB --memory 8GB --iso-url centos --openshift-version 3.9.0 --insecure-registry <registry-ip>:<port>
```

Memory and storage can be varied based on availability. It is recommended to
have 4GB memory and 20GB disk space as minimum. However, make sure to use
`--iso-url centos` part in above command as we have setup things on CentOS based
minishift VM. 

**CentOS VM**

A CentOS VM with 8GB memory and 50GB disk space should suffice. You can adjust
the resources based on availability. It is recommended to have 4GB memory and
20GB disk space as minimum.

In the VM, install docker and enable openshift origin repos:

```bash
$ yum install -y docker git centos-release-openshift-origin
$ yum install -y origin-clients
```

Edit Docker config to support OpenShift's internal registry and the external
registry we created in earlier step. Update `/etc/docker/daemon.json`

```json
{
"insecure-registries":["172.30.0.0/16", "<registry-ip>:<port>"]
}
```

Now enable docker and bring up the oc cluster

```bash
$ systemctl enable --now docker
$ oc cluster up --public-hostname=<IP address of the VM>
```

This will bring up the OpenShift cluster with latest verion of OpenShift origin.

**Bringing up the service**

Once the VM is ready with OpenShift cluster in it, spin up a Jenkins server
that can be used by the Jenkins Pipeline buildconfigs. Also, since we're going
to be building images using Jenkins pods, we need to add few capabilities to
the Jenkins service account.

Do this on host system:

```bash
$ oc login -u system:admin
$ oc process -p MEMORY_LIMIT=1Gi openshift//jenkins-persistent| oc create -f -
$ oc adm policy add-scc-to-user privileged system:serviceaccount:myproject:jenkins
$ oc adm policy add-role-to-user system:image-builder system:serviceaccount:myproject:jenkins
```

This spins up a persistent Jenkins deployment which has 1 GB memory alloted to
it. The Jenkins service spun up by this template is recognized and used by the
Jenkins Pipelines.

Now, clone this repo on host system (not the VM). Login to the OpenShift
cluster as user `developer` and create a build from the buildconfig under
`seed-job` directory:

```bash
# on host system
$ git clone https://github.com/dharmit/ccp-openshift/
$ cd ccp-openshift
$ oc login -u developer
<use any password>
$ oc process -p PIPELINE_BRANCH=<branch-name> -p JENKINSFILE_GIT_BRANCH=<branch-name> -p REGISTRY_URL=<registry-ip>:<port> -f seed-job/buildtemplate.yaml |oc create -f -
```

`<branch-name>` in above command needs to be replaced with the branch of this
repo (or its fork - for dev purposes) you want to use to deploy.

Now check in the OpenShift web console under Build -> Pipelines and see if a
Jenkins Pipeline has been created. Be patient because the image being used is
quite large (2.2 GB) at the moment.

To be able to build multiple container images at the same time, edit the
Jenkins deployment and add an environment variable `JENKINS_JAVA_OVERRIDES` to
it with the value
`-Dhudson.slaves.NodeProvisioner.initialDelay=0,-Dhudson.slaves.NodeProvisioner.MARGIN=50,-Dhudson.slaves.NodeProvisioner.MARGIN0=0.85`.

Since you changed the configuration, wait for the a new deployment to take
effect. Once it's done, exec into the Jenkins pod and check the output of `ps
-ef`. The three configuration options we added above should up in the `java`
command as space-separated and not comma-separated. Refer [this
diff](https://github.com/openshift/openshift-docs/pull/7259/files?short_path=05f80f3#diff-05f80f3ab954ce57c630417065819109)
to ensure that values are passed properly.
