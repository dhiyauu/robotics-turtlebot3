FROM ros:humble-ros-base-jammy

ARG USERNAME=dev
ARG UID=1000
ARG GID=1000
SHELL ["/bin/bash", "-c"]

RUN apt-get update && apt-get install -y --no-install-recommends \
	python3-colcon-common-extensions \
	python3-pip \
	python3-rosdep \
	ros-humble-rviz2 \
	ros-humble-rqt-graph \
	ros-humble-demo-nodes-cpp \
	ros-humble-demo-nodes-py \
	git nano iputils-ping net-tools \
	mesa-utils libgl1-mesa-dri \
	&& rm -rf /var/lib/apt/lists/*

RUN groupadd -g ${GID} ${USERNAME} 2>/dev/null || true && \
	useradd -m -u ${UID} -g ${GID} -s /bin/bash ${USERNAME} && \
	echo "source /opt/ros/humble/setup.bash" >> /home/${USERNAME}/.bashrc && \
	echo "[ -f /ws/install/setup.bash ] && source /ws/install/setup.bash" \
		>> /home/${USERNAME}/.bashrc

# Folder workspace dibuat milik user, supaya named volume yang
# di-mount ke /ws/build dan /ws/install tidak dimiliki root
RUN mkdir -p /ws/src /ws/build /ws/install /ws/log && \
	chown -R ${UID}:${GID} /ws

COPY docker/entrypoint.sh /entrypoint.sh
# buang karakter CR bila file sempat tersimpan dengan line ending Windows
RUN sed -i 's/\r$//' /entrypoint.sh && chmod +x /entrypoint.sh

USER ${USERNAME}
WORKDIR /ws
ENTRYPOINT ["/entrypoint.sh"]
CMD ["bash"]
