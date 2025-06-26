#!/usr/bin/env python3
"""
Page Generator Script for EventHawk Dashboard

This script creates a new page and adds it to the navigation system.
Usage: python create_page.py "Page Name"
"""

import os
import sys
import re
from pathlib import Path

def to_pascal_case(text):
    """Convert text to PascalCase"""
    words = re.sub(r'[^a-zA-Z0-9\s_]', '', text).split()
    if not words:
        return "NewPage"
    return ''.join(word.capitalize() for word in words)

def to_kebab_case(text):
    """Convert text to kebab-case"""
    words = re.sub(r'[^a-zA-Z0-9\s_]', '', text).split()
    if not words:
        return "new-page"
    return '-'.join(word.lower() for word in words)

def get_icon_suggestion(page_name):
    """Get a suggested Material-UI icon based on page name"""
    icon_mapping = {
        'dashboard': 'DashboardIcon',
        'analytics': 'AnalyticsIcon',
        'events': 'BarChartIcon',
        'users': 'PeopleIcon',
        'settings': 'SettingsIcon',
        'reports': 'AssessmentIcon',
        'monitoring': 'MonitorIcon',
        'logs': 'DescriptionIcon',
        'metrics': 'TrendingUpIcon',
        'alerts': 'NotificationsIcon',
        'config': 'TuneIcon',
        'help': 'HelpIcon',
        'about': 'InfoIcon',
        'profile': 'AccountCircleIcon',
        'search': 'SearchIcon',
        'filter': 'FilterListIcon',
        'export': 'FileDownloadIcon',
        'import': 'FileUploadIcon',
    }
    
    page_lower = page_name.lower()
    for key, icon in icon_mapping.items():
        if key in page_lower:
            return icon
    
    return 'PageviewIcon'

def create_page_template(page_name, pascal_case_name, kebab_case_name):
    """Create the JSX page template"""
    icon_name = get_icon_suggestion(page_name)
    
    template = f"""import React, {{ useState, useEffect }} from 'react';
import {{ 
  Box, 
  Typography, 
  Paper, 
  CircularProgress, 
  Alert,
  Grid,
  Card,
  CardContent,
  CardHeader,
  Divider
}} from '@mui/material';
import {{ 
  {icon_name},
  TrendingUpIcon,
  AssessmentIcon
}} from '@mui/icons-material';

const {pascal_case_name} = () => {{
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [data, setData] = useState(null);

  useEffect(() => {{
    setLoading(true);
    
    const fetchData = async () => {{
      try {{
        // TODO: Replace with your actual API endpoint
        // const response = await fetch('/api/{kebab_case_name}');
        // const result = await response.json();
        // setData(result);
        
        // Mock data for now
        setData({{
          title: '{page_name}',
          description: 'This is the {page_name} page',
          stats: [
            {{ label: 'Total Items', value: '1,234' }},
            {{ label: 'Active Items', value: '567' }},
          ]
        }});
        setLoading(false);
      }} catch (err) {{
        setError(err.message);
        setLoading(false);
      }}
    }};

    fetchData();
  }}, []);

  if (loading) {{
    return (
      <Box sx={{{{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '50vh' }}}}>
        <CircularProgress />
      </Box>
    );
  }}

  if (error) {{
    return (
      <Box sx={{{{ p: 4 }}}}>
        <Alert severity='error'>{{error}}</Alert>
      </Box>
    );
  }}

  return (
    <Box sx={{{{ flex: 1, p: 4, bgcolor: '#f3f6fa', minHeight: '100vh' }}}}>
      <Paper sx={{{{ p: 4, borderRadius: 3 }}}}>
        <Box sx={{{{ display: 'flex', alignItems: 'center', mb: 3 }}}}>
          <{icon_name} sx={{{{ fontSize: 32, mr: 2, color: 'primary.main' }}}} />
          <Typography variant='h4' fontWeight='bold'>
            {page_name}
          </Typography>
        </Box>

        <Divider sx={{{{ mb: 3 }}}} />

        {{data && (
          <>
            <Typography variant='h6' color='text.secondary' mb={{3}}>
              {{data.description}}
            </Typography>

            <Grid container spacing={{3}} mb={{4}}>
              {{data.stats.map((stat, index) => (
                <Grid item xs={{12}} sm={{6}} md={{3}} key={{index}}>
                  <Card sx={{{{ 
                    bgcolor: 'background.paper',
                    '&:hover': {{ 
                      boxShadow: 3,
                      transform: 'translateY(-2px)',
                      transition: 'all 0.2s ease-in-out'
                    }}
                  }}}}>
                    <CardContent sx={{{{ textAlign: 'center', p: 3 }}}}>
                      <Box sx={{{{ color: 'primary.main', mb: 1 }}}}>
                        <TrendingUpIcon />
                      </Box>
                      <Typography variant='h4' fontWeight='bold' color='primary.main'>
                        {{stat.value}}
                      </Typography>
                      <Typography variant='body2' color='text.secondary'>
                        {{stat.label}}
                      </Typography>
                    </CardContent>
                  </Card>
                </Grid>
              ))}}
            </Grid>

            <Card>
              <CardHeader 
                title='Content Section'
                subheader='Add your main content here'
              />
              <CardContent>
                <Typography variant='body1'>
                  This is a template for the {page_name} page. You can customize this content
                  by adding your specific components, charts, tables, or other UI elements.
                </Typography>
              </CardContent>
            </Card>
          </>
        )}}
      </Paper>
    </Box>
  );
}};

export default {pascal_case_name};
"""
    
    return template

