# OnlineCinema-2.0

Repository for the development of a new Online Cinema with new functionality and fixed bugs. Project consists of several microservices, which collectively provide functionality of online cinema.

The development is conducted according to the principle of clean architecture.

Following microservices are user in the project.

- Auth microservice with JWT Tokens (In develop).
- Microservice which work with movies (Planned).
- Microservice which for with UGC, for example, likes, reviews (Planned).
- Billing microservice (Planned).
- Notifications microservice, for example, sending emails to users (Planned).

And several others (Planned).

As a API Gateway is used Nginx. If verification is required, Nginx send request to Auth microservice and if response is okay, go next.

Each microservice directory has a two README files on english and russian with detailed description of microservice work.

## How start a project?

Project root has ./start.sh file written in Bash.
It contains commands for start the project.

```bash
# Start project in develop mode.
./start.sh --type=develop

# Start project in production mode.
./start.sh --type=production
```

Project require Docker for start - [**Installation manual**](https://docs.docker.com/manuals/)
