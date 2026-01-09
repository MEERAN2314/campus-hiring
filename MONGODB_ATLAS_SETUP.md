# MongoDB Atlas Setup Guide

## Why MongoDB Atlas?

MongoDB Atlas is a fully-managed cloud database service that provides:
- ✅ Free tier (512MB storage)
- ✅ Automatic backups
- ✅ High availability
- ✅ No server maintenance
- ✅ Global deployment
- ✅ Built-in security

Perfect for development and production!

---

## Step-by-Step Setup

### 1. Create MongoDB Atlas Account

1. Go to https://www.mongodb.com/cloud/atlas/register
2. Sign up with email or Google account
3. Verify your email address
4. Log in to Atlas dashboard

### 2. Create a Free Cluster

1. Click **"Build a Database"** or **"Create"**
2. Choose **"Shared"** (Free tier - M0)
3. Select your cloud provider:
   - AWS (recommended)
   - Google Cloud
   - Azure
4. Choose a region close to you
5. Cluster Name: `campus-hiring` (or any name)
6. Click **"Create Cluster"**
7. Wait 3-5 minutes for cluster creation

### 3. Create Database User

1. In the left sidebar, click **"Database Access"**
2. Click **"Add New Database User"**
3. Choose **"Password"** authentication
4. Set username: `campus_hiring_user` (or your choice)
5. Click **"Autogenerate Secure Password"** or set your own
6. **IMPORTANT:** Copy and save the password!
7. Database User Privileges: Select **"Read and write to any database"**
8. Click **"Add User"**

### 4. Whitelist IP Address

1. In the left sidebar, click **"Network Access"**
2. Click **"Add IP Address"**
3. For development, choose one:
   - **"Add Current IP Address"** (your current IP)
   - **"Allow Access from Anywhere"** (0.0.0.0/0) - easier for development
4. Add a comment: "Development access"
5. Click **"Confirm"**

**Note:** For production, whitelist only specific IP addresses!

### 5. Get Connection String

1. Go back to **"Database"** in the left sidebar
2. Click **"Connect"** button on your cluster
3. Choose **"Connect your application"**
4. Driver: **Python**
5. Version: **3.12 or later**
6. Copy the connection string

It will look like:
```
mongodb+srv://campus_hiring_user:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
```

### 6. Configure Your Application

1. Open your `.env` file
2. Replace `<password>` with your actual password
3. Add the database name

**Example:**
```bash
# If your password is: MySecurePass123
# And cluster is: cluster0.abc123.mongodb.net

MONGODB_URL=mongodb+srv://campus_hiring_user:MySecurePass123@cluster0.abc123.mongodb.net/?retryWrites=true&w=majority
MONGODB_DB_NAME=campus_hiring
```

**Important Notes:**
- Replace `<password>` with your actual password
- If password has special characters, URL-encode them:
  - `@` → `%40`
  - `#` → `%23`
  - `$` → `%24`
  - `%` → `%25`
  - `&` → `%26`

### 7. Test Connection

Run your application:
```bash
docker-compose up --build
```

Or locally:
```bash
./run.sh
```

Check logs for:
```
Successfully connected to MongoDB
Database indexes created successfully
```

---

## Connection String Format

### Full Format
```
mongodb+srv://<username>:<password>@<cluster-url>/<database>?retryWrites=true&w=majority
```

### Components
- `mongodb+srv://` - Protocol (uses DNS SRV records)
- `<username>` - Database user (e.g., campus_hiring_user)
- `<password>` - User password (URL-encoded if special chars)
- `<cluster-url>` - Your cluster URL (e.g., cluster0.abc123.mongodb.net)
- `<database>` - Database name (optional in connection string)
- `?retryWrites=true&w=majority` - Connection options

### Example
```
mongodb+srv://myuser:MyPass123@cluster0.abc123.mongodb.net/campus_hiring?retryWrites=true&w=majority
```

---

## Troubleshooting

### Error: "Authentication failed"
**Solution:**
- Verify username and password are correct
- Check if password has special characters (URL-encode them)
- Ensure database user was created successfully

### Error: "Connection timeout"
**Solution:**
- Check if your IP is whitelisted in Network Access
- Verify cluster is running (not paused)
- Check your internet connection
- Try whitelisting 0.0.0.0/0 for testing

