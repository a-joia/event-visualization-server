import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import InputBase from '@mui/material/InputBase';
import IconButton from '@mui/material/IconButton';
import Badge from '@mui/material/Badge';
import NotificationsIcon from '@mui/icons-material/Notifications';
import Avatar from '@mui/material/Avatar';
import { Box, Typography, alpha } from '@mui/material';

const Topbar = () => (
  <AppBar position="static" elevation={0} sx={{ bgcolor: 'white', color: 'primary.main', boxShadow: 1 }}>
    <Toolbar sx={{ justifyContent: 'space-between' }}>
      <Box sx={{ display: 'flex', alignItems: 'center', bgcolor: (theme) => alpha(theme.palette.primary.light, 0.1), borderRadius: 2, px: 2, py: 0.5 }}>
        <InputBase placeholder="Search..." sx={{ ml: 1, flex: 1 }} inputProps={{ 'aria-label': 'search' }} />
      </Box>
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
        <IconButton color="primary" sx={{ bgcolor: 'primary.lighter', '&:hover': { bgcolor: 'primary.light' } }}>
          <Badge badgeContent={2} color="error">
            <NotificationsIcon />
          </Badge>
        </IconButton>
        <Avatar sx={{ bgcolor: 'primary.main', color: 'white', fontWeight: 'bold' }}>JD</Avatar>
      </Box>
    </Toolbar>
  </AppBar>
);

export default Topbar; 