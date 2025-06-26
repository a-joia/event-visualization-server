import * as React from 'react';
import Drawer from '@mui/material/Drawer';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import HomeIcon from '@mui/icons-material/Home';
import PageviewIcon from '@mui/icons-material/Pageview';
import BarChartIcon from '@mui/icons-material/BarChart';
import PeopleIcon from '@mui/icons-material/People';
import WidgetsIcon from '@mui/icons-material/Widgets';
import ViewModuleIcon from '@mui/icons-material/ViewModule';
import DescriptionIcon from '@mui/icons-material/Description';
import AnalyticsIcon from '@mui/icons-material/Analytics';
import { Box, Typography } from '@mui/material';
import { Link, useLocation } from 'react-router-dom';

const navItems = [
  { name: 'Events', icon: <BarChartIcon />, path: '/events' },
  // { name: 'Dashboard', icon: <HomeIcon />, path: '/dashboard' },
  { name: 'Analytics', icon: <AnalyticsIcon />, path: '/analytics' },
  // { name: 'CRM', icon: <PeopleIcon /> },
  // { name: 'Page Layouts', icon: <ViewModuleIcon /> },
  // { name: 'Widgets', icon: <WidgetsIcon /> },
  // { name: 'Forms', icon: <DescriptionIcon /> },
  // { name: 'Test Page', icon: <PageviewIcon />, path: '/test-page' },
];

const Sidebar = () => {
  const location = useLocation ? useLocation() : { pathname: window.location.pathname };
  return (
    <Drawer
      variant="permanent"
      sx={{
        width: 240,
        flexShrink: 0,
        [`& .MuiDrawer-paper`]: { width: 240, boxSizing: 'border-box', background: 'linear-gradient(to bottom, #1e293b, #334155)', color: 'white' },
      }}
    >
      <Box sx={{ display: 'flex', alignItems: 'center', p: 3, borderBottom: '1px solid #334155' }}>
        <Box sx={{ bgcolor: 'primary.main', borderRadius: 2, width: 40, height: 40, display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 'bold', fontSize: 10, mr: 2 }}>
          ACCIA
        </Box>
        <Typography variant="h6" fontWeight="bold" letterSpacing={1}>
        EventHawk
        </Typography>
      </Box>
      <List sx={{ mt: 2 }}>
        {navItems.map(({ name, icon, path }) => (
          <ListItem key={name} disablePadding>
            <ListItemButton
              component={Link}
              to={path}
              selected={location.pathname.startsWith(path)}
              sx={{
                borderRadius: 2,
                mx: 1,
                my: 0.5,
                '&.Mui-selected, &.Mui-selected:hover': { bgcolor: 'primary.main', color: 'white' },
                '&:hover': { bgcolor: 'primary.main', color: 'white' },
              }}
            >
              <ListItemIcon sx={{ color: 'inherit' }}>{icon}</ListItemIcon>
              <ListItemText primary={name} />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
      <Box sx={{ flexGrow: 1 }} />
      <Box sx={{ p: 2, borderTop: '1px solid #334155', textAlign: 'center', fontSize: 12, color: 'rgba(255,255,255,0.5)' }}>
        &copy;  Accia Team
      </Box>
    </Drawer>
  );
};

export default Sidebar; 