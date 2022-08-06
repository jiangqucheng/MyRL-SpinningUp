## Select base image.
# FROM jupyter/datascience-notebook:latest
FROM pytorch/pytorch:1.11.0-cuda11.3-cudnn8-devel
# FROM nvcr.io/nvidia/pytorch:22.05-py3

# build arg: user
ARG user=test


## Update & install required packages.
RUN apt-key adv --fetch-keys http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/3bf863cc.pub \
	&& apt-get update \
	&& apt-get upgrade -y \
	&& apt-get install -y sudo wget gcc g++ python3.8 python3-pip git net-tools inetutils-ping \
	&& apt-get install -y libosmesa6-dev patchelf libgl1-mesa-dev swig xterm dbus-x11 python-opengl\
	&& apt-get install -y libopenmpi-dev \
    && apt-get clean all  \
    && rm -r /var/lib/apt/lists/* 


# add user: give sudo permit, set the passwd.
RUN useradd --create-home --no-log-init --shell /bin/bash ${user} \
    && adduser ${user} sudo \
    && echo "${user}:1" | chpasswd
# change user's UID and GID
# RUN usermod -u 1000 ${user} && usermod -G 1000 ${user}

## Create and goto workspace.
VOLUME /workspace
WORKDIR /workspace
RUN chmod -R 777 /workspace

## Select user.
USER ${user}

## Other apt packages related to OpenGL.
# apt-get install -y freeglut3-dev libglu1-mesa-dev libsoil-dev libglm-dev libassimp-dev libglew-dev libglfw3-dev libxinerama-dev libxcursor-dev libxi-dev libfreetype6-dev x11-apps mesa-utils

## 启动 box2d 可能会报错 Failed to create GLFW window 或 libGL error: No matching fbConfigs or visuals found。这被认为是 WSL 默认使用 OpenGL1.4 版本导致的。
# WSL 默认设置的是 Indirect Rendering ，最高只能支持 OpenGL1.4 ，而很多地方需要 1.5 以上。为了能支持更高的版本，我们需要设置：
#   export MESA_GL_VERSION_OVERRIDE=3.3
#   unset LIBGL_ALWAYS_INDIRECT
# 再次运行命令，就能使用 OpenGL3.3 。注意，必须设置 Indirect Rendering ，否则，上述设置 OpenGL 的命令无效。同时，Windows 下的 VcXsrv 也必须取消 Native opengl 这一选项。
# 可以直接在 config.xlaunch 中设置 XDMCPIndirect="False"，并重启服务！（确认原服务结束运行并使用更新后的配置重启实例！）

## add env exports
ENV LD_LIBRARY_PATH $LD_LIBRARY_PATH:/usr/local/nvidia/lib:/usr/local/nvidia/lib64:/usr/lib/nvidia:/home/${user}/.mujoco/mujoco210/bin:/root/.mujoco/mujoco210/bin
ENV LANG C.UTF-8
ENV MESA_GL_VERSION_OVERRIDE 3.3

## Add initialize script to container.
# ADD http://abcd.com/efgh.txt .
COPY ./setup_mujoco.py /workspace/setup_mujoco.py

# Download mujoco and set up in env.
RUN mkdir -p ~/.mujoco \
    && wget https://mujoco.org/download/mujoco210-linux-x86_64.tar.gz -O ~/mujoco.tar.gz \
    && tar -xf ~/mujoco.tar.gz -C ~/.mujoco \
    && rm ~/mujoco.tar.gz \
	&& echo "" >> ~/.bashrc \
	&& echo "# MUJOCO Settings." >> ~/.bashrc \
	&& echo "export LD_LIBRARY_PATH=\$LD_LIBRARY_PATH:/usr/local/nvidia/lib:/usr/local/nvidia/lib64:/usr/lib/nvidia:/home/${user}/.mujoco/mujoco210/bin" >> ~/.bashrc \
	&& pip3 install --no-cache-dir 'mujoco-py<2.2,>=2.1' \
	&& python3 /workspace/setup_mujoco.py \
	&& rm /workspace/setup_mujoco.py \
	&& unset LIBGL_ALWAYS_INDIRECT

# Download OpenAI/SpinningUp and set up in env. 
# Run this before compose mount the real dirctory, for start-up speed.
RUN git clone https://github.com/jiangqucheng/OpenAI-spinningup.git \
	&& cd OpenAI-spinningup \
	&& pip install -e . \
	&& cd ..

## Set entrypoint.
# ENTRYPOINT [ "jupyter", "lab", "--ip=*", "--port", "8088", "--no-browser", "--allow-root" ]
# ENTRYPOINT [ "bash" ]

