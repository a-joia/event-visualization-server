import React, { useEffect, useState } from 'react';
import { Box, CircularProgress, Paper, Typography, Divider, Grid, Card, CardContent, CardHeader } from '@mui/material';
import { Pageview, TrendingUp } from '@mui/icons-material';
import { Alert } from '@mui/material';

const TestPage = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [data, setData] = useState(null);

  useEffect(() => {
    // Simulate an API call
    setTimeout(() => {
      setLoading(false);
      setError(null);
      setData({
        description: 'This is a sample description for the Test Page.',
        stats: [
          { value: 120, label: 'Total Users' },
          { value: 80, label: 'Active Users' },
          { value: 40, label: 'New Users' },
          { value: 20, label: 'Inactive Users' }
        ]
      });
    }, 2000);
  }, []);

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '50vh' }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box sx={{ p: 4 }}>
        <Alert severity='error'>{error}</Alert>
      </Box>
    );
  }

  return (
    <Box sx={{ flex: 1, p: 4, bgcolor: '#f3f6fa', minHeight: '100vh' }}>
      <Paper sx={{ p: 4, borderRadius: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
          <Pageview sx={{ fontSize: 32, mr: 2, color: 'primary.main' }} />
          <Typography variant='h4' fontWeight='bold'>
            Test Page
          </Typography>
        </Box>

        <Divider sx={{ mb: 3 }} />

        {data && (
          <>
            <Typography variant='h6' color='text.secondary' mb={3}>
              {data.description}
            </Typography>

            <Grid container spacing={3} mb={4}>
              {data.stats.map((stat, index) => (
                <Grid item xs={12} sm={6} md={3} key={index}>
                  <Card sx={{ 
                    bgcolor: 'background.paper',
                    '&:hover': { 
                      boxShadow: 3,
                      transform: 'translateY(-2px)',
                      transition: 'all 0.2s ease-in-out'
                    }
                  }}>
                    <CardContent sx={{ textAlign: 'center', p: 3 }}>
                      <Box sx={{ color: 'primary.main', mb: 1 }}>
                        <TrendingUp />
                      </Box>
                      <Typography variant='h4' fontWeight='bold' color='primary.main'>
                        {stat.value}
                      </Typography>
                      <Typography variant='body2' color='text.secondary'>
                        {stat.label}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>

            <Card>
              <CardHeader 
                title='Content Section'
                subheader='Add your main content here'
              />
              <CardContent>
                <Typography variant='body1'>
                  This is a template for the Test Page page. You can customize this content
                  by adding your specific components, charts, tables, or other UI elements.
                </Typography>
              </CardContent>
            </Card>
          </>
        )}
      </Paper>
    </Box>
  );
};

export default TestPage; 