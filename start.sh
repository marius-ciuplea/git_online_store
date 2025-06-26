#!/bin/sh

# Acest script este pentru așteptarea bazei de date

# Variabile pentru baza de date
DB_HOST="db"
DB_PORT="5432"

echo "Verific disponibilitatea serviciului de bază de date $DB_HOST:$DB_PORT..."

# Așteaptă până când portul bazei de date este accesibil
until nc -z "$DB_HOST" "$DB_PORT"; do
  echo "Serviciul $DB_HOST:$DB_PORT nu este încă gata. Aștept 1 secundă..."
  sleep 1
done

echo "Serviciul $DB_HOST:$DB_PORT este acum disponibil!"

# Opțional: Rulăm comenzile Django înainte de a porni serverul
# Acestea sunt utile în development pentru a te asigura că baza de date este la zi.
echo "Rulând migrările Django (opțional)..."
python manage.py migrate --noinput

# Pornesc serverul de dezvoltare Django în prim plan
echo "Pornesc serverul de dezvoltare Django..."
exec python /app/manage.py runserver 0.0.0.0:8000