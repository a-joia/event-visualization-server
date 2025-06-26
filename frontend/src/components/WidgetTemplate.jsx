import * as React from 'react';
import { 
  Box, 
  Paper, 
  Typography, 
  IconButton, 
  Dialog, 
  DialogTitle, 
  DialogContent, 
  DialogActions, 
  Button, 
  TextField,
  Rating,
  Chip
} from '@mui/material';
import { 
  ChatBubbleOutline, 
  Close, 
  Send,
  Feedback
} from '@mui/icons-material';

// Widget Template Component
function WidgetTemplate({ 
  title, 
  children, 
  height = 300, 
  width = '100%',
  subtitle,
  actions,
  onFeedbackSubmit
}) {
  const [feedbackOpen, setFeedbackOpen] = React.useState(false);
  const [feedback, setFeedback] = React.useState('');
  const [rating, setRating] = React.useState(0);
  const [feedbackType, setFeedbackType] = React.useState('general');

  const handleFeedbackOpen = () => {
    setFeedbackOpen(true);
  };

  const handleFeedbackClose = () => {
    setFeedbackOpen(false);
    setFeedback('');
    setRating(0);
    setFeedbackType('general');
  };

  const handleFeedbackSubmit = () => {
    if (onFeedbackSubmit) {
      onFeedbackSubmit({
        title,
        feedback,
        rating,
        type: feedbackType,
        timestamp: new Date().toISOString()
      });
    }
    handleFeedbackClose();
  };

  const feedbackTypes = [
    { value: 'general', label: 'General', color: 'default' },
    { value: 'bug', label: 'Bug Report', color: 'error' },
    { value: 'feature', label: 'Feature Request', color: 'primary' },
    { value: 'improvement', label: 'Improvement', color: 'success' },
    { value: 'question', label: 'Question', color: 'info' }
  ];

  return (
    <>
      <Paper 
        elevation={2} 
        sx={{ 
          borderRadius: 3, 
          p: 3, 
          height, 
          width,
          position: 'relative',
          overflow: 'hidden'
        }}
      >
        {/* Header */}
        <Box display="flex" justifyContent="space-between" alignItems="flex-start" mb={2}>
          <Box>
            <Typography variant="h6" fontWeight="bold">
              {title}
            </Typography>
            {subtitle && (
              <Typography variant="body2" color="text.secondary" mt={0.5}>
                {subtitle}
              </Typography>
            )}
          </Box>
          {actions && (
            <Box display="flex" gap={1}>
              {actions}
            </Box>
          )}
        </Box>

        {/* Content Area */}
        <Box sx={{ height: `calc(100% - 80px)`, position: 'relative' }}>
          {children}
        </Box>

        {/* Feedback Button */}
        <Box 
          sx={{ 
            position: 'absolute', 
            bottom: 16, 
            right: 16,
            zIndex: 10
          }}
        >
          <IconButton
            onClick={handleFeedbackOpen}
            sx={{
              bgcolor: 'primary.main',
              color: 'white',
              width: 40,
              height: 40,
              boxShadow: 3,
              '&:hover': {
                bgcolor: 'primary.dark',
                transform: 'scale(1.1)',
                transition: 'all 0.2s ease-in-out'
              }
            }}
          >
            <ChatBubbleOutline />
          </IconButton>
        </Box>
      </Paper>

      {/* Feedback Dialog */}
      <Dialog 
        open={feedbackOpen} 
        onClose={handleFeedbackClose}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>
          <Box display="flex" justifyContent="space-between" alignItems="center">
            <Box display="flex" alignItems="center" gap={1}>
              <Feedback color="primary" />
              <Typography variant="h6">Plot Feedback</Typography>
            </Box>
            <IconButton onClick={handleFeedbackClose} size="small">
              <Close />
            </IconButton>
          </Box>
        </DialogTitle>
        
        <DialogContent>
          <Box display="flex" flexDirection="column" gap={3}>
 

            {/* Feedback Text */}
            <Box>
              <Typography variant="subtitle2" fontWeight="bold" mb={1}>
                How can I improve this plot?
              </Typography>
              <TextField
                fullWidth
                multiline
                rows={4}
                placeholder="Tell us what you think about this widget, any issues you've noticed, or suggestions for improvement..."
                value={feedback}
                onChange={(e) => setFeedback(e.target.value)}
                variant="outlined"
                size="small"
              />
            </Box>
          </Box>
        </DialogContent>

        <DialogActions sx={{ p: 3, pt: 1 }}>
          <Button onClick={handleFeedbackClose} color="inherit">
            Cancel
          </Button>
          <Button 
            onClick={handleFeedbackSubmit}
            variant="contained"
            startIcon={<Send />}
            disabled={!feedback.trim()}
          >
            Submit Feedback
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
}

export default WidgetTemplate; 