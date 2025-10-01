# Casnet Backend

This project is a FastAPI-based backend application designed to manage tenants, users, persons, tasks, and calendar events. It features an in-memory database for demonstration purposes and a full suite of CRUD API endpoints for each resource.

## Project Structure

The project is organized into the following main directories:

-   `src/`: Contains the main application source code.
    -   `enum/`: Defines various enumerations used across the application (e.g., `EStatus`, `EGender`).
    -   `model/`: Contains the Pydantic data models for all resources (`Tenant`, `UserAccount`, `Person`, etc.).
    -   `routers/`: Defines the API endpoints for each resource.
    -   `database.py`: Initializes the in-memory database and populates it with dummy data.
    -   `main.py`: The main entry point for the FastAPI application.
    -   `util.py`: Contains utility functions.

## API Endpoints

The application provides full CRUD (Create, Read, Update, Delete) endpoints for the following resources:

-   **Tenants**: `/tenant`
-   **Users**: `/user`
-   **Persons**: `/person`
-   **Tasks**: `/task`
-   **Calendar**: `/calendar`

For detailed information on each endpoint, please refer to the auto-generated OpenAPI documentation available at `/docs` when the application is running.

## Getting Started

To get the application running locally, follow these steps:

1.  **Install Dependencies**: Make sure you have Python and `pip` installed. Then, install the required packages:

    ```bash
    pip install fastapi "uvicorn[standard]"
    ```

2.  **Run the Application**: From the root directory of the project, run the following command:

    ```bash
    uvicorn src.main:app --reload
    ```

3.  **Access the API**: The application will be available at `http://127.0.0.1:8000`. You can access the interactive API documentation at `http://127.0.0.1:8000/docs`.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
