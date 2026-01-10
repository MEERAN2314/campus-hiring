# Docker Commands for HireWave

## Development Environment

### Start all services
```bash
docker-compose up -d
```

### Start with build
```bash
docker-compose up -d --build
```

### View logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f web
docker-compose logs -f celery_worker
docker-compose logs -f redis
```

### Stop services
```bash
docker-compose down
```

### Stop and remove volumes
```bash
docker-compose down -v
```

### Restart a service
```bash
docker-compose restart web
```

### Execute commands in container
```bash
# Access web container shell
docker-compose exec web bash

# Run Python script
docker-compose exec web python seed_data.py

# Access Redis CLI
docker-compose exec redis redis-cli
```

## Production Environment

### Start production services
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Build and start
```bash
docker-compose -f docker-compose.prod.yml up -d --build
```

### View production logs
```bash
docker-compose -f docker-compose.prod.yml logs -f
```

### Stop production services
```bash
docker-compose -f docker-compose.prod.yml down
```

## Maintenance Commands

### Clean up unused Docker resources
```bash
# Remove stopped containers
docker container prune

# Remove unused images
docker image prune -a

# Remove unused volumes
docker volume prune

# Remove everything unused
docker system prune -a --volumes
```

### Check container status
```bash
docker-compose ps
```

### Check resource usage
```bash
docker stats
```

### Inspect container
```bash
docker-compose exec web env
```

## Database Operations

### Seed database
```bash
docker-compose exec web python seed_data.py
```

### Backup uploads
```bash
docker cp hirewave-web:/app/uploads ./backup-uploads
```

### Restore uploads
```bash
docker cp ./backup-uploads hirewave-web:/app/uploads
```

## Troubleshooting

### Rebuild without cache
```bash
docker-compose build --no-cache
docker-compose up -d
```

### Check health status
```bash
docker-compose ps
docker inspect --format='{{.State.Health.Status}}' hirewave-web
```

### View container logs with timestamps
```bash
docker-compose logs -f --timestamps web
```

### Access container as root
```bash
docker-compose exec -u root web bash
```

## Network Commands

### List networks
```bash
docker network ls
```

### Inspect network
```bash
docker network inspect hirewave-network
```

## Volume Commands

### List volumes
```bash
docker volume ls
```

### Inspect volume
```bash
docker volume inspect hirewave_redis_data
```

### Backup Redis data
```bash
docker run --rm -v hirewave_redis_data:/data -v $(pwd):/backup alpine tar czf /backup/redis-backup.tar.gz -C /data .
```

### Restore Redis data
```bash
docker run --rm -v hirewave_redis_data:/data -v $(pwd):/backup alpine tar xzf /backup/redis-backup.tar.gz -C /data
```
