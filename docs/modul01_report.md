# Laporan Praktikum Modul 1
## Dockerized ROS 2 Development Environment

### 1. Tujuan

Praktikum ini bertujuan untuk membuat lingkungan pengembangan ROS 2 Humble
menggunakan Docker sehingga ROS 2 dapat dijalankan di dalam container tanpa
perlu melakukan instalasi ROS 2 secara langsung pada host.

Selain itu, praktikum bertujuan untuk membuat package ROS 2 menggunakan
ament_python, menjalankan node talker dan listener, serta menyimpan
konfigurasi project ke dalam repository Git agar dapat digunakan kembali
pada komputer lain.

---

### 2. Lingkungan yang Digunakan

- Sistem operasi host: Windows
- Virtual environment: WSL 2
- Distribusi Linux: Ubuntu 22.04
- Docker: Docker Engine
- ROS 2: Humble
- Base image: ros:humble-ros-base-jammy
- Version control: Git
- Repository: GitHub

Project disimpan pada filesystem Linux WSL:

~/robotics-turtlebot3

dan tidak menggunakan folder /mnt/c untuk workspace utama.

---

### 3. Persiapan WSL

WSL 2 digunakan sebagai lingkungan Linux pada Windows.

Ubuntu 22.04 digunakan sebagai distribusi Linux untuk menjalankan Docker
dan workspace ROS 2.

Systemd juga dikonfigurasi pada WSL agar Docker Engine dapat dijalankan
dengan lebih mudah.

---

### 4. Konfigurasi Docker

Docker Engine dipasang di dalam Ubuntu pada WSL.

Image dasar ROS 2 Humble yang digunakan adalah:

ros:humble-ros-base-jammy

Image kemudian digunakan sebagai dasar untuk membuat environment
development ROS 2.

Dockerfile dibuat pada:

docker/Dockerfile

Sedangkan konfigurasi Docker Compose dibuat pada:

docker/compose.yaml

dan konfigurasi khusus WSL dibuat pada:

docker/compose.wsl.yaml

File entrypoint dibuat pada:

docker/entrypoint.sh

---

### 5. Pembuatan Package ROS 2

Package ROS 2 dibuat dengan nama:

my_first_robot_package

Package menggunakan build type:

ament_python

Package kemudian dibangun menggunakan colcon:

colcon build --symlink-install

Setelah proses build selesai, workspace di-source menggunakan:

source install/setup.bash

Package kemudian diuji menggunakan:

ros2 run my_first_robot_package hello_robot

Package berhasil dibuat dan dapat dijalankan di dalam container.

---

### 6. Menjalankan Docker Compose

Docker Compose dijalankan dari folder:

~/robotics-turtlebot3/docker

Perintah yang digunakan:

docker compose build

Kemudian container dijalankan dengan:

docker compose up

Docker Compose menjalankan dua service ROS 2:

- talker
- listener

Keduanya menggunakan ROS_DOMAIN_ID yang sama sehingga dapat saling
berkomunikasi.

---

### 7. Pengujian Talker dan Listener

Pengujian dilakukan dengan menjalankan:

docker compose up

Hasil yang diharapkan adalah talker melakukan publishing pesan dan
listener menerima pesan tersebut.

Contoh output:

m01_talker | [INFO] [talker]: Publishing: 'Hello World: 1'
m01_listener | [INFO] [listener]: I heard: [Hello World: 1]

m01_talker | [INFO] [talker]: Publishing: 'Hello World: 2'
m01_listener | [INFO] [listener]: I heard: [Hello World: 2]

Pengujian menunjukkan bahwa node talker dan listener berhasil
berkomunikasi.

---

### 8. Pengujian ROS 2 Node

Untuk memastikan kedua node terdeteksi oleh ROS 2, digunakan perintah:

ros2 node list

Hasil yang diharapkan:

/talker
/listener

Hasil tersebut menunjukkan bahwa kedua node ROS 2 berhasil berjalan
dan terdeteksi dalam ROS 2 graph.

---

### 9. Masalah yang Ditemui

#### 9.1 Instalasi Ubuntu 22.04 melalui WSL

Pada proses instalasi Ubuntu 22.04 menggunakan:

wsl --install -d Ubuntu-22.04

sempat terjadi error:

Wsl/InstallDistro/0x80072f78

Masalah tersebut terjadi ketika proses download Ubuntu tidak mendapatkan
respons server yang valid.

---

#### 9.2 Docker Compose tidak menemukan configuration file

Ketika menjalankan Docker Compose dari folder project utama, muncul:

no configuration file provided: not found

Masalah terjadi karena file compose.yaml berada di dalam folder:

~/robotics-turtlebot3/docker

Sehingga Docker Compose harus dijalankan dari folder docker.

---

#### 9.3 Kesalahan format compose.yaml

Saat melakukan pengecekan konfigurasi Compose, sempat muncul error:

additional properties 'service' not allowed

Masalah disebabkan oleh kesalahan penulisan struktur YAML pada
compose.yaml.

Struktur kemudian diperbaiki sehingga service talker dan listener dapat
dikenali oleh Docker Compose.

---

#### 9.4 Dockerfile parse error

Pada proses build image sempat muncul:

dockerfile parse error

Kesalahan disebabkan oleh format penulisan command pada Dockerfile,
khususnya penggunaan backslash pada perintah multi-line.

Dockerfile kemudian diperbaiki dan proses build berhasil dilakukan.

---

#### 9.5 Entry point exec format error

Container sempat berhenti dengan error:

exec /entrypoint.sh: exec format error

Masalah terjadi pada file entrypoint.sh.

File kemudian diperbaiki agar menggunakan line ending Linux dan memiliki
permission executable.

Setelah diperbaiki, container dapat dijalankan kembali.

---

### 10. Git dan Repository

Project disimpan menggunakan Git pada repository GitHub.

Repository memiliki struktur utama:

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
├── tests/
├── README.md
├── .gitignore
└── .gitattributes

Repository dibuat agar project dapat direproduksi pada komputer lain
dengan menjalankan Docker Compose.

---

### 11. Kesimpulan

Praktikum Modul 1 berhasil dilakukan dengan membuat Dockerized ROS 2
Development Environment menggunakan ROS 2 Humble.

Package my_first_robot_package berhasil dibuat dan di-build menggunakan
colcon.

Node talker dan listener berhasil dijalankan menggunakan Docker Compose
dan dapat saling bertukar pesan.

Repository GitHub juga digunakan untuk menyimpan source code,
Dockerfile, Docker Compose, README, dan laporan praktikum sehingga
environment dapat direproduksi pada komputer lain.
