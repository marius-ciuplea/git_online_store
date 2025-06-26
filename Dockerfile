FROM debian:bookworm-slim

# Setare variabile de mediu pentru Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instalare dependențe de sistem necesare pentru Python, Node.js, netcat și compilare
# netcat (nc) este necesar pentru verificarea disponibilității bazei de date în start.sh
# build-essential, curl, git, libpq-dev sunt adăugate conform solicitării pentru robustete
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3.11 \
    python3.11-venv \
    python3-pip \
    build-essential \
    curl \
    git \
    nodejs \
    npm \
    libpq-dev \
    netcat-traditional && \
    rm -rf /var/lib/apt/lists/*

# Creează un symlink pentru python3.11 ca 'python' și 'pip'
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1 && \
    update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1

# Setează directorul de lucru principal în container
WORKDIR /app

# Creare și activare mediu virtual Python
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copiază fișierul requirements.txt și instalează dependențele Python în venv
# Această metodă profită de caching-ul Docker.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiază scriptul de pornire și fă-l executabil
# Acest script va porni atât serverul Django, cât și Tailwind CSS watch
COPY start.sh  /app/
# Acordă permisiuni pentru calea /app/start.sh
RUN chmod +x /app/start.sh

# Copiază restul codului aplicației în container
COPY . /app/

# Portul pe care va asculta serverul Django
EXPOSE 8000

# Comanda implicită care va fi rulată la pornirea containerului
# Aceasta va lansa scriptul start.sh, care gestionează pornirea ambelor servicii
CMD ["/app/start.sh"]
