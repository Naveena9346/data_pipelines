# Environment Configuration — DataForge

## Environment Variables

Copy `.env.example` to `.env` in both `backend/` and `frontend/` directories.

### Backend Environment Variables (`backend/.env`)

```env
# General System Configuration
ENVIRONMENT=development
LOG_LEVEL=INFO
SECRET_KEY=dataforge_super_secret_development_key_change_in_production
ACCESS_TOKEN_EXPIRE_MINUTES=480

# Database Configuration
DATABASE_URL=postgresql+asyncpg://dataforge_user:dataforge_password@localhost:5432/dataforge_db
DB_POOL_SIZE=20
DB_MAX_OVERFLOW=10

# Redis & Celery Configuration
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/1

# Storage Paths
DATA_STORAGE_PATH=./data_storage
UPLOAD_TEMP_DIR=./uploads

# Security & Encryption
ENCRYPTION_KEY=super_secret_aes_32_byte_key_here!
```

### Frontend Environment Variables (`frontend/.env`)

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_APP_TITLE=DataForge Platform
VITE_ENABLE_MOCK_DATA=false
```