### Error: "Server selection timeout"
**Solution:**
- Verify connection string format is correct
- Check cluster URL is correct
- Ensure `mongodb+srv://` protocol is used (not `mongodb://`)
- Wait a few minutes if cluster was just created

### Error: "Database user not found"
**Solution:**
- Go to Database Access and verify user exists
- Check username spelling in connection string
- Ensure user has proper permissions

### Password with Special Characters
If your password is: `MyP@ss#123`

URL-encode it: `MyP%40ss%23123`

Full connection string:
```
mongodb+srv://myuser:MyP%40ss%23123@cluster0.abc123.mongodb.net/campus_hiring
```

---

## Security Best Practices

### Development
- ✅ Use strong passwords
- ✅ Whitelist specific IPs when possible
- ✅ Use environment variables (never commit passwords)
- ✅ Create database-specific users

### Production
- ✅ Whitelist only application server IPs
- ✅ Use VPC peering (paid tiers)
- ✅ Enable encryption at rest
- ✅ Regular security audits
- ✅ Monitor access logs
- ✅ Use separate users for different services

---

## MongoDB Atlas Features

### Free Tier (M0)
- 512 MB storage
- Shared RAM
- Shared vCPU
- Perfect for development and small projects

### Monitoring
- Real-time performance metrics
- Query performance insights
- Connection statistics
- Storage usage

### Backups
- Automatic daily backups (paid tiers)
- Point-in-time recovery (paid tiers)
- Manual snapshots

### Scaling
Easy to upgrade when needed:
- M0 (Free) → M2 ($9/month) → M5 ($25/month)
- Vertical scaling (more RAM/CPU)
- Horizontal scaling (sharding)

---

## Managing Your Database

### View Data
1. Go to **"Database"** → **"Browse Collections"**
2. Select your database: `campus_hiring`
3. View collections: users, jobs, assessments, etc.
4. Browse documents

### Create Indexes
Indexes are automatically created by the application on startup!

Check in Atlas:
1. **"Database"** → **"Browse Collections"**
2. Select collection
3. Click **"Indexes"** tab

### Monitor Performance
1. **"Database"** → Click your cluster
2. **"Metrics"** tab
3. View:
   - Operations per second
   - Network traffic
   - Connections
   - Query performance

---

## Useful MongoDB Atlas Commands

### Using MongoDB Compass (GUI)
1. Download: https://www.mongodb.com/try/download/compass
2. Connect using your connection string
3. Visual interface for data management

### Using MongoDB Shell
```bash
# Install MongoDB Shell
# Download from: https://www.mongodb.com/try/download/shell

# Connect
mongosh "mongodb+srv://username:password@cluster0.abc123.mongodb.net/campus_hiring"

# List databases
show dbs

# Use database
use campus_hiring

# List collections
show collections

# Query data
db.users.find()
db.jobs.find()

# Count documents
db.applications.countDocuments()
```

---

## Cost Estimation

### Free Tier (M0)
- **Cost:** $0/month
- **Storage:** 512 MB
- **Perfect for:** Development, testing, small projects

### When to Upgrade
Upgrade when you need:
- More storage (>512 MB)
- Better performance
- Automatic backups
- More connections
- Dedicated resources

### Paid Tiers
- **M2:** $9/month (2GB storage)
- **M5:** $25/month (5GB storage)
- **M10+:** Custom pricing

---

## Quick Reference

### Connection String Template
```bash
MONGODB_URL=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority
MONGODB_DB_NAME=campus_hiring
```

### Common Issues Checklist
- [ ] Username is correct
- [ ] Password is correct (URL-encoded if needed)
- [ ] Cluster URL is correct
- [ ] IP address is whitelisted
- [ ] Database user has proper permissions
- [ ] Cluster is running (not paused)
- [ ] Using `mongodb+srv://` protocol

### Support Resources
- Atlas Documentation: https://docs.atlas.mongodb.com
- Community Forums: https://www.mongodb.com/community/forums
- University (Free courses): https://university.mongodb.com

---

## Next Steps

After setup:
1. ✅ Connection string in `.env`
2. ✅ Start your application
3. ✅ Verify connection in logs
4. ✅ Check collections are created
5. ✅ Test user registration
6. ✅ Monitor in Atlas dashboard

---

**You're all set! MongoDB Atlas is now powering your Campus Hiring Platform! 🚀**
