# How to Create New Widgets

This guide explains how to add new widgets to your dashboard UI.

## 1. Create a Widget Component
- Go to `frontend/src/components/`.
- Create a new file, e.g., `MyWidget.jsx`.
- Use Material-UI components (Card, Paper, Typography, etc.) for consistency.

Example:
```jsx
import { Card, CardContent, Typography } from '@mui/material';

const MyWidget = () => (
  <Card sx={{ borderRadius: 3, boxShadow: 3 }}>
    <CardContent>
      <Typography variant="h6">My Widget Title</Typography>
      {/* Your widget content here */}
    </CardContent>
  </Card>
);

export default MyWidget;
```

## 2. Add the Widget to the Dashboard
- Open `frontend/src/components/DashboardWidgets.jsx`.
- Import your new widget at the top:
  ```jsx
  import MyWidget from './MyWidget';
  ```
- Add your widget inside the main layout, using a `<Grid item>` for placement:
  ```jsx
  <Grid item xs={12} md={6}>
    <MyWidget />
  </Grid>
  ```

## 3. Best Practices
- Use MUI's Grid system for responsive layouts.
- Keep widget logic and UI in the same file if simple, or split into subcomponents/hooks if complex.
- Use MUI theming for consistent colors and spacing.
- Test your widget in both light and dark mode if supported.

## 4. (Optional) Connect to Backend
- Use `fetch` or a library like `axios` to get data from your FastAPI backend.
- Store data in React state/hooks.

---
For questions or suggestions, see the main README or open an issue. 