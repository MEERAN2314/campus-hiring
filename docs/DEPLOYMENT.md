# Deployment Guide

## Local Development

### Prerequisites
- Python 3.11+
- MongoDB
- Redis
- Google Gemini API Key

### Setup Steps

1. **Clone and Setup**
```bash
git clone <repository-url>
cd hirewave
python3 setup.py
```

2. **Configure Environment**
Edit `.env` file with your settings:
```bash
GOOGLE_API_KEY=your-gemini-api-key
MONGODB_URL=mongodb://localhost:27017
REDIS_URL=redis://localhost:6379/0
```

3. **Start Services**

Terminal 1 - Redis:
```bash
redis-server
```

Terminal 2 - FastAPI:
```bash
./run.sh
# or
make run
```

Terminal 3 - Celery Worker:
```bash
./run_celery.sh
# or
make celery
```

Note: MongoDB Atlas is cloud-hosted, no local MongoDB installation needed!

4. **Access Application**
- Web: http://localhost:8000
- API Docs: http://localhost:8000/api/docs

## Docker Deployment

### Quick Start
```bash
# Make sure .env has your MongoDB Atlas connection string
docker-compose up --build
```

This starts:
- FastAPI application (port 8000)
- Redis (port 6379)
- Celery worker

MongoDB Atlas is used as the cloud database (no local MongoDB container needed).

### Stop Services
```bash
docker-compose down
```

## Production Deployment

### Using Docker

1. **Update docker-compose.yml for production**
```yaml
# Add environment variables
# Configure volumes for persistence
# Set up reverse proxy (nginx)
```

2. **Deploy**
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Using Cloud Services

#### MongoDB Atlas (Already Configured!)
Your application is already configured to use MongoDB Atlas:
1. Connection string in .env
2. Automatic index creation
3. Cloud-hosted, no maintenance needed
4. Free tier: 512MB storage

**Connection String Format:**
```
mongodb+srv://<username>:<password>@<cluster>.mongodb.net/<dbname>?retryWrites=true&w=majority
```

**Security Best Practices:**
- Use strong passwords
- Whitelist only necessary IP addresses
- Enable authentication
- Use database-specific users
- Regular backups (Atlas does this automatically)

#### Redis Cloud
1. Create instance at redis.com/try-free
2. Get connection URL
3. Update REDIS_URL in .env

#### Deploy to Cloud Platform

**Heroku:**
```bash
heroku create hirewave-app
heroku addons:create heroku-redis:hobby-dev
heroku config:set GOOGLE_API_KEY=your-key
git push heroku main
```

**AWS EC2:**
1. Launch EC2 instance
2. Install Docker
3. Clone repository
4. Run docker-compose

**Google Cloud Run:**
```bash
gcloud builds submit --tag gcr.io/PROJECT-ID/hirewave
gcloud run deploy --image gcr.io/PROJECT-ID/hirewave --platform managed
```

## Environment Variables

Required:
- `GOOGLE_API_KEY` - Gemini API key
- `MONGODB_URL` - MongoDB connection string
- `REDIS_URL` - Redis connection string
- `JWT_SECRET_KEY` - Secret for JWT tokens

Optional:
- `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD` - Email notifications
- `MAX_UPLOAD_SIZE` - File upload limit
- `DEBUG` - Debug mode (False in production)

## Monitoring

### Logs
```bash
# Application logs
tail -f logs/app.log

# Celery logs
tail -f logs/celery.log

# Docker logs
docker-compose logs -f
```

### Health Check
```bash
curl http://localhost:8000/health
```

## Scaling

### Horizontal Scaling
- Run multiple FastAPI instances behind load balancer
- Scale Celery workers: `celery -A app.celery_worker worker --concurrency=4`

### Database
- Use MongoDB replica sets for high availability
- Enable Redis persistence

## Security Checklist

- [ ] Change all default passwords
- [ ] Use strong JWT_SECRET_KEY
- [ ] Enable HTTPS (SSL/TLS)
- [ ] Configure CORS properly
- [ ] Set up firewall rules
- [ ] Regular security updates
- [ ] Backup database regularly
- [ ] Monitor for suspicious activity

## Backup

### MongoDB Atlas Backup
MongoDB Atlas provides automatic backups:
- Continuous backups (on paid tiers)
- Point-in-time recovery
- Manual snapshots available

**Manual Export (if needed):**
```bash
# Install MongoDB Database Tools
# Download from: https://www.mongodb.com/try/download/database-tools

# Export database
mongodump --uri="mongodb+srv://username:password@cluster.mongodb.net/hirewave" --out=/backup

# Import database
mongorestore --uri="mongodb+srv://username:password@cluster.mongodb.net/hirewave" /backup/hirewave
```

## Troubleshooting

### Common Issues

**Port already in use:**
```bash
lsof -ti:8000 | xargs kill -9
```

**MongoDB connection failed:**
- Verify MongoDB Atlas connection string is correct
- Check username and password are URL-encoded
- Ensure IP address is whitelisted in Atlas Network Access
- Verify cluster is running in Atlas dashboard
- Check database user has proper permissions

**Celery tasks not running:**
- Ensure Redis is running
- Check Celery worker logs
- Verify CELERY_BROKER_URL

**AI evaluation errors:**
- Verify GOOGLE_API_KEY is valid
- Check API quota limits
- Review error logs

## Performance Optimization

1. **Database Indexing** - Already configured in database.py
2. **Caching** - Use Redis for frequently accessed data
3. **CDN** - Serve static files via CDN
4. **Compression** - Enable gzip compression
5. **Connection Pooling** - Configure MongoDB connection pool

## Support

For issues and questions:
- Check logs first
- Review documentation
- Open GitHub issue
- Contact support team
