# Magic Newton Roll Bot

## Description

Magic Newton Automation is a bot designed to automate daily tasks on the Magic Newton platform. Currently, the bot supports the daily roll feature, which allows users to perform daily dice rolls to earn rewards. The bot can handle multiple user tokens and supports the use of proxies to manage requests.

## Features

- Automates daily dice roll tasks
- Supports multiple user tokens
- Uses proxies to manage requests
- Displays user information and quest status
- Configurable delays between tasks

## How to Use

### Requirements

- Python 3.10
- Recommended to use a virtual environment to avoid module conflicts

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/0xsyo/magicnewton.git
    cd magicnewton
    ```

2. Create and activate a virtual environment:
    ```bash
    # On Windows
    python -m venv venv
    venv\Scripts\activate

    # On Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install the required modules:
    ```bash
    pip install -r requirements.txt
    ```

### Configuration

1. Create a `token.txt` file in the root directory and add your user tokens, one per line.
2. (Optional) Create a `proxy.txt` file in the root directory and add your proxy addresses, one per line.

### Running the Bot

- On Windows:
    ```bash
    python main.py
    ```

- On Linux:
    ```bash
    python3 main.py
    ```

## Disclaimer

I am not responsible for any issues or damages that may arise from using this bot. Use it at your own risk and make sure to comply with the terms of service of the Magic Newton platform.

---

# Magic Newton Roll Bot

## Deskripsi

Magic Newton Automation adalah bot yang dirancang untuk mengotomatiskan tugas harian di platform Magic Newton. Saat ini, bot mendukung fitur roll harian, yang memungkinkan pengguna untuk melakukan roll dadu harian untuk mendapatkan hadiah. Bot dapat menangani beberapa token pengguna dan mendukung penggunaan proxy untuk mengelola permintaan.

## Fitur

- Mengotomatiskan tugas roll dadu harian
- Mendukung beberapa token pengguna
- Menggunakan proxy untuk mengelola permintaan
- Menampilkan informasi pengguna dan status quest
- Penundaan yang dapat dikonfigurasi antara tugas

## Cara Menggunakan

### Persyaratan

- Python 3.10
- Disarankan menggunakan virtual environment untuk menghindari konflik modul

### Instalasi

1. Clone repository:
    ```bash
    git clone https://github.com/0xsyo/magicnewton.git
    cd magicnewton
    ```

2. Buat dan aktifkan virtual environment:
    ```bash
    # Pada Windows
    python -m venv venv
    venv\Scripts\activate

    # Pada Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Instal modul yang diperlukan:
    ```bash
    pip install -r requirements.txt
    ```

### Konfigurasi

1. Buat file `token.txt` di direktori root dan tambahkan token pengguna Anda, satu per baris.
2. (Opsional) Buat file `proxy.txt` di direktori root dan tambahkan alamat proxy Anda, satu per baris.

### Menjalankan Bot

- Pada Windows:
    ```bash
    python main.py
    ```

- Pada Linux:
    ```bash
    python3 main.py
    ```

## Disclaimer

Saya tidak bertanggung jawab atas masalah atau kerusakan yang mungkin timbul dari penggunaan bot ini. Gunakan dengan risiko Anda sendiri dan pastikan untuk mematuhi syarat dan ketentuan layanan platform Magic Newton.
