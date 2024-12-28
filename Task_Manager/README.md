
# Focus Flow
#### Video Demo: https://youtu.be/7zXOPIiOiqk
#### Description:
Focus Flow is a comprehensive task management website developed using Flask and SQL. Designed with user-friendliness in mind, it allows individuals to manage their tasks efficiently and effectively. The platform is tailored to provide a seamless experience, ensuring that users can focus on completing their tasks rather than navigating complex systems.

#### Project Overview:
Focus Flow is built on the robust Flask framework and utilizes SQL for database management. This combination ensures a reliable and scalable application that can handle the various needs of task management. The website offers a range of functionalities aimed at helping users organize, prioritize, and complete their tasks with ease.

#### Login and Registration:
When users first access Focus Flow, they are greeted with a login page. Here, they have the option to either log in with their existing credentials or register for a new account. The registration process is straightforward, requiring basic information to create an account. All form validations, including those for login and registration, are meticulously handled within the app routes to ensure data integrity and security.

#### Home Page:
Upon successful registration or login, users are redirected to the home page. This central hub provides easy navigation to all available actions. The design is intuitive, ensuring that users can quickly find and access the functionalities they need. Whether they want to create a new task, reschedule an existing one, or view their progress, the home page serves as the starting point for all activities.

#### Create Task:
The Create Task feature is one of the core components of Focus Flow. Users are required to fill out a form with details about the new task, including a deadline. The system performs thorough validations to ensure that all entries are correct. If an invalid deadline is provided, the user is prompted with an error message and must re-submit the form with the appropriate details. Each task must have a unique name to avoid confusion and maintain the clarity of records in the database.

#### Task Overview:
Once a task is added, users can view an overview of their tasks on the home page. This section includes,Current Tasks: A list of tasks that are currently active, Task Success Rate: A calculated metric that shows the percentage of tasks completed within their deadlines, Upcoming Tasks: Tasks that are due soon, Most Prioritized Task to Complete: The task that should be completed first based on its priority level.The Task Success Rate is calculated by dividing the number of tasks completed within the deadline by the total number of tasks completed. This metric helps users gauge their productivity and adherence to deadlines.

#### Reschedule Tasks:
Flexibility is key to effective task management, and Focus Flow provides a robust rescheduling feature. Users can access the Reschedule route to change the deadlines of their tasks. The system uses an accordion interface for users to select the task they wish to reschedule. However, tasks cannot be rescheduled to a date before the original deadline, ensuring that users adhere to realistic timelines.

#### Complete Tasks:
In the Complete route, users can mark their tasks as completed. This action updates the task status and reflects the change on the home page. Users can track their progress and see how many tasks they have successfully completed.

#### Prioritize Tasks:
Prioritization is crucial for managing multiple tasks effectively. Focus Flow allows users to prioritize tasks they deem important. Once a task is prioritized, it must be completed before any other task can be prioritized. This feature prevents users from shifting priorities haphazardly and ensures focus on the most critical tasks. If users attempt to prioritize another task without completing the current one, they are redirected to the home page with a message prompting them to finish the existing prioritized task.

#### Logout:
After performing all the desired actions the user can safely logout of the website and can use the website again using the login page.
