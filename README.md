# Time serie Web server

## Docker image

Production way to deploy all your projects.

# Run Docker-compose localy

Step 1: `Build` your docker compose

```bash
sudo docker-compose -f local.yml build
```

Step 2: `Run` the compose (final step)

```bash
sudo docker-compose -f local.yml up
```

# Extra Commands

### Don't run if you only want to run localy

`Init user tables`

```bash
sudo docker-compose -f local.yml run --rm ts_webservice python manage.py makemigrations
sudo docker-compose -f local.yml run --rm ts_webservice python manage.py migrate
```

# Crear usuario administrador

Crea un usuario administrador para todo el sistema.

```bash
sudo docker-compose -f local.yml run --rm ts_webservice python manage.py createsuperuser
```
