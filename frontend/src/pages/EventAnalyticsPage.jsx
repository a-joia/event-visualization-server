import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Grid, 
  Paper, 
  Typography, 
  Card, 
  CardContent, 
  Button,
  Chip,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  CircularProgress,
  Alert,
  TextField,
  Checkbox,
  FormControlLabel,
  OutlinedInput,
  ListItemText
} from '@mui/material';
import { 
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
  BarChart,
  Bar
} from 'recharts';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import TrendingDownIcon from '@mui/icons-material/TrendingDown';
import WarningIcon from '@mui/icons-material/Warning';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import ErrorIcon from '@mui/icons-material/Error';
import ScheduleIcon from '@mui/icons-material/Schedule';
import AnalyticsIcon from '@mui/icons-material/Analytics';
import FilterListIcon from '@mui/icons-material/FilterList';
import WidgetTemplate from '../components/WidgetTemplate';

// Analytics Card Component
function AnalyticsCard({ title, value, change, icon, color, subtitle }) {
  return (
    <Card sx={{ 
      borderRadius: 3, 
      boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
      transition: 'transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out',
      '&:hover': {
        transform: 'translateY(-2px)',
        boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)'
      }
    }}>
      <CardContent sx={{ p: 3 }}>
        <Box display="flex" justifyContent="space-between" alignItems="flex-start" mb={2}>
          <Box>
            <Typography variant="body2" color="text.secondary" mb={1}>
              {title}
            </Typography>
            <Typography variant="h4" fontWeight="bold" color={color}>
              {value}
            </Typography>
          </Box>
          <Box 
            sx={{ 
              p: 1.5, 
              borderRadius: 2, 
              bgcolor: `${color}.light`, 
              color: `${color}.main`,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}
          >
            {icon}
          </Box>
        </Box>
        
        {change !== null && (
          <Box display="flex" alignItems="center" mb={1}>
            {change > 0 ? (
              <TrendingUpIcon sx={{ color: 'success.main', fontSize: 16, mr: 0.5 }} />
            ) : (
              <TrendingDownIcon sx={{ color: 'error.main', fontSize: 16, mr: 0.5 }} />
            )}
            <Typography 
              variant="body2" 
              color={change > 0 ? 'success.main' : 'error.main'}
              fontWeight="medium"
            >
              {change > 0 ? '+' : ''}{change}%
            </Typography>
          </Box>
        )}
        
        <Typography variant="body2" color="text.secondary">
          {subtitle}
        </Typography>
      </CardContent>
    </Card>
  );
}

