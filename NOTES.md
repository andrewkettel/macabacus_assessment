## Design & trade-offs

### Environment/API/Model Design
- Decided to split the models, routers and tests into separate folders to keep things organized if this project was to expand. 
- I chose to use a uuid4 for the Task id for its uniqueness and ability to be a database id column in most databases, though uuid7 would be better in a database since it is time ordered which makes for a more efficient index.
- I defaulted the id and created_at fields in the model so they could be ignored in the API layer. This could lead to issues which would be solved with better validation on the model and API but doesn't seem necessary in a quick prototype with no database.
- In-memory list is simple to manage but will not persist through server restart. It is sufficient for a prototype but would need to change before deployment as it will get very memory intensive as the list grows.
- Used simple one-line list comprehension for id uniqueness check, filtering, and to find the object to update. These will get slower as the in-memory list grows but using a database removes these issues.
- Implemented the id uniqueness check using the uniqueness of pythons `set` type for simplicity and efficiency. This hides which objects are colliding but is good enough for a prototype.  A DB implementation does not have this issue
- Implemented tests for the main features (API create, update, list, and filter) and a few error states (duplicate id, id not found for update)
- Skipped implementing other data validation checks as that would more test Pydantic type checking and not code in this project.  I like to see integration tests like this to validate certain parts of underlying libraries to get notified when they change but are not necessary

### Deliberate left out
- More robust data validation. The inherent type checking of Pydantic, ability to have the API ignore id and created_at, and custom id uniqueness validation seemed sufficient for a prototype. Data modeling through an ORM is where I would add more data validation.
- Error responses.  The error responses from FastAPI and Pydantic seemed sufficient for a developer to debug and troubleshoot the API but better messaging would be necessary to send to a Frontend.

If given more time, I would implement validation better. Adding restrictions to `id` and `created_at` to the create endpoint and errors if the user tries to update the id or created_at through the update endpoint. Other features like a full-fledged database, docker containers, and deploy commands would currently be overkill in my opinion until a User/Authentication system is implemented. Another useful feature that could be added quickly to make this more secure would be an API key to limit who could access the API.

## Scaling work off the request path

For a long running process, I would first use FastAPIs BackgroundTasks for the work to keep the endpoint responsive. It has some limitations though. It runs in process (limited to one cpu), can't be retried, and crashes can be silent. Depending on the use case, Celery/Redis or a cloud pub/sub queue would be more appropriate. These both allow for horizontal scaling, better monitoring, retry on failure, and are well supported by most cloud providers.

More task statuses could be implemented (like sending_notifications, processing_data) with the task updating to `done` when the background task finishes if that is necessary. The frontend could then poll the status of the long-running task and update the UI accordingly or a WebSocket could be used to send status notifications from backend to frontend. Polling is simpler but increases API requests, WebSockets are more complicated but would use less resources on the backend.

## Security & performance

For performance, a database could be used to store, retrieve, and filter tasks without the constant memory overhead of storing the list. This would also remove the list loops used for uniqueness checking, finding the object to update, and filtering which would increase responsiveness as the list gets bigger. Any of the major databases would be better at handling many inserts/updates concurrently than an in-memory list, providing atomicity, keeping the data consistent across the application. A database would also provide data persistence through app restarts which the in-memory list lacks.

For security, first thing I would add is a User and Authentication system, possibly using OAuth2 or JWT which both have support in FastAPI or even Basic Auth if this is truly a single user system. 

If this API was meant for a specific front-end, it could be locked down allow only a single IP address to reach it through the webserver or through the deploy host network settings.  If the API is meant to be open to the world, rate limiting would be a good addition. I have found a few different packages that would make this easy to implement in FastAPI or it could be handled by the host it is deployed to.  The cloud providers I have used include tools to secure endpoints including rate limiting and IP whitelisting.

Not necessarily security related but an audit log would be helpful in debugging and diagnosing bugs and issues.

## Production readiness

For production readiness, the most important features would be the security features previously discussed. Without those, it leaves the server and API layer open to attack and potential loss of data or creation of garbage data. Basic Authentication is simple and effective but would lack customizability and logging.  JWT or OAuth are well supported and can be connected to a more full-fledged User system. Rate Limiting would be useful to make sure the API responsive and ensure a smooth user experience but would be of lower importance than other security features. 

Second most important to me would be a database to keep the data persistent and consistent, remove memory and data processing overhead from the API layer, and allow for multiple API workers to spread the load. This would allow the API to grow in usage without impact to responsiveness. 

After implementing security features and a database, I would modify the project to run in a docker container so that multiple workers can easily be created and scaled up and down as necessary through kubernetes or deployed on different cloud providers easily. During that process, I would implement a health check api so that workers can be monitored and restarted as necessary to prevent downtime.

Once dockerized, I would implement process monitoring, logging/reporting, alerting, audit logs, and load balancing to ensure stability and reliability and to make it easier to debug and troubleshoot any production issues that arise. A lot of these could be handled through standard cloud provider tools (AWS CloudWatch, Google Cloud Monitoring) or off the shelf add-ons (Prometheus, Grafana).
