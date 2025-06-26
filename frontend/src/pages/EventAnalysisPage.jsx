import React, { useEffect, useState } from 'react';
import { Box, Typography, Paper, CircularProgress, Alert, Grid, Chip } from '@mui/material';
import { useParams } from 'react-router-dom';
import { marked } from 'marked';
import { AccessTime, Schedule, Timer } from '@mui/icons-material';

const EventAnalysisPage = () => {
  const { eventId } = useParams ? useParams() : { eventId: window.location.pathname.split('/').pop() };
  const [event, setEvent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setLoading(true);
    fetch(`/api/events/${eventId}`)
      .then(res => {
        if (!res.ok) throw new Error('Event not found');
        return res.json();
      })
      .then(data => {
        setEvent(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, [eventId]);

  const formatDateTime = (dateString) => {
    if (!dateString) return 'Not specified';
    return new Date(dateString).toLocaleString();
  };

  const calculateDuration = (start, end) => {
    if (!start || !end) return 'Duration not available';
    const startDate = new Date(start);
    const endDate = new Date(end);
    const diffMs = endDate - startDate;
    const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
    const diffMinutes = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60));
    return `${diffHours}h ${diffMinutes}m`;
  };

  return (
    <Box sx={{ flex: 1, p: 4, bgcolor: '#f3f6fa', minHeight: '100vh' }}>
      <Paper sx={{ p: 4, borderRadius: 3 }}>
        {loading ? (
          <CircularProgress />
        ) : error ? (
          <Alert severity="error">{error}</Alert>
        ) : event ? (
          <>
            <Typography variant="h4" fontWeight="bold" mb={3}>Event Analysis</Typography>
            
            {/* Event ID and Status */}
            <Box mb={3}>
              <Typography variant="h6" color="primary" mb={1}>Event ID: {event.id}</Typography>
              <Chip 
                label={event.status} 
                color={event.status === 'active' ? 'success' : event.status === 'pending' ? 'warning' : 'default'}
                sx={{ mr: 1 }}
              />
              <Chip label={event.tag} variant="outlined" />
            </Box>

            {/* Event Timing Information */}
            <Box mb={4}>
              <Typography variant="h6" fontWeight="bold" mb={2} display="flex" alignItems="center">
                <Schedule sx={{ mr: 1 }} />
                Event Timing
              </Typography>
              <Grid container spacing={3}>
                <Grid item xs={12} md={4}>
                  <Paper sx={{ p: 2, bgcolor: '#e3f2fd' }}>
                    <Typography variant="subtitle2" color="primary" display="flex" alignItems="center" mb={1}>
                      <AccessTime sx={{ mr: 1, fontSize: 20 }} />
                      Event Start
                    </Typography>
                    <Typography variant="body1" fontWeight="bold">
                      {formatDateTime(event.event_start)}
                    </Typography>
                  </Paper>
                </Grid>
                <Grid item xs={12} md={4}>
                  <Paper sx={{ p: 2, bgcolor: '#fff3e0' }}>
                    <Typography variant="subtitle2" color="warning.main" display="flex" alignItems="center" mb={1}>
                      <AccessTime sx={{ mr: 1, fontSize: 20 }} />
                      Event End
                    </Typography>
                    <Typography variant="body1" fontWeight="bold">
                      {formatDateTime(event.event_end)}
                    </Typography>
                  </Paper>
                </Grid>
                <Grid item xs={12} md={4}>
                  <Paper sx={{ p: 2, bgcolor: '#e8f5e8' }}>
                    <Typography variant="subtitle2" color="success.main" display="flex" alignItems="center" mb={1}>
                      <Timer sx={{ mr: 1, fontSize: 20 }} />
                      Duration
                    </Typography>
                    <Typography variant="body1" fontWeight="bold">
                      {calculateDuration(event.event_start, event.event_end)}
                    </Typography>
                  </Paper>
                </Grid>
              </Grid>
            </Box>

            {/* Original Event Time */}
            <Box mb={3}>
              <Typography variant="subtitle1" fontWeight="bold" mb={1}>Created Time:</Typography>
              <Typography>{formatDateTime(event.time)}</Typography>
            </Box>

            {/* Event Report */}
            <Box mt={4} mb={3}>
              <Typography variant="h6" fontWeight="bold" mb={2}>Event Report</Typography>
              <Box
                sx={{ bgcolor: '#f5f5f5', borderRadius: 2, p: 3, mt: 1 }}
                dangerouslySetInnerHTML={{ __html: marked.parse(event.description || 'No description available') }}
              />
            </Box>

            {/* Summary */}
            <Box mt={4}>
              <Typography variant="h6" fontWeight="bold" mb={2}>Summary</Typography>
              <Typography variant="body1" sx={{ bgcolor: '#fafafa', p: 2, borderRadius: 2 }}>
                {event.summary || 'No summary available'}
              </Typography>
            </Box>
          </>
        ) : null}
      </Paper>
    </Box>
  );
};

export default EventAnalysisPage; 