import React, { useState, useEffect } from 'react';
import { Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, TableFooter, IconButton, Button, Typography, Box, CircularProgress, Alert } from '@mui/material';
import ArrowBackIosNewIcon from '@mui/icons-material/ArrowBackIosNew';
import ArrowForwardIosIcon from '@mui/icons-material/ArrowForwardIos';
import { useNavigate } from 'react-router-dom';

const statusColor = {
  solved: '#C8E6C9', // green
  threat: '#FFCDD2', // red
  pending: '#ECECEC', // gray
};

const statusText = {
  solved: 'Solved',
  threat: 'Threat',
  pending: 'Pending',
};

const EventWidgetsConfig = () => {
  const [page, setPage] = useState(0);
  const rowsPerPage = 20;
  const [events, setEvents] = useState([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate ? useNavigate() : (id) => window.location.href = `/event/${id}`;

  useEffect(() => {
    setLoading(true);
    setError(null);
    
    console.log('Fetching events from:', `/api/events?offset=${page * rowsPerPage}&limit=${rowsPerPage}`);
    
    fetch(`/api/events?offset=${page * rowsPerPage}&limit=${rowsPerPage}`)
      .then(res => {
        console.log('Raw response:', res);
        if (!res.ok) {
          throw new Error(`HTTP error! status: ${res.status}`);
        }
        return res.text().then(text => {
          console.log('Raw response text:', text);
          try {
            return JSON.parse(text);
          } catch (e) {
            throw new Error('JSON.parse error: ' + e.message + '\nRaw response: ' + text);
          }
        });
      })
      .then(data => {
        console.log('Received data:', data);
        setEvents(data.events || []);
        setTotal(data.total || 0);
        setLoading(false);
      })
      .catch(err => {
        console.error('Error fetching events:', err);
        setError(err.message);
        setLoading(false);
      });
  }, [page]);

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const maxPage = Math.ceil(total / rowsPerPage) - 1;

  return (
    <Box sx={{ flex: 1, p: 4, bgcolor: '#f3f6fa', minHeight: '100vh' }}>
      <Typography variant="h5" color='#777777' fontWeight="bold" mb={2}>Recent Events</Typography>
      
      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          Error loading events: {error}
        </Alert>
      )}
      
      <TableContainer component={Paper} sx={{ borderRadius: 3 }}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>Name</TableCell>
              <TableCell>Summary</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Tag</TableCell>
              <TableCell>Time</TableCell>
              <TableCell align="right">Action</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {loading ? (
              <TableRow>
                <TableCell colSpan={7} align="center"><CircularProgress /></TableCell>
              </TableRow>
            ) : events.length === 0 ? (
              <TableRow>
                <TableCell colSpan={7} align="center">
                  <Typography color="text.secondary">No events found</Typography>
                </TableCell>
              </TableRow>
            ) : (
              events.map((event) => (
                <TableRow key={event.id} sx={{ backgroundColor: statusColor[event.status] }}>
                  <TableCell>{event.id}</TableCell>
                  <TableCell>{event.name}</TableCell>
                  <TableCell>{event.summary}</TableCell>
                  <TableCell>
                    <Typography fontWeight="bold" color={event.status === 'solved' ? 'success.main' : event.status === 'threat' ? 'error.main' : 'text.secondary'}>
                      {statusText[event.status]}
                    </Typography>
                  </TableCell>
                  <TableCell>{event.tag}</TableCell>
                  <TableCell>{new Date(event.time).toLocaleString()}</TableCell>
                  <TableCell align="right">
                    <Button variant="contained" color="primary" size="small" onClick={() => navigate(`/event/${event.id}`)}>
                      Analyse
                    </Button>
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
          <TableFooter>
            <TableRow>
              <TableCell colSpan={7} align="right">
                <IconButton onClick={(e) => handleChangePage(e, Math.max(0, page - 1))} disabled={page === 0}>
                  <ArrowBackIosNewIcon fontSize="small" />
                </IconButton>
                <Typography component="span" mx={2}>{page + 1} / {Math.max(1, maxPage + 1)}</Typography>
                <IconButton onClick={(e) => handleChangePage(e, page + 1)} disabled={page >= maxPage}>
                  <ArrowForwardIosIcon fontSize="small" />
                </IconButton>
              </TableCell>
            </TableRow>
          </TableFooter>
        </Table>
      </TableContainer>
    </Box>
  );
};

export default EventWidgetsConfig; 