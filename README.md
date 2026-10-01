# robotics-turtlebot3

Dockerized ROS 2 Humble Development Environment.

## Syarat

* Docker Engine >= 24
* Docker Compose >= v2.20
* Git >= 2.34
* WSL 2 + Ubuntu 22.04 untuk pengguna Windows

ROS 2 tidak perlu dipasang di host karena ROS 2 dijalankan di dalam Docker.

## Struktur Project

```text
robotics-turtlebot3/
├── docker/
│   ├── Dockerfile
│   ├── compose.yaml
│   ├── compose.wsl.yaml
│   └── entrypoint.sh
├── src/
│   └── my_first_robot_package/
├── docs/
├── config/
├── data/
├── launch/
├── maps/
└── tests/
```

## Cara Menjalankan

Clone repository:

```bash
git clone git@github.com:dhiyauu/robotics-turtlebot3.git
```

Masuk ke folder project:

```bash
cd robotics-turtlebot3
```

Masuk ke folder Docker:

```bash
cd docker
```

Build image:

```bash
docker compose build
```

Jalankan Docker Compose:

```bash
docker compose up
```

## Hasil yang Diharapkan

Node `talker` dan `listener` berjalan otomatis dan saling bertukar pesan.

Contoh output:

```text
m01_talker | [INFO] [talker]: Publishing: 'Hello World: 1'
m01_listener | [INFO] [listener]: I heard: [Hello World: 1]

m01_talker | [INFO] [talker]: Publishing: 'Hello World: 2'
m01_listener | [INFO] [listener]: I heard: [Hello World: 2]

m01_talker | [INFO] [talker]: Publishing: 'Hello World: 3'
m01_listener | [INFO] [listener]: I heard: [Hello World: 3]
```

Nomor pada `Publishing` dan `I heard` harus sama.

## Package ROS 2

Package yang digunakan dalam praktikum:

```text
my_first_robot_package
```

Package dibuat menggunakan:

```text
ament_python
```

Package dibangun menggunakan:

```bash
colcon build --symlink-install
```

Setelah build, source workspace:

```bash
source install/setup.bash
```

Untuk menjalankan package:

```bash
ros2 run my_first_robot_package hello_robot
```

## Pengujian Node

Untuk melihat status container:

```bash
docker compose ps
```

Untuk melihat node ROS 2:

```bash
docker compose run --rm talker ros2 node list
```

Hasil yang diharapkan:

```text
/talker
/listener
```

Untuk menguji topic `/chatter`:

```bash
docker compose run --rm talker ros2 topic echo /chatter --once
```

## Reproducibility

Repository ini dibuat agar dapat dijalankan kembali pada komputer lain yang memiliki Docker Engine dan Docker Compose.

```bash
git clone git@github.com:dhiyauu/robotics-turtlebot3.git
cd robotics-turtlebot3/docker
docker compose build
docker compose up
```

Jika `talker` dan `listener` langsung berjalan dan saling bertukar pesan tanpa instalasi ROS 2 pada host, maka environment berhasil direproduksi.

## Menghentikan Container

Untuk menghentikan container:

```bash
docker compose down
```

Untuk menghentikan container sekaligus menghapus named volume:

```bash
docker compose down -v
```