def update_app_jsx(page_name, pascal_case_name, kebab_case_name):
    """Update App.jsx to include the new route"""
    app_jsx_path = Path("frontend/src/App.jsx")
    
    if not app_jsx_path.exists():
        print("❌ Error: App.jsx not found!")
        return False
    
    with open(app_jsx_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add import statement
    import_pattern = r'(import.*from.*;\n)'
    import_match = re.search(import_pattern, content)
    if import_match:
        new_import = f"import {pascal_case_name} from './pages/{pascal_case_name}.jsx';\n"
        content = re.sub(import_pattern, r'\1' + new_import, content, count=1)
    
    # Add route
    routes_pattern = r'(<Routes>\n)(.*?)(\n\s*</Routes>)'
    routes_match = re.search(routes_pattern, content, re.DOTALL)
    if routes_match:
        new_route = f'            <Route path="/{kebab_case_name}" element={<{pascal_case_name} />} />\n'
        content = re.sub(routes_pattern, r'\1\2' + new_route + r'\3', content, flags=re.DOTALL)
    
    with open(app_jsx_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def update_sidebar_jsx(page_name, kebab_case_name):
    """Update Sidebar.jsx to include the new navigation item"""
    sidebar_jsx_path = Path("frontend/src/components/Sidebar.jsx")
    
    if not sidebar_jsx_path.exists():
        print("❌ Error: Sidebar.jsx not found!")
        return False
    
    with open(sidebar_jsx_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Add icon import if needed
    icon_name = get_icon_suggestion(page_name)
    if f"{icon_name} from" not in content:
        # Find the icon imports section and add the new icon
        icon_imports_pattern = r'(import.*from.*@mui/icons-material.*;\n)'
        icon_imports_match = re.search(icon_imports_pattern, content)
        if icon_imports_match:
            new_icon_import = f"import {icon_name} from '@mui/icons-material/{icon_name.replace('Icon', '')}';\n"
            content = re.sub(icon_imports_pattern, r'\1' + new_icon_import, content, count=1)
    
    # Add navigation item
    nav_items_pattern = r'(const navItems = \[)(.*?)(\];)'
    nav_items_match = re.search(nav_items_pattern, content, re.DOTALL)
    if nav_items_match:
        new_nav_item = f'  {{ name: \'{page_name}\', icon: <{icon_name} />, path: \'/{kebab_case_name}\' }},\n'
        content = re.sub(nav_items_pattern, r'\1\2' + new_nav_item + r'\3', content, flags=re.DOTALL)
    
    with open(sidebar_jsx_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def main():
    if len(sys.argv) != 2:
        print("❌ Usage: python create_page.py \"Page Name\"")
        print("Example: python create_page.py \"User Management\"")
        sys.exit(1)
    
    page_name = sys.argv[1].strip()
    if not page_name:
        print("❌ Error: Page name cannot be empty")
        sys.exit(1)
    
    # Convert page name to different formats
    pascal_case_name = to_pascal_case(page_name)
    kebab_case_name = to_kebab_case(page_name)
    
    print(f"🚀 Creating new page: {page_name}")
    print(f"📁 Pascal case: {pascal_case_name}")
    print(f"🔗 Kebab case: {kebab_case_name}")
    
    # Create pages directory if it doesn't exist
    pages_dir = Path("frontend/src/pages")
    pages_dir.mkdir(parents=True, exist_ok=True)
    
    # Create the page file
    page_file_path = pages_dir / f"{pascal_case_name}.jsx"
    
    if page_file_path.exists():
        print(f"❌ Error: Page file {page_file_path} already exists!")
        sys.exit(1)
    
    # Generate page template
    page_template = create_page_template(page_name, pascal_case_name, kebab_case_name)
    
    # Write the page file
    with open(page_file_path, 'w', encoding='utf-8') as f:
        f.write(page_template)
    
    print(f"✅ Created page file: {page_file_path}")
    
    # Update App.jsx
    if update_app_jsx(page_name, pascal_case_name, kebab_case_name):
        print("✅ Updated App.jsx with new route")
    else:
        print("❌ Failed to update App.jsx")
        sys.exit(1)
    
    # Update Sidebar.jsx
    if update_sidebar_jsx(page_name, kebab_case_name):
        print("✅ Updated Sidebar.jsx with new navigation item")
    else:
        print("❌ Failed to update Sidebar.jsx")
        sys.exit(1)
    
    print("\n🎉 Page creation completed successfully!")
    print(f"📄 New page: {page_file_path}")
    print(f"🔗 Route: /{kebab_case_name}")
    print(f"🧭 Navigation: {page_name}")
    print("\n💡 Next steps:")
    print("1. Start your development server: cd frontend && npm run dev")
    print("2. Navigate to the new page in your browser")
    print("3. Customize the page content and functionality")
    print("4. Add any necessary API endpoints in the backend")

if __name__ == "__main__":
    main() 