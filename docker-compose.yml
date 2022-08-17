services:
  postgres:
    image: postgres:12-alpine
    restart: always
    environment:
      POSTGRES_USER: interviewee
      POSTGRES_PASSWORD: wannasucceed
      POSTGRES_DB: awesomeinc
    volumes:
      - ./data/init.sql:/docker-entrypoint-initdb.d/init.sql
      - data:/var/lib/postgresql/data
    ports:
      - ${POSTGRES_PORT:-5432}:5432
  pgadmin:
    image: dpage/pgadmin4:6
    restart: always
    environment:
      PGADMIN_DEFAULT_EMAIL: interviewee@test.com
      PGADMIN_DEFAULT_PASSWORD: wannasucceed
    volumes:
      - ./data/servers.json:/pgadmin4/servers.json
    ports:
      - ${PGADMIN_PORT:-8080}:80
    depends_on:
      - postgres
volumes:
  data: {}
