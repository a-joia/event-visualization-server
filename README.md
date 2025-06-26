# Dashboard Autogen

This project is a modern dashboard web application with a React + Material-UI (MUI) frontend and a FastAPI backend.

## Quick Start

### Running the Servers

**1. Start the Backend (FastAPI)**
```bash
cd backend
uvicorn main:app --reload
```
- Backend will be available at: http://localhost:8000

**2. Start the Frontend (React)**
```bash
cd frontend
npm run dev
```
- Frontend will be available at: http://localhost:5173

**Note:** You need to run both servers simultaneously in separate terminal windows.

## Prerequisites
- Node.js (v18+ recommended)
- npm (v9+ recommended)
- Python 3.8+

## Setup Instructions

### 1. Clone the repository
```
git clone <your-repo-url>
cd dasboard-autogen
```

### 2. Frontend Setup
```
cd frontend
npm install
npm run dev
```
- The frontend will be available at `http://localhost:5173` by default.

### 3. Backend Setup
```
python -m venv backend-venv
# On Windows:
backend-venv\Scripts\activate
# On Mac/Linux:
source backend-venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload
```
- The backend will be available at `http://localhost:8000` by default.

## How to Run the Backend

1. **Activate the Python Virtual Environment**
   - If you haven't already created it, do:
     ```sh
     python -m venv backend-venv
     ```
   - **On Windows:**
     ```sh
     backend-venv\Scripts\activate
     ```
   - **On Mac/Linux:**
     ```sh
     source backend-venv/bin/activate
     ```

2. **Install Dependencies**
   ```sh
   pip install -r backend/requirements.txt
   ```

3. **Start the FastAPI Server**
   ```sh
   cd backend
   uvicorn main:app --reload
   ```
   - The backend will be available at: http://localhost:8000
   - The `--reload` flag auto-restarts the server on code changes (great for development).

## Example: Creating a New Event via API
You can create a new event by sending a POST request to `/api/events`. Here's an example using `curl`:

```sh
curl -X POST http://localhost:8000/api/events \
  -H "Content-Type: application/json" \
  -d '{
    "id": 101,
    "name": "New Event",
    "summary": "This is a new event.",
    "status": "pending",
    "tag": "system",
    "time": "2024-06-23T15:00:00",
    "description": "## New Event\n\nThis is a **markdown** description for the new event."
  }'
```

- You should receive a JSON response confirming the event was created.
- All fields are required.

## Project Structure
- `frontend/` — React + MUI dashboard UI
- `backend/` — FastAPI backend
- `apis/` — Additional API modules (e.g., event creation)
- `docs/` — Documentation

## Sidebar Navigation
The sidebar navigation items are defined in `frontend/src/components/Sidebar.jsx` in the `navItems` array. You can add, remove, or reorder items by editing this array. Example:

```js
const navItems = [
  { name: 'Events', icon: <BarChartIcon />, path: '/events' },
  { name: 'Dashboard', icon: <HomeIcon />, path: '/dashboard' },
  // { name: 'Analytics', icon: <BarChartIcon /> },
  // { name: 'CRM', icon: <PeopleIcon /> },
  // { name: 'Page Layouts', icon: <ViewModuleIcon /> },
  // { name: 'Widgets', icon: <WidgetsIcon /> },
  // { name: 'Forms', icon: <DescriptionIcon /> },
];
```
- Only items with a `path` property will appear as navigation links.
- You can comment out or remove lines to hide items from the sidebar.
- The order of items in the array determines their order in the sidebar.

## Adding More Routes/Pages
To add a new page/route to the app:
1. **Create a new page component** in `frontend/src/pages/`, e.g. `MyNewPage.jsx`.
2. **Add a route** in `frontend/src/App.jsx` inside the `<Routes>` block:
   ```jsx
   import MyNewPage from './pages/MyNewPage';
   // ...
   <Routes>
     {/* existing routes */}
     <Route path="/my-new-page" element={<MyNewPage />} />
   </Routes>
   ```
3. **(Optional) Add a sidebar link** by editing the `navItems` array in `Sidebar.jsx`:
   ```js
   { name: 'My New Page', icon: <SomeIcon />, path: '/my-new-page' },
   ```

Now you can navigate to `/my-new-page` in your app!

## Useful Commands
- `npm run dev` — Start the frontend in development mode
- `uvicorn backend.main:app --reload` — Start the backend in development mode

---
For more details on adding new widgets, see [`docs/how-to-create-new-wirdges`](docs/how-to-create-new-wirdges) 