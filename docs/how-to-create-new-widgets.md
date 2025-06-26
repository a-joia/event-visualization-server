# How to Create New Widgets

This guide explains how to use the `WidgetTemplate` component to create consistent, feedback-enabled widgets for your dashboard.

## Overview

The `WidgetTemplate` component provides a standardized container for all dashboard widgets with:
- Consistent styling and layout
- Built-in feedback functionality with a chat button
- Configurable title, subtitle, and actions
- Responsive design

## Basic Usage

```jsx
import WidgetTemplate from '../components/WidgetTemplate';

function MyWidget() {
  const handleFeedbackSubmit = (feedbackData) => {
    console.log('Feedback submitted:', feedbackData);
    // Send feedback to your backend
  };

  return (
    <WidgetTemplate
      title="My Widget Title"
      height={350}
      onFeedbackSubmit={handleFeedbackSubmit}
    >
      {/* Your widget content goes here */}
      <div>Widget content</div>
    </WidgetTemplate>
  );
}
```

## WidgetTemplate Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `title` | string | required | The widget title displayed in the header |
| `children` | ReactNode | required | The widget content |
| `height` | number/string | 300 | Widget height in pixels or CSS value |
| `width` | string | '100%' | Widget width |
| `subtitle` | string | optional | Subtitle displayed below the title |
| `actions` | ReactNode | optional | Action buttons displayed in the header |
| `onFeedbackSubmit` | function | optional | Callback when feedback is submitted |

## Examples

### Simple Chart Widget

```jsx
import WidgetTemplate from '../components/WidgetTemplate';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

function ChartWidget() {
  const data = [
    { name: 'Jan', value: 400 },
    { name: 'Feb', value: 300 },
    { name: 'Mar', value: 600 },
  ];

  const handleFeedbackSubmit = (feedbackData) => {
    // Handle feedback submission
    console.log('Chart feedback:', feedbackData);
  };

  return (
    <WidgetTemplate
      title="Sales Trend"
      subtitle="Monthly sales performance"
      height={400}
      onFeedbackSubmit={handleFeedbackSubmit}
    >
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="value" stroke="#6366f1" />
        </LineChart>
      </ResponsiveContainer>
    </WidgetTemplate>
  );
}
```

### Widget with Actions

```jsx
import WidgetTemplate from '../components/WidgetTemplate';
import { Button, FormControl, InputLabel, Select, MenuItem } from '@mui/material';

function WidgetWithActions() {
  const [selectedOption, setSelectedOption] = React.useState('option1');

  const actions = (
    <>
      <FormControl size="small" sx={{ minWidth: 120 }}>
        <InputLabel>Filter</InputLabel>
        <Select
          value={selectedOption}
          label="Filter"
          onChange={(e) => setSelectedOption(e.target.value)}
        >
          <MenuItem value="option1">Option 1</MenuItem>
          <MenuItem value="option2">Option 2</MenuItem>
        </Select>
      </FormControl>
      <Button variant="outlined" size="small">
        Export
      </Button>
    </>
  );

  return (
    <WidgetTemplate
      title="Data Analysis"
      height={350}
      actions={actions}
      onFeedbackSubmit={handleFeedbackSubmit}
    >
      {/* Widget content */}
    </WidgetTemplate>
  );
}
```

### Custom Content Widget

```jsx
import WidgetTemplate from '../components/WidgetTemplate';
import { Box, Typography, Chip } from '@mui/material';

function CustomContentWidget() {
  return (
    <WidgetTemplate
      title="System Status"
      subtitle="Current system health indicators"
      height={250}
      onFeedbackSubmit={handleFeedbackSubmit}
    >
      <Box display="flex" flexDirection="column" gap={2}>
        <Box display="flex" justifyContent="space-between" alignItems="center">
          <Typography variant="body1">API Gateway</Typography>
          <Chip label="Healthy" color="success" size="small" />
        </Box>
        <Box display="flex" justifyContent="space-between" alignItems="center">
          <Typography variant="body1">Database</Typography>
          <Chip label="Warning" color="warning" size="small" />
        </Box>
        <Box display="flex" justifyContent="space-between" alignItems="center">
          <Typography variant="body1">Cache Layer</Typography>
          <Chip label="Healthy" color="success" size="small" />
        </Box>
      </Box>
    </WidgetTemplate>
  );
}
```

