Eclipse CROPS Builder Container
========================
This repo is to create an image that is able to build the eclipse-crops plugin
using Maven. If test projects are also provided, e.g. RCPTT projects with
pom.xml files appropriately set up, the tests will also be run. The main
difference between it and https://github.com/crops/yocto-dockerfiles is that
it has helpers to create users and groups within the container. This is so that
the output generated in the container will be readable by the user on the
host.

TL;DR
-----
```
docker build -t crops/eclipse-crops-builder .
```
```
docker run --rm -t -v $HOME/workdir:/workdir -p 5900:5900 crops/eclipse-crops-builder:neon-1a --workdir=/workdir --id $(id -u):$(id -g)
```

Running the container
---------------------
Here a very simple but usable scenario for using the container is described.
It is by no means the *only* way to run the container, but is a great starting
point.

* **Create a workdir**

  First we'll create a directory that will be used as the workspace
  and as the clone location of the project (default is from GitHub).
  The build and test results will be in this same workspace.

  ```
  mkdir $HOME/workdir
  ```

  For the rest of the instructions we'll assume the workdir chosen was
  `$HOME/workdir`.

* **The docker command**

  Assuming you used the *workdir* from above, the command
  to run a container for the first time would be:

  ```
  docker run --rm -t -v $HOME/workdir:/workdir -p 5900:5900 \
  crops/eclipse-crops-builder:neon-1a --workdir=/workdir \
  --id $(id -u):$(id -g)
  ```

  Let's discuss some of the options:
  * **_-v $HOME/workdir:/workdir**: The default location of the
    workspace inside of the container is /workdir. So this part of the
    command says to use *$HOME/workdir* as */workdir* inside the
    container.
  * **_--workdir=/workdir**: This causes the container to start in the
    workspace specified. In this case it corresponds to *$HOME/workdir* due to
    the previous *-v* argument. The container will also use the uid and gid
    of the workdir as the uid and gid of the user in the container.
  * **_--project=relative/path/to/some/project_**: This causes the
    project directory specified to be used for the build project (the git
    clone), rather than the default project which is cloned from inside the
    container. The default project is ```https://github.com/crops/eclipse-crops```.
  * **_--repo=<URI to git repo>_**: This causes the container to clone from
    the given URI rather than the default.
  * **_--branch=<git branch>_**: This causes the container to checkout the
    given branch rather than the default ('master').
  * **_--args <arguments to pass to maven>_**: Anything after **_--args_**
    will be passed to ``mvn``` when the container is launched, rather than
    the default command (```mvn -fae verify```).


  This container also launches a vncserver and a window manager, since Eclipse
  needs a DISPLAY to run. For building only, this is not needed, as Maven is
  a pure command line tool. But, if UI tests are being run with a Maven-enabled
  RCPTT project, it will launch Eclipse as the Application Under Test (AUT).

  You can observe the UI tests while they are running by connecting your
  VNC client to the container's exposed vnc port (e.g. 5900).

  On Mac OSX, this is as simple as Command-K vnc://<docker ip address>:<port>,
  e.g. ```vnc://172.17.0.2:5900/```

* **Advanced usage examples**

  * Non-default git repo and branch:
  ```docker run --rm -t -v $HOME/workdir:/workdir -p 5900:5900 crops/eclipse-crops-builder:neon-1a --workdir=/workdir --id $(id -u):$(id -g) --repo=https://github.com/moto-timo/eclipse-crops --branch=target-tests-v2```


  * Non-default mvn command:
  ```ocker run --rm -t -v $HOME/workdir:/workdir -p 5900:5900 crops/eclipse-crops-builder:neon-1a --workdir=/workdir --id $(id -u):$(id -g) --repo=https://github.com/moto-timo/eclipse-crops --branch=target-tests-v2 --args verify -rf :org.yocto.crops.target.ui.tests```