const EventAnalyticsPage = () => {
  // Line chart states
  const [kustoData, setKustoData] = useState(null);
  const [filteredData, setFilteredData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedMetrics, setSelectedMetrics] = useState('all');
  const [availableMetrics, setAvailableMetrics] = useState([]);
  const [minDate, setMinDate] = useState('');
  const [maxDate, setMaxDate] = useState('');

  // Bar chart states
  const [barData, setBarData] = useState(null);
  const [barLoading, setBarLoading] = useState(false);
  const [barError, setBarError] = useState(null);
  const [availableFeatures, setAvailableFeatures] = useState([]);
  const [selectedFeature, setSelectedFeature] = useState('');
  const [selectedValues, setSelectedValues] = useState([]);
  const [availableValues, setAvailableValues] = useState([]);
  const [barMinDate, setBarMinDate] = useState('');
  const [barMaxDate, setBarMaxDate] = useState('');
  const [binSize, setBinSize] = useState('1D');

  // Fetch kusto data on component mount
  useEffect(() => {
    fetchKustoData();
    fetchBarFeatures();
  }, []);

  // Filter data when date range changes
  useEffect(() => {
    if (kustoData) {
      filterDataByDateRange();
    }
  }, [kustoData, minDate, maxDate]);

  // Set default bar date range (15 days)
  useEffect(() => {
    const endDate = new Date();
    const startDate = new Date();
    startDate.setDate(endDate.getDate() - 15);
    
    setBarMaxDate(endDate.toISOString().split('T')[0]);
    setBarMinDate(startDate.toISOString().split('T')[0]);
  }, []);

  // Fetch bar data when parameters change
  useEffect(() => {
    if (selectedFeature && barMinDate && barMaxDate) {
      fetchBarData();
    }
  }, [selectedFeature, barMinDate, barMaxDate, binSize]);

  useEffect(() => {
    // Always select all available values if selectedValues is empty or out of sync
    if (
      availableValues.length > 0 &&
      (selectedValues.length === 0 ||
        selectedValues.some(v => !availableValues.includes(v)))
    ) {
      setSelectedValues(availableValues);
    }
  }, [availableValues]);

  const fetchKustoData = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/events/analytics/kusto-data');
      if (!response.ok) {
        throw new Error('Failed to fetch kusto data');
      }
      const data = await response.json();
      
      // Get all available metrics (excluding timestamp)
      const metrics = Object.keys(data).filter(key => key !== 'timestamp');
      setAvailableMetrics(metrics);
      
      // Transform the data for the line chart with timestamps as X-axis
      const chartData = data.timestamp.map((timestamp, index) => {
        const point = { timestamp };
        metrics.forEach(metric => {
          point[metric] = data[metric][index];
        });
        return point;
      });
      
      setKustoData(chartData);
      
      // Set initial date range
      if (chartData.length > 0) {
        const timestamps = chartData.map(point => new Date(point.timestamp));
        const minTimestamp = new Date(Math.min(...timestamps));
        const maxTimestamp = new Date(Math.max(...timestamps));
        
        setMinDate(minTimestamp.toISOString().split('T')[0]);
        setMaxDate(maxTimestamp.toISOString().split('T')[0]);
      }
      
      setError(null);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching kusto data:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchBarFeatures = async () => {
    try {
      const response = await fetch('/api/events/analytics/bar-features');
      if (!response.ok) {
        throw new Error('Failed to fetch bar features');
      }
      const data = await response.json();
      setAvailableFeatures(data.features);
      if (data.features.length > 0) {
        setSelectedFeature(data.features[0]);
      }
    } catch (err) {
      console.error('Error fetching bar features:', err);
    }
  };

  const fetchBarData = async () => {
    try {
      setBarLoading(true);
      setBarError(null);
      
      const params = new URLSearchParams({
        feature: selectedFeature,
        start_date: barMinDate,
        end_date: barMaxDate,
        bin_size: binSize
      });
      
      const response = await fetch(`/api/events/analytics/bar-data?${params}`);
      if (!response.ok) {
        throw new Error('Failed to fetch bar data');
      }
      const data = await response.json();
      
      // Extract unique values and set them as available
      const uniqueValues = [...new Set(data.data.map(item => item.value))];
      setAvailableValues(uniqueValues);
      
      // Transform data to group by date (process all data first)
      const groupedData = {};
      data.data.forEach(item => {
        if (!groupedData[item.date]) {
          groupedData[item.date] = {};
        }
        groupedData[item.date][item.value] = item.count;
      });
      
      // Convert to array format for recharts
      const transformedData = Object.keys(groupedData).map(date => {
        const dateData = { date };
        // Include all available values, not just selected ones
        uniqueValues.forEach(value => {
          dateData[value] = groupedData[date][value] || 0;
        });
        return dateData;
      });
      
      // Sort by date
      transformedData.sort((a, b) => new Date(a.date) - new Date(b.date));
      
      setBarData(transformedData);
      
    } catch (err) {
      setBarError(err.message);
      console.error('Error fetching bar data:', err);
    } finally {
      setBarLoading(false);
    }
  };

  const filterDataByDateRange = () => {
    if (!kustoData) return;

    let filtered = kustoData;

    if (minDate) {
      const minDateObj = new Date(minDate);
      filtered = filtered.filter(point => new Date(point.timestamp) >= minDateObj);
    }

    if (maxDate) {
      const maxDateObj = new Date(maxDate);
      maxDateObj.setHours(23, 59, 59, 999); // Set to end of day
      filtered = filtered.filter(point => new Date(point.timestamp) <= maxDateObj);
    }

    setFilteredData(filtered);
  };

  // Handle feedback submission
  const handleFeedbackSubmit = (feedbackData) => {
    console.log('Feedback submitted:', feedbackData);
    // Here you would typically send the feedback to your backend
    // For now, we'll just log it to the console
  };

  // Generate colors for different metrics
  const getMetricColor = (index) => {
    const colors = ['#6366f1', '#ef4444', '#10b981', '#f59e0b', '#8b5cf6', '#06b6d4', '#84cc16', '#f97316'];
    return colors[index % colors.length];
  };

  // Generate colors for bar chart values
  const getBarColor = (index) => {
    const colors = ['#3b82f6', '#ef4444', '#10b981', '#f59e0b', '#8b5cf6', '#06b6d4', '#84cc16', '#f97316', '#ec4899', '#14b8a6'];
    return colors[index % colors.length];
  };

  return (
    <Box component="main" sx={{ flex: 1, p: 4, bgcolor: '#f3f6fa', minHeight: '100vh' }}>
      {/* Header */}
      <Box mb={4}>
        <Typography variant="h4" color="black" fontWeight="bold" mb={1}>
          Event Analytics
        </Typography>
      </Box>


      {/* Analytics Cards */}
      <Grid container spacing={3} mb={3}>
        <Grid item xs={12} sm={6} md={3}>
          <AnalyticsCard
            title="Total Events"
            value="1,234"
            change={12.5}
            icon={<AnalyticsIcon />}
            color="primary"
            subtitle="This month"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <AnalyticsCard
            title="Success Rate"
            value="94.2%"
            change={2.1}
            icon={<CheckCircleIcon />}
            color="success"
            subtitle="Average response time: 45ms"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <AnalyticsCard
            title="Error Rate"
            value="5.8%"
            change={-1.2}
            icon={<ErrorIcon />}
            color="error"
            subtitle="23 errors this week"
          />
        </Grid>

      </Grid>

      {/* Line Chart */}
      <Grid container spacing={3} mb={3}>
        <Grid item xs={12}>
          <WidgetTemplate
            title="Temporal Data Analytics"
            height={400}
            actions={
              <Box display="flex" gap={2} alignItems="center">
                <TextField
                  label="From Date"
                  type="date"
                  value={minDate}
                  onChange={(e) => setMinDate(e.target.value)}
                  size="small"
                  sx={{ minWidth: 150 }}
                  InputLabelProps={{ shrink: true }}
                />
                <TextField
                  label="To Date"
                  type="date"
                  value={maxDate}
                  onChange={(e) => setMaxDate(e.target.value)}
                  size="small"
                  sx={{ minWidth: 150 }}
                  InputLabelProps={{ shrink: true }}
                />
                <FormControl size="small" sx={{ minWidth: 120 }}>
                  <InputLabel>Metrics</InputLabel>
                  <Select
                    value={selectedMetrics}
                    label="Metrics"
                    onChange={(e) => setSelectedMetrics(e.target.value)}
                  >
                    <MenuItem value="all">All Metrics</MenuItem>
                    {availableMetrics.map((metric, index) => (
                      <MenuItem key={metric} value={metric}>
                        {metric.charAt(0).toUpperCase() + metric.slice(1)}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Box>
            }
            onFeedbackSubmit={handleFeedbackSubmit}
          >
            {loading ? (
              <Box display="flex" justifyContent="center" alignItems="center" height={300}>
                <CircularProgress />
              </Box>
            ) : error ? (
              <Box display="flex" justifyContent="center" alignItems="center" height={300}>
                <Alert severity="error">{error}</Alert>
              </Box>
            ) : filteredData ? (
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={filteredData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis 
                    dataKey="timestamp" 
                    tickFormatter={(value) => {
                      try {
                        const date = new Date(value);
                        return date.toLocaleDateString();
                      } catch {
                        return value;
                      }
                    }}
                  />
                  <YAxis />
                  <Tooltip 
                    labelFormatter={(value) => {
                      try {
                        const date = new Date(value);
                        return date.toLocaleString();
                      } catch {
                        return value;
                      }
                    }}
                  />
                  <Legend />
                  {selectedMetrics === 'all' ? (
                    availableMetrics.map((metric, index) => (
                      <Line 
                        key={metric}
                        type="monotone" 
                        dataKey={metric} 
                        stroke={getMetricColor(index)}
                        strokeWidth={2}
                        name={metric.charAt(0).toUpperCase() + metric.slice(1)}
                        dot={false}
                      />
                    ))
                  ) : (
                    <Line 
                      type="monotone" 
                      dataKey={selectedMetrics} 
                      stroke={getMetricColor(availableMetrics.indexOf(selectedMetrics))}
                      strokeWidth={2}
                      dot={false}
                    />
                  )}
                </LineChart>
              </ResponsiveContainer>
            ) : (
              <Box display="flex" justifyContent="center" alignItems="center" height={300}>
                <Typography variant="body2" color="text.secondary">
                  No data available
                </Typography>
              </Box>
            )}
            <Box mt={2} textAlign="center">
              <Typography variant="body2" color="text.secondary">
                Data from Kusto backend - {selectedMetrics === 'all' ? 'All Metrics' : `Metric: ${selectedMetrics.charAt(0).toUpperCase() + selectedMetrics.slice(1)}`}
                {filteredData && ` (${filteredData.length} data points)`}
              </Typography>
            </Box>
          </WidgetTemplate>
        </Grid>
      </Grid>

      {/* Bar Chart */}
      <Grid container spacing={3} mb={3}>
        <Grid item xs={12}>
          <WidgetTemplate
            title="Categorical Data Analytics"
            height={500}
            actions={
              <Box display="flex" gap={2} alignItems="center" flexWrap="wrap">
                <TextField
                  label="From Date"
                  type="date"
                  value={barMinDate}
                  onChange={(e) => setBarMinDate(e.target.value)}
                  size="small"
                  sx={{ minWidth: 150 }}
                  InputLabelProps={{ shrink: true }}
                />
                <TextField
                  label="To Date"
                  type="date"
                  value={barMaxDate}
                  onChange={(e) => setBarMaxDate(e.target.value)}
                  size="small"
                  sx={{ minWidth: 150 }}
                  InputLabelProps={{ shrink: true }}
                />
                <FormControl size="small" sx={{ minWidth: 120 }}>
                  <InputLabel>Feature</InputLabel>
                  <Select
                    value={selectedFeature}
                    label="Feature"
                    onChange={(e) => {
                      setSelectedFeature(e.target.value);
                      setSelectedValues([]); // Reset selected values when feature changes
                    }}
                  >
                    {availableFeatures.map((feature) => (
                      <MenuItem key={feature} value={feature}>
                        {feature.charAt(0).toUpperCase() + feature.slice(1)}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
                <FormControl size="small" sx={{ minWidth: 120 }}>
                  <InputLabel>Bin Size</InputLabel>
                  <Select
                    value={binSize}
                    label="Bin Size"
                    onChange={(e) => setBinSize(e.target.value)}
                  >
                    <MenuItem value="1H">1 Hour</MenuItem>
                    <MenuItem value="1D">1 Day</MenuItem>
                    <MenuItem value="1W">1 Week</MenuItem>
                    <MenuItem value="1M">1 Month</MenuItem>
                    <MenuItem value="3M">3 Months</MenuItem>
                  </Select>
                </FormControl>
              </Box>
            }
            onFeedbackSubmit={handleFeedbackSubmit}
          >
            {/* Value Selection Controls */}
            <Box mb={2} p={2} bgcolor="grey.50" borderRadius={1}>
              <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
                <Typography variant="subtitle2" fontWeight="bold">
                  Values ({selectedValues.length} of {availableValues.length} selected)
                </Typography>
                <Box display="flex" gap={1}>
                  <Button
                    size="small"
                    variant="outlined"
                    onClick={() => setSelectedValues(availableValues)}
                    disabled={selectedValues.length === availableValues.length}
                  >
                    Select All
                  </Button>
                  <Button
                    size="small"
                    variant="outlined"
                    onClick={() => setSelectedValues([])}
                    disabled={selectedValues.length === 0}
                  >
                    Clear All
                  </Button>
                </Box>
              </Box>
              
              {/* Search for values */}
              <TextField
                size="small"
                placeholder="Search values..."
                variant="outlined"
                fullWidth
                sx={{ mb: 1 }}
                onChange={(e) => {
                  const searchTerm = e.target.value.toLowerCase();
                  if (searchTerm) {
                    const filtered = availableValues.filter(value => 
                      value.toLowerCase().includes(searchTerm)
                    );
                    setSelectedValues(filtered);
                  } else {
                    setSelectedValues(availableValues);
                  }
                }}
              />
              
              {/* Scrollable value selection */}
              <Box 
                sx={{ 
                  maxHeight: 120, 
                  overflowY: 'auto',
                  border: '1px solid',
                  borderColor: 'grey.300',
                  borderRadius: 1,
                  p: 1,
                  bgcolor: 'white'
                }}
              >
                <FormControl fullWidth size="small">
                  <Select
                    multiple
                    value={selectedValues}
                    onChange={(e) => setSelectedValues(e.target.value)}
                    input={<OutlinedInput />}
                    renderValue={(selected) => (
                      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                        {selected.slice(0, 3).map((value) => (
                          <Chip 
                            key={value} 
                            label={value} 
                            size="small" 
                            onDelete={() => {
                              setSelectedValues(selectedValues.filter(v => v !== value));
                            }}
                          />
                        ))}
                        {selected.length > 3 && (
                          <Chip 
                            label={`+${selected.length - 3} more`} 
                            size="small" 
                            variant="outlined"
                          />
                        )}
                      </Box>
                    )}
                    MenuProps={{
                      PaperProps: {
                        style: {
                          maxHeight: 300,
                        },
                      },
                    }}
                  >
                    {availableValues.map((value) => (
                      <MenuItem key={value} value={value}>
                        <Checkbox checked={selectedValues.indexOf(value) > -1} />
                        <ListItemText 
                          primary={value} 
                          primaryTypographyProps={{ fontSize: '0.875rem' }}
                        />
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Box>
            </Box>

            {barLoading ? (
              <Box display="flex" justifyContent="center" alignItems="center" height={300}>
                <CircularProgress />
              </Box>
            ) : barError ? (
              <Box display="flex" justifyContent="center" alignItems="center" height={300}>
                <Alert severity="error">{barError}</Alert>
              </Box>
            ) : barData && barData.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={barData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis 
                    dataKey="date" 
                    tickFormatter={(value) => {
                      if (binSize === "1H") {
                        return new Date(value).toLocaleString();
                      } else if (binSize === "1W") {
                        const date = new Date(value);
                        return `Week ${date.toLocaleDateString()}`;
                      } else if (binSize === "1M") {
                        // Format as "Jan 2024", "Feb 2024", etc.
                        const date = new Date(value + "-01"); // Add day to make it a valid date
                        return date.toLocaleDateString('en-US', { month: 'short', year: 'numeric' });
                      } else if (binSize === "3M") {
                        // Format as "Q1 2024", "Q2 2024", etc.
                        return value;
                      } else {
                        return new Date(value).toLocaleDateString();
                      }
                    }}
                    angle={-45}
                    textAnchor="end"
                    height={80}
                    interval={0}
                    tick={{ fontSize: 12 }}
                  />
                  <YAxis />
                  <Tooltip 
                    labelFormatter={(value) => {
                      if (binSize === "1H") {
                        return new Date(value).toLocaleString();
                      } else if (binSize === "1W") {
                        const date = new Date(value);
                        return `Week starting ${date.toLocaleDateString()}`;
                      } else if (binSize === "1M") {
                        const date = new Date(value + "-01");
                        return date.toLocaleDateString('en-US', { month: 'long', year: 'numeric' });
                      } else if (binSize === "3M") {
                        return `Quarter ${value}`;
                      } else {
                        return new Date(value).toLocaleDateString();
                      }
                    }}
                    contentStyle={{
                      backgroundColor: 'rgba(255, 255, 255, 0.95)',
                      border: '1px solid #ccc',
                      borderRadius: '4px',
                      padding: '8px'
                    }}
                  />
                  <Legend 
                    wrapperStyle={{
                      paddingTop: '10px',
                      fontSize: '12px'
                    }}
                  />
                  {selectedValues.map((value, index) => (
                    <Bar 
                      key={value}
                      dataKey={value} 
                      fill={getBarColor(index)}
                      name={value}
                    />
                  ))}
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <Box display="flex" justifyContent="center" alignItems="center" height={300}>
                <Typography variant="body2" color="text.secondary">
                  No data available
                </Typography>
              </Box>
            )}
            <Box mt={2} textAlign="center">
              <Typography variant="body2" color="text.secondary">
                Feature: {selectedFeature.charAt(0).toUpperCase() + selectedFeature.slice(1)} | 
                Bin Size: {
                  binSize === "1H" ? "1 Hour" : 
                  binSize === "1D" ? "1 Day" : 
                  binSize === "1W" ? "1 Week" :
                  binSize === "1M" ? "1 Month" :
                  binSize === "3M" ? "3 Months" : "1 Day"
                } |
                {barData && ` ${barData.length} data points`} |
                {selectedValues.length > 0 && ` ${selectedValues.length} values selected`}
              </Typography>
            </Box>
          </WidgetTemplate>
        </Grid>
      </Grid>
    </Box>
  );
};

export default EventAnalyticsPage; 