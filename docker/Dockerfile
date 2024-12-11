FROM postgres:latest

# Set environment variables
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=password
ENV POSTGRES_DB=asset_analysis

# Copy schema and migration files to the initialization directory
COPY schema/tables /docker-entrypoint-initdb.d/
COPY schema/migrations /docker-entrypoint-initdb.d/