## Feedback System

The WidgetTemplate includes a built-in feedback system with:

### Feedback Button
- Located in the bottom-right corner of each widget
- Styled as a floating action button with chat icon
- Opens a feedback dialog when clicked

### Feedback Dialog Features
- **Feedback Type Selection**: Choose from General, Bug Report, Feature Request, Improvement, or Question
- **Rating System**: 5-star rating for widget quality
- **Text Feedback**: Multi-line text area for detailed feedback
- **Submit/Cancel Actions**: Submit feedback or cancel the dialog

### Feedback Data Structure

When feedback is submitted, the `onFeedbackSubmit` callback receives an object with:

```javascript
{
  title: "Widget Title",
  feedback: "User's feedback text",
  rating: 4, // 1-5 stars
  type: "bug", // feedback type
  timestamp: "2024-01-15T10:30:00.000Z"
}
```

### Handling Feedback

```jsx
const handleFeedbackSubmit = (feedbackData) => {
  // Send to your backend API
  fetch('/api/feedback', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(feedbackData),
  });
  
  // Or log for development
  console.log('Feedback received:', feedbackData);
};
```

## Best Practices

### 1. Consistent Heights
Use consistent height values across similar widgets:
- Small widgets: 200-250px
- Medium widgets: 300-350px
- Large widgets: 400-500px

### 2. Responsive Content
Ensure your widget content is responsive:
```jsx
<ResponsiveContainer width="100%" height={300}>
  {/* Chart content */}
</ResponsiveContainer>
```

### 3. Meaningful Titles
Use clear, descriptive titles:
- ✅ "Monthly Sales Trend"
- ❌ "Chart 1"

### 4. Helpful Subtitles
Add context with subtitles:
```jsx
<WidgetTemplate
  title="User Activity"
  subtitle="Daily active users over the last 30 days"
>
```

### 5. Appropriate Actions
Add relevant actions in the header:
- Filter controls
- Export buttons
- Refresh buttons
- Settings/configuration

## Integration with Existing Components

To convert existing widgets to use WidgetTemplate:

### Before (using Paper)
```jsx
<Paper elevation={2} sx={{ borderRadius: 3, p: 3, height: 350 }}>
  <Typography variant="h6" fontWeight="bold" mb={2}>
    Widget Title
  </Typography>
  {/* Widget content */}
</Paper>
```

### After (using WidgetTemplate)
```jsx
<WidgetTemplate
  title="Widget Title"
  height={350}
  onFeedbackSubmit={handleFeedbackSubmit}
>
  {/* Widget content */}
</WidgetTemplate>
```

## Styling Customization

The WidgetTemplate uses Material-UI's `sx` prop for styling. You can customize the appearance by modifying the component:

```jsx
// In WidgetTemplate.jsx
<Paper 
  elevation={2} 
  sx={{ 
    borderRadius: 3, 
    p: 3, 
    height, 
    width,
    position: 'relative',
    overflow: 'hidden',
    // Add custom styles here
    bgcolor: 'background.paper',
    border: '1px solid',
    borderColor: 'divider',
  }}
>
```

## Troubleshooting

### Widget Content Not Visible
- Ensure the content area has proper height
- Check if content is being clipped by overflow settings
- Verify ResponsiveContainer is used for charts

### Feedback Button Not Working
- Ensure `onFeedbackSubmit` prop is provided
- Check browser console for errors
- Verify Material-UI icons are properly imported

### Layout Issues
- Use consistent height values across similar widgets
- Ensure proper Grid container/item structure
- Check for conflicting CSS styles

## Next Steps

1. **Backend Integration**: Set up API endpoints to handle feedback submission
2. **Feedback Analytics**: Create a dashboard to view and analyze user feedback
3. **Widget Configuration**: Add configuration options for widget customization
4. **Theme Integration**: Customize widget appearance based on your theme 