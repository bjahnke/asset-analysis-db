FROM postgres:latest

# Set environment variables
ENV POSTGRES_USER postgres
ENV POSTGRES_PASSWORD password
ENV POSTGRES_DB asset_analysis

# Copy the schema and migration files
COPY ../schema /docker-entrypoint-initdb.d/