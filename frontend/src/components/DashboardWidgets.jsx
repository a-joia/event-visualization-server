import * as React from 'react';
import { Card, CardContent, Typography, Grid, Paper, Box } from '@mui/material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, Legend, PieChart, Pie, Cell } from 'recharts';
import { useReactTable, getCoreRowModel, flexRender } from '@tanstack/react-table';
import WidgetTemplate from './WidgetTemplate';

const lineData = [
  { name: 'Jan', uv: 400, pv: 2400 },
  { name: 'Feb', uv: 300, pv: 1398 },
  { name: 'Mar', uv: 200, pv: 9800 },
  { name: 'Apr', uv: 278, pv: 3908 },
  { name: 'May', uv: 189, pv: 4800 },
  { name: 'Jun', uv: 239, pv: 3800 },
  { name: 'Jul', uv: 349, pv: 4300 },
];

const barData = [
  { name: 'UI', value: 12 },
  { name: 'UX', value: 18 },
  { name: 'Web', value: 32 },
  { name: 'App', value: 24 },
  { name: 'SEO', value: 14 },
];

const pieData = [
  { name: 'Subscribers', value: 8620 },
  { name: 'Visitors', value: 3200 },
  { name: 'Leads', value: 1200 },
];
const COLORS = ['#6366f1', '#34d399', '#f59e42'];

const tableData = [
  { country: 'Germany', sales: 3562, average: '56.23%' },
  { country: 'USA', sales: 2650, average: '25.33%' },
  { country: 'Australia', sales: 912, average: '12.45%' },
  { country: 'UK', sales: 689, average: '8.99%' },
];

const columns = [
  { header: 'Country', accessorKey: 'country' },
  { header: 'Sales', accessorKey: 'sales' },
  { header: 'Average', accessorKey: 'average' },
];

function ModernTable({ columns, data }) {
  const table = useReactTable({ columns, data, getCoreRowModel: getCoreRowModel() });
  return (
    <Paper elevation={2} sx={{ overflowX: 'auto', borderRadius: 2 }}>
      <table className="min-w-full bg-white divide-y divide-gray-200">
        <thead className="bg-slate-50">
          {table.getHeaderGroups().map(headerGroup => (
            <tr key={headerGroup.id}>
              {headerGroup.headers.map(header => (
                <th key={header.id} className="px-6 py-3 text-left text-xs font-bold text-slate-600 uppercase tracking-wider">
                  {flexRender(header.column.columnDef.header, header.getContext())}
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody className="divide-y divide-gray-200">
          {table.getRowModel().rows.map(row => (
            <tr key={row.id}>
              {row.getVisibleCells().map(cell => (
                <td key={cell.id} className="px-6 py-4 whitespace-nowrap text-sm text-slate-700">
                  {flexRender(cell.column.columnDef.cell, cell.getContext())}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </Paper>
  );
}

const DashboardWidgets = () => {
  // Handle feedback submission
  const handleFeedbackSubmit = (feedbackData) => {
    console.log('Feedback submitted:', feedbackData);
    // Here you would typically send the feedback to your backend
    // For now, we'll just log it to the console
  };

  return (
    <Box component="main" sx={{ flex: 1, p: 4, bgcolor: '#f3f6fa', minHeight: '100vh' }}>
      <Grid container spacing={3} mb={2}>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ borderRadius: 3, bgcolor: 'primary.main', color: 'white', boxShadow: 3 }}>
            <CardContent>
              <Typography variant="caption" sx={{ opacity: 0.8 }}>All Earnings</Typography>
              <Typography variant="h4" fontWeight="bold" mt={1}>$30,200</Typography>
              <Typography variant="caption" sx={{ bgcolor: 'rgba(255,255,255,0.15)', px: 1.5, py: 0.5, borderRadius: 2, mt: 1, display: 'inline-block' }}>+12% this month</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ borderRadius: 3, bgcolor: 'success.main', color: 'white', boxShadow: 3 }}>
            <CardContent>
              <Typography variant="caption" sx={{ opacity: 0.8 }}>Page Views</Typography>
              <Typography variant="h4" fontWeight="bold" mt={1}>290+</Typography>
              <Typography variant="caption" sx={{ bgcolor: 'rgba(255,255,255,0.15)', px: 1.5, py: 0.5, borderRadius: 2, mt: 1, display: 'inline-block' }}>+8% this week</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ borderRadius: 3, bgcolor: 'warning.main', color: 'white', boxShadow: 3 }}>
            <CardContent>
              <Typography variant="caption" sx={{ opacity: 0.8 }}>Task Completed</Typography>
              <Typography variant="h4" fontWeight="bold" mt={1}>145</Typography>
              <Typography variant="caption" sx={{ bgcolor: 'rgba(255,255,255,0.15)', px: 1.5, py: 0.5, borderRadius: 2, mt: 1, display: 'inline-block' }}>+5% today</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ borderRadius: 3, bgcolor: 'info.main', color: 'white', boxShadow: 3 }}>
            <CardContent>
              <Typography variant="caption" sx={{ opacity: 0.8 }}>Downloads</Typography>
              <Typography variant="h4" fontWeight="bold" mt={1}>500</Typography>
              <Typography variant="caption" sx={{ bgcolor: 'rgba(255,255,255,0.15)', px: 1.5, py: 0.5, borderRadius: 2, mt: 1, display: 'inline-block' }}>+2% this month</Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
      <Grid container spacing={3} mb={2}>
        <Grid item xs={12} md={8}>
          <WidgetTemplate
            title="Visitors Trend"
            height={350}
            onFeedbackSubmit={handleFeedbackSubmit}
          >
            <ResponsiveContainer width="100%" height={220}>
              <LineChart data={lineData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="uv" stroke="#6366f1" strokeWidth={2} activeDot={{ r: 8 }} />
                <Line type="monotone" dataKey="pv" stroke="#34d399" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </WidgetTemplate>
        </Grid>
        <Grid item xs={12} md={4}>
          <WidgetTemplate
            title="Project Completion"
            height={350}
            onFeedbackSubmit={handleFeedbackSubmit}
          >
            <Box display="flex" flexDirection="column" alignItems="center" justifyContent="center" height="100%">
              <ResponsiveContainer width="100%" height={180}>
                <BarChart data={barData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="value" fill="#6366f1" radius={[8, 8, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
              <Box mt={2} textAlign="center">
                <Typography variant="h5" fontWeight="bold" color="primary">76.6M</Typography>
                <Typography variant="caption" color="text.secondary">Total Earnings</Typography>
              </Box>
            </Box>
          </WidgetTemplate>
        </Grid>
      </Grid>
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <WidgetTemplate
            title="Global Sales by Top Locations"
            height={320}
            onFeedbackSubmit={handleFeedbackSubmit}
          >
            <ModernTable columns={columns} data={tableData} />
          </WidgetTemplate>
        </Grid>
        <Grid item xs={12} md={6}>
          <WidgetTemplate
            title="New Users"
            height={320}
            onFeedbackSubmit={handleFeedbackSubmit}
          >
            <Box display="flex" flexDirection="column" alignItems="center" justifyContent="center" height="100%">
              <ResponsiveContainer width="100%" height={180}>
                <PieChart>
                  <Pie data={pieData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={60} label>
                    {pieData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
              <Box mt={2} textAlign="center">
                <Typography variant="h5" fontWeight="bold" color="primary">8.62K</Typography>
                <Typography variant="caption" color="text.secondary">Subscribers</Typography>
              </Box>
            </Box>
          </WidgetTemplate>
        </Grid>
      </Grid>
    </Box>
  );
};

export default DashboardWidgets; 